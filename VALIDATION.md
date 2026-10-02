# ImageQuay validation

## Current 1.0.3 evidence — 2026-10-02

Python 3.12.13, macOS: **289 passed** with `python -m pytest -q -p no:cacheprovider`.

The tests cover the published snapshot/container/signature/export/I/O boundaries and the new record, plist, binding and chained-fixup engines. The new checks include exact signed `struct` packing, nested byte order and pointer width, short record failures, independent bitfield masks and instance isolation, union bytes, Python `plistlib` interoperability, XML entities/duplicate keys, binary object regions/reference cycles, input/output/depth budgets, partial stream writes, normal/weak/lazy/threaded bindings, signed ordinals/addends, every supported pointer format, all three chained import widths, page/multi-start bounds, segment identity, explicit external-cache resolution and bounded nlist strings. No fixture is executed.

The historical differential contains **822 observations: 416 unchanged, 402 repaired bitfield codec observations, four repaired image observations**. Each bitfield repair must match the exact prior exception and an independent word/mask/roundtrip/render expectation. Image differences are confined to export addresses already checked by Apple `nm` and function-start zero termination checked by Apple `dyld_info`. Every other field must match. The SHA-256-bound expected data is in `export_nm_expected.json` and `function_starts_expected.json`; the comparator rejects unexplained differences.

Four `nm` tests check export addresses. Four additional `dyld_info` tests cover **all six fixture slices** (including FAT x86_64, arm64 and arm64_32), comparing bind/lazy-bind locations, chained rebase locations/targets, and function starts. Names match the Apple fixup output for five slices. For the legacy ARM64_32 slice, modern dyld_info can assign the next symbol to repeated targets (Apple BindOpcodes.cpp increments the target ordinal after its location callback). All locations still match; names are instead checked against Apple printed binding operands and the exact SHA-bound `arm64_32_binding_expected.json` vector. This is a documented tool discrepancy, not a general mismatch allowance. Both sets explicitly skip on non-macOS. Normal XML/binary encodings also match the maintained Python standard library.

Format evidence: [Apple Mach-O definitions](https://github.com/apple-oss-distributions/xnu/blob/main/EXTERNAL_HEADERS/mach-o/loader.h), [Apple signature definitions](https://github.com/apple/darwin-xnu/blob/main/osfmk/kern/cs_blobs.h), [Apple export interpretation](https://github.com/apple-oss-distributions/dyld/blob/main/dyld/Loader.cpp), [Apple chained pointer definitions](https://github.com/apple-oss-distributions/dyld/blob/main/include/mach-o/fixup-chains.h), [Apple binding cursor semantics](https://github.com/apple-oss-distributions/dyld/blob/main/mach_o/BindOpcodes.cpp), and [Python plistlib API](https://docs.python.org/3.12/library/plistlib.html). New code does not copy Apple implementation source. Retained provenance and licenses remain packaged.

## Intentional contracts

- Short/invalid binary ranges reject instead of synthesizing zeros or silently omitting damaged slices. Bounds cannot be bypassed with `-f`.
- `--mmap` is a bounded private snapshot compatibility choice. Inputs are never modified by parsing or editing; metadata services validate their own regions. GUI/ObjC/Swift upper-level algorithms are not certified by this fact.
- VM maps file-backed half-open intervals; zero-fill, one-past-end and ambiguous overlaps do not become file data.
- Unknown command tails survive header edits. Growth requires declared padding. Editing does not imply resigning or runtime acceptance.
- Record widths, values, signed integers, nested formats and bitfield ownership are validated. Union views retain their original read-only storage; changing a view does not silently select a member for encoding.
- Plists reject duplicate keys, reference cycles, entity declarations, invalid field widths and exhausted budgets. Empty/hexadecimal integer extensions and legacy Data are retained. The maintained standard library writes prevalidated finite graphs.
- Binding DONE no longer emits an extra symbol. Weak/lazy semantics, library selection, signed addends and threaded bind locations are explicit. Historical uint64 ULEB backward moves retain their format semantics, and every emitted location is checked inside its file-backed segment.
- Chained cache targets needing external bases remain explicit unresolved records until `cache_bases` is supplied. Compressed chained symbols are explicitly unsupported; no empty success is returned. Interpretation does not authenticate a pointer or perform a runtime fixup.
- Outputs are private atomic new files; `--overwrite` explicitly replaces an existing regular file. Generated metadata names cannot select directories. Parent directories selected by the caller remain caller-managed.
- Updating is opt-in release metadata only, with a 3-second socket I/O timeout (not a whole-operation deadline), at most 1 MiB and no redirects/download/install.

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
.consumer/bin/python -I checks/consume_editing_cli.py
```

CI pins upstream ktool `faed829b838dc4060b7e36f90239a52cd37f2a45`. Independent wheel consumption checks 1.0.3 identity, alias/record/plist compatibility, signed and nested records, cyclic plist rejection, the bounded store/export vector and private output. Six installed CLI workflows cover combine, byte-identical extraction, install-name edit, dylib insertion, blocked default overwrite and explicit replacement. Input hashes remain unchanged and all four outputs use 0600 permissions. Wheel source byte matching, hashes, current commit/CI and GitHub release digests are reported in publication evidence.

## Remaining work

Full ObjC/Swift, GUI, header/TBD/rendering, Swift name decoding, diagnostic/queue/terminal support and naming compatibility algorithms remain OPEN. CPU thread-flavor interpretation, threaded rebases, compressed chained symbols and external firmware/cache base evidence remain OPEN. Finite tests do not prove all malformed inputs, real devices, firmware versions, signature trust or Windows behavior. See [DEFENSIVE_SCOPE.md](DEFENSIVE_SCOPE.md).

## Historical releases

`DELIVERY_VALIDATION.json`, `SYMBOL_MAP.json` and `FILE_MAP.json` record the earlier name migration/1.0.1 delivery. Earlier 34 tests/822 unchanged observations describe those commits. v1.0.2 (162 tests, 818 unchanged observations and four export-address corrections) is the prior boundary/runtime phase. All v1.0.0/v1.0.1/v1.0.2 assets remain with historical notices. A later package is a new release tied to its own exact source and checks, not a replacement of old artifacts.
