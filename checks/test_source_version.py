"""Keep the source-tree CLI version aligned with the declared package version."""

from pathlib import Path
import os
import re
import subprocess
import sys


def test_uninstalled_source_reports_declared_version():
    root = Path(__file__).resolve().parents[1]
    metadata = (root / "pyproject.toml").read_text()
    match = re.search(r'(?m)^version\s*=\s*"([^"]+)"', metadata)
    assert match is not None
    declared = match.group(1)

    code = """
import importlib.metadata as metadata
original = metadata.version
def without_imagequay(name):
    if name == 'imagequay':
        raise metadata.PackageNotFoundError(name)
    return original(name)
metadata.version = without_imagequay
from imagequay.formatting import quay_version_output
quay_version_output()
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src")
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=root,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )
    assert result.stdout.startswith(f"ImageQuay v{declared};")
