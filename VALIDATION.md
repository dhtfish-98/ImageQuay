# Validation

Local validation date: 2026-10-02 (Asia/Tokyo). Python 3.12.13.

- Upstream tests: 30 passed.
- Derivative tests: 34 passed.
- Independent upstream/derivative observations: 822; zero differences. Return values, serialized keys/display labels, binary output and observed exception types/messages are checked.
- Scope-resolved source/module mappings are in SYMBOL_MAP.json and FILE_MAP.json. Python protocol hooks, framework callbacks, serialized field labels, enum identifiers, public compatibility aliases and fixed fixture bytes are explicit exceptions. Obsolete upstream packaging and Sphinx build configuration were replaced by the current build/CI configuration.

## Reproduce

```sh
python -m pip install -r requirements-test.lock
python -m pip install -e .
python -m pytest -q
python checks/compare_upstream.py --upstream-root /path/to/pinned-upstream-checkout
python -m build
python -m pip install dist/*.whl
python -I checks/consume_installation.py
```

The GitHub workflow checks out upstream commit `faed829b838dc4060b7e36f90239a52cd37f2a45` separately. Package builds, independent consumer installation and final package/source hash checks are recorded in DELIVERY_VALIDATION.json when completed. Source comparison does not establish device or external-service behavior.

## Limits

- Real-device/firmware-version validation and interactive terminal GUI: OPEN.
- Inherited upstream parser limitations are preserved; the comparison observes original exceptions rather than silently repairing upstream behavior.
- The old test assumed a larger linker header/segment. The isolated x86_64 fixture uses clang header padding; three fat slices were built (x86_64, arm64, arm64_32). Current SDK lacks original armv7 link inputs, so armv7 fixture rebuilding is OPEN.

Runtime setuptools is pinned to 80.10.2 because the retained upstream code relies on pkg_resources.

Release v1.0.1 restores executable file modes and the first-line position of interpreter directives. Distribution metadata now uses derivative release 1.0.1; upstream format/version constants retain their protocol values. No algorithm changes were made.

## 2026-10-02 capability review

The current runtime entry points, file/process/network capabilities and attribution were reviewed. See DEFENSIVE_SCOPE.md for the exact paths and remaining limitations. This documentation update does not claim another execution of the historical full test suite, a rewrite of every upstream algorithm, or CVP eligibility. GitHub CI for the new commit is separate evidence.
