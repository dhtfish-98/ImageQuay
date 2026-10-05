#!/usr/bin/env python3
"""Build or restore frozen Mach-O fixtures from attributed project history.

All output is created under Build. The exact hash gate prevents a different
SDK from silently changing the historical parser test corpus. When the
compiler differs, the pinned earlier public commit supplies the same bytes.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "checks" / "sources" / "ktool"
BUILD = ROOT / "Build"
FIXTURES = BUILD / "fixtures"
EXPECTED_SOURCE = {
    "testbin1.m": "ef37a73819f143de58a88c8d2b91acdc45e758facccbc5ebfa7fa602528df5e2",
    "testlib1.m": "ef4fe3a6824b0325d5fc0e25fb7215dc0f1c3a0b8911bc096f730a85247ae5d7",
    "testent.xml": "3fd02302a76e2ce4b5c28aa104f5f25491a263471702fafc1aa144b9bcb4f738",
}
EXPECTED_FILES = ("testbin1", "testbin1.fat", "testbin1.signed", "testlib1.dylib")
REFERENCE_COMMIT = "aa76377254fdb2f18286f452bbeb1512a4b034a5"
ARM64_32_UUID = bytes.fromhex("ac68909a2286344aad953bf0615d35f2")
FROZEN_LIBSYSTEM_VERSION = 1336 << 16


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(*args: str) -> str:
    result = subprocess.run(args, text=True, capture_output=True, timeout=90)
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {args!r}\n{result.stderr[-3000:]}")
    return result.stdout.strip()


def published_reference(name: str, expected_sha256: str) -> bytes:
    """Read a frozen fixture from the exact pre-migration public commit."""
    if name not in EXPECTED_FILES:
        raise ValueError("Unknown reference fixture")
    result = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{REFERENCE_COMMIT}:checks/bins/{name}"],
        capture_output=True, timeout=30,
    )
    if result.returncode:
        raise RuntimeError("Pinned public fixture is unavailable: " + name)
    if hashlib.sha256(result.stdout).hexdigest() != expected_sha256:
        raise ValueError("Pinned public fixture hash changed: " + name)
    return result.stdout


def normalize_arm64_32(path: Path) -> int:
    """Restore only the frozen UUID and libSystem SDK version load command.

    The original ARM64_32 test vector used libSystem 1336.0.0. Newer SDKs
    change that load-command version and hence ld's content-derived UUID;
    the final whole-file SHA gate confirms the remaining bytes are identical.
    """
    raw = bytearray(path.read_bytes())
    if len(raw) < 28 or struct.unpack_from("<I", raw)[0] != 0xFEEDFACE:
        raise ValueError("ARM64_32 fixture does not have a Mach-O 32-bit header")
    count = struct.unpack_from("<I", raw, 16)[0]
    offset = 28
    uuid_count = libsystem_count = 0
    previous_version = None
    for _ in range(count):
        if offset + 8 > len(raw):
            raise ValueError("Mach-O load command exceeds fixture")
        command, size = struct.unpack_from("<II", raw, offset)
        if size < 8 or offset + size > len(raw):
            raise ValueError("Malformed Mach-O load command")
        if command == 0x1B:
            if size != 24:
                raise ValueError("Unexpected LC_UUID size")
            raw[offset + 8:offset + 24] = ARM64_32_UUID
            uuid_count += 1
        elif command == 0xC:
            if size < 24:
                raise ValueError("Malformed LC_LOAD_DYLIB")
            name_offset = struct.unpack_from("<I", raw, offset + 8)[0]
            if name_offset >= size:
                raise ValueError("Dylib name leaves load command")
            name = bytes(raw[offset + name_offset:offset + size]).split(b"\0", 1)[0]
            if name == b"/usr/lib/libSystem.B.dylib":
                previous_version = struct.unpack_from("<I", raw, offset + 16)[0]
                struct.pack_into("<I", raw, offset + 16, FROZEN_LIBSYSTEM_VERSION)
                libsystem_count += 1
        offset += size
    if uuid_count != 1 or libsystem_count != 1:
        raise ValueError("Expected exactly one LC_UUID and one libSystem load command")
    path.write_bytes(raw)
    return previous_version


def main() -> None:
    if sys.platform != "darwin":
        raise SystemExit("Mach-O fixture regeneration requires macOS/Xcode")
    if BUILD.is_symlink() or FIXTURES.is_symlink():
        raise ValueError("Build and fixture output must be real directories")
    for name, expected in EXPECTED_SOURCE.items():
        if digest(SOURCE / name) != expected:
            raise ValueError("Pinned upstream fixture source changed: " + name)
    manifest = json.loads((ROOT / "checks" / "export_nm_expected.json").read_text())
    if set(manifest) != set(EXPECTED_FILES):
        raise ValueError("Frozen fixture manifest must name all four outputs")
    BUILD.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="fixture-build-", dir=BUILD) as temporary:
        work = Path(temporary)
        x86 = work / "x86"
        x86.mkdir()
        source_bin = str(SOURCE / "testbin1.m")
        source_lib = str(SOURCE / "testlib1.m")
        run("xcrun", "clang", source_bin, "-o", str(work / "testbin1"),
            "-framework", "Foundation", "-arch", "x86_64", "-Wl,-headerpad,0x4000")
        run("xcrun", "clang", source_lib, "-o", str(work / "testlib1.dylib"),
            "-framework", "Foundation", "-dynamiclib", "-arch", "x86_64",
            "-install_name", "bins/testlib1.dylib")
        run("xcrun", "clang", source_bin, "-o", str(x86 / "testbin1"),
            "-framework", "Foundation", "-arch", "x86_64")
        run("xcrun", "clang", source_bin, "-o", str(work / "testbin1.arm64"),
            "-framework", "Foundation", "-arch", "arm64")
        watch_sdk = run("xcrun", "--show-sdk-path", "--sdk", "watchos")
        arm64_32 = work / "testbin1.arm64_32"
        run("xcrun", "clang", source_bin, "-o", str(arm64_32),
            "-L", str(SOURCE), "-framework", "Foundation",
            "-Wl,-undefined,dynamic_lookup", "-target", "arm64_32-apple-watchos7.0",
            "-isysroot", watch_sdk)
        previous_version = normalize_arm64_32(arm64_32)
        run("xcrun", "lipo", "-create", str(x86 / "testbin1"),
            str(work / "testbin1.arm64"), str(arm64_32),
            "-output", str(work / "testbin1.fat"))
        signed = work / "testbin1.signed"
        shutil.copyfile(x86 / "testbin1", signed)
        run("codesign", "-s", "-", "--entitlements", str(SOURCE / "testent.xml"),
            str(signed), "--force")
        hashes = {name: digest(work / name) for name in EXPECTED_FILES}
        mismatch = {name: (hashes[name], manifest[name]["sha256"])
                    for name in EXPECTED_FILES if hashes[name] != manifest[name]["sha256"]}
        mode = "SOURCE_REPRODUCED"
        if mismatch:
            # SDK/OS-dependent linker and signing bytes are not accepted as a
            # replacement corpus. Restore only the exact SHA-bound historical
            # inputs into ignored Build and expose the difference in the log.
            for name in EXPECTED_FILES:
                (work / name).write_bytes(
                    published_reference(name, manifest[name]["sha256"])
                )
            mode = "PINNED_HISTORY_REFERENCE"
        FIXTURES.mkdir(exist_ok=True)
        for name in EXPECTED_FILES:
            destination = FIXTURES / name
            if destination.is_symlink():
                raise ValueError("Fixture destination must not be a symlink")
            staged = FIXTURES / (name + ".new")
            shutil.copyfile(work / name, staged)
            staged.chmod(0o644)
            os.replace(staged, destination)
    print(json.dumps({
        "status": "PASS_FROZEN_FIXTURES",
        "mode": mode,
        "compiler_sha256": hashes,
        "fixture_directory": str(FIXTURES),
        "upstream_commit": "faed829b838dc4060b7e36f90239a52cd37f2a45",
        "reference_commit": REFERENCE_COMMIT if mode == "PINNED_HISTORY_REFERENCE" else None,
        "libsystem_version_before_normalization": previous_version,
        "sha256": {name: digest(FIXTURES / name) for name in EXPECTED_FILES},
    }, sort_keys=True))


if __name__ == "__main__":
    main()
