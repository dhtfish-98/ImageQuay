# ImageQuay validation

## Current 1.0.2 rewrite evidence — 2026-10-02

Python 3.12.13, macOS. `python -m pytest -q -p no:cacheprovider`: **162 passed**.

The current tests check exact reads and all-or-nothing in-memory patches; 0–31 byte truncations; 32/64-bit and big/little-endian headers; command sizes/counts/regions; FAT bounds, overlaps and identities; unknown command tails and Unicode edits; private no-clobber/atomic outputs and explicit regular-file replacement; symlink/FIFO input rejection; failed/concurrent output publication; string bounds/cache invalidation; 64-bit LEB vectors; SuperBlob slot bounds; export cycles/regions/flags/reexports/resolvers and numeric addresses; huge VM ranges without per-page allocation; file-backed half-open translations; record-cache identity; finite binding repetition and explicit trie path/name budgets; verified header padding; restored error state; and default offline CLI behavior. Update metadata is tested with injected responses; no actual network response is asserted by those mocks.

Historical differential observer: **822 observations, 818 unchanged**, four image observations contain intentional export address corrections. `compare_upstream.py` permits only those exact address changes; every other field must match. `export_nm_expected.json` binds each fixture's SHA-256 and expected export addresses. Four tests independently check every listed address with Apple `nm`; the corrected addresses use every bit of the terminal ULEB128. On non-macOS, those four oracle tests are explicitly skipped.

New bounded readers and metadata interpretation follow [Apple Mach-O record definitions](https://github.com/apple-oss-distributions/xnu/blob/main/EXTERNAL_HEADERS/mach-o/loader.h), [Apple signature blob definitions](https://github.com/apple/darwin-xnu/blob/main/osfmk/kern/cs_blobs.h), and [Apple dyld export terminal interpretation](https://github.com/apple-oss-distributions/dyld/blob/main/dyld/Loader.cpp). No Apple source is copied into the new implementation.

## Intentional contract changes

- Invalid/truncated reads reject instead of silently returning shorter slices or zero integers. Corrupt FAT slices reject rather than yielding a partial architecture list. Count/size disagreement, invalid or overlapping slot/range declarations and missing terminators reject.
- `use_mmaped_io`/`--mmap` are accepted compatibility choices using bounded private snapshot bytes. No input file is modified.
- VM translations use half-open file-backed intervals. Zero-fill and one-past-end addresses are not file data; ambiguous overlaps reject. Old tests which deliberately shifted `__TEXT` into another file-backed mapping now expect an error.
- Unknown command tails are preserved during edits. Header growth requires declared padding; `-f` does not bypass input bounds. Editing is not resigning or runtime validation.
- Correct export addresses replace the inherited low-7-bit-loss decoding. Construction methods previously returning empty `None` now report `NotImplementedError` where creation remains unimplemented.
- Output defaults are private atomic new files. `--overwrite` makes existing regular output replacement explicit; input/output symlinks are rejected. Metadata names cannot select output directories.
- Updates are explicitly chosen with `--check-updates`, restricted to this repository's release metadata with a 3-second socket I/O timeout (not a whole-operation deadline), and never install/download code. Runtime distribution version now uses `importlib.metadata`; packaging is an explicit dependency.

## Reproduce

```sh
python -m pip install -r requirements-test.lock
python -m pip install -e .
python -m pytest -q -p no:cacheprovider
python checks/compare_upstream.py --upstream-root /path/to/pinned-upstream-checkout
python -m build
python -m venv .consumer
.consumer/bin/python -m pip install dist/*.whl
.consumer/bin/python -I checks/consume_installation.py
```

CI separately checks out ktool commit `faed829b838dc4060b7e36f90239a52cd37f2a45`. Installed consumption checks 1.0.2 metadata, alias/record/plist compatibility, the bounded byte store, a numeric export vector and private no-clobber output outside the source import path. The release's wheel/source content hashes and matching CI are supplied with the publication evidence, rather than inferred from a build status.

The independent installed CLI also passed six workflows: combine, byte-identical extraction, install-name edit, dylib-command insertion, blocked default overwrite and explicit regular-file replacement. Every input stayed unchanged and all four produced files used 0600 permissions. CI repeats these workflows from the installed wheel.

## Work still required

See [DEFENSIVE_SCOPE.md](DEFENSIVE_SCOPE.md) for exact rewritten modules and inherited work. Full ObjC/Swift, chained fixups, SymbolTable/remaining loader behavior, GUI, header/TBD generators and plist/record core rewrites remain OPEN. Binding threaded interpretation, all malformed inputs, real devices, firmware versions and manual GUI interaction remain OPEN. macOS is the current tested platform; Windows-specific curses behavior has not been verified.

## Historical releases

`DELIVERY_VALIDATION.json`, `SYMBOL_MAP.json` and `FILE_MAP.json` describe the earlier naming/module migration and 1.0.1 delivery, not the new implementation's full coverage. Earlier 34 tests/822 unchanged observations and unchanged-algorithm claims belong to those historical commits. v1.0.0/v1.0.1 assets remain downloadable with historical notices; they contain earlier parser behavior. The new 1.0.2 release is a bounded-input/runtime rewrite with the explicit limits above.
