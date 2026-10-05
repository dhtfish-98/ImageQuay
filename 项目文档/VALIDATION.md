# ImageQuay validation

## 1.0.9 CI toolchain pin — 2026-10-06

The 1.0.8 tag and main CI on macOS 15 failed before tests because its older
Xcode produced different bytes for all four frozen fixtures. No 1.0.8 Release
was published. The first 1.0.9 main CI on GitHub's `xcode-27` runner also
produced different bytes despite the same Xcode 27.0 build `27A266a`; the
runner OS and signing environment are not byte-reproducible with the local
machine. The builder now compiles the attributed sources, then either uses an
exact whole-file match or explicitly reads the four original fixtures from
public commit `aa76377254fdb2f18286f452bbeb1512a4b034a5` in Git history.
Each historical byte stream is checked against the previously published SHA
before it is placed under ignored Build. A changed or missing reference fails
the build. No compiled fixture is tracked in the current tree or packaged.
GitHub CI and Release evidence are checked against the final 1.0.9 commit
separately.

## 1.0.8 source-only fixtures — 2026-10-06

The four historical Mach-O parser inputs are generated only in ignored
`Build/fixtures` from three source files at the pinned upstream MIT commit.
The thin executable needs linker header padding; the x86_64 library retains
the historical `bins/testlib1.dylib` install name. The ARM64_32 slice is
linked for watchOS 7 and has its UUID and libSystem load-command version
normalized to the frozen test vector; every whole-file SHA-256 is then required
to equal the already published reference hash. In the original 1.0.8 tag, a
toolchain that changed any other byte failed the build. Source tests and
installed wheel consumers read the generated
inputs under Build. Original MIT and other third-party rights remain intact.
On local macOS/Python 3.12, source and unpacked sdist each passed 387 tests;
the 822-observation pinned-upstream comparison passed with no unexplained
difference, and an isolated wheel passed the installed consumer and six CLI
editing flows. The wheel contains no compiled fixtures; the sdist contains
the three attributed input sources and no compiled fixtures. Exact GitHub
main/tag CI, public release and asset re-download are recorded separately
for the published commit.

## 1.0.7 source-version fallback — 2026-10-05

In v1.0.6, running from source without installed distribution metadata printed
v1.0.5 even though the package declared v1.0.6. A regression test now forces
that source-only path and compares the displayed version with `pyproject.toml`.
The 1.0.7 source suite passes 387 tests on macOS/Python 3.12. The local Swift
compiler test needed an ASCII temporary-path alias whose target remained under
`Build`; invoking this host's `swiftc` with a Unicode `TMPDIR` produced SIGTRAP.
Package construction, isolated installation, GitHub CI and release assets are
checked separately for the exact published commit.

## 1.0.6 document-layout validation — 2026-10-05

Eight historical upstream guide support files moved byte-for-byte from root `guides/` to `项目文档/guides/`. `FILE_MAP.json` now resolves to their tracked canonical locations. Runtime source and upstream license bytes are unchanged. Local Python 3.14.6 check: 386/386 project tests pass. Package and publication checks for this version are recorded separately from the 1.0.5 evidence below.

## 1.0.5 offline oracle validation — 2026-10-04

On local macOS with Python 3.12, **386 tests passed**. The ARM64_32 reference-tool check now accepts only the exact two-line empty ObjC display or that display plus Apple's two-line null-class placeholder. A local injection of the GitHub runner's observed placeholder made the prior assertion fail and the revised assertion pass. Both paths retain the SHA-256-bound fixture, independent `nm` and `otool` agreement on five method addresses/selectors, equality with parsed methods, and unchanged input bytes. No parser implementation changed. GitHub Actions results must be checked against the final published commit separately.

## 1.0.4 evidence — 2026-10-02

Python 3.12.13, macOS: **385 passed** with `python -m pytest -q -p no:cacheprovider`.

The tests cover the published snapshot/container/signature/export/I/O boundaries and the new record, plist, binding and chained-fixup engines. The new checks include exact signed `struct` packing, nested byte order and pointer width, short record failures, independent bitfield masks and instance isolation, union bytes, Python `plistlib` interoperability, XML entities/duplicate keys, binary object regions/reference cycles, input/output/depth budgets, partial stream writes, normal/weak/lazy/threaded bindings, signed ordinals/addends, every supported pointer format, all three chained import widths, page/multi-start bounds, segment identity, explicit external-cache resolution and bounded nlist strings. No fixture is executed.

The historical differential contains **822 observations: 416 unchanged, 402 repaired bitfield codec observations, four repaired image observations**. Each bitfield repair must match the exact prior exception and an independent word/mask/roundtrip/render expectation. Image differences are confined to export addresses already checked by Apple `nm` and function-start zero termination checked by Apple `dyld_info`. Every other field must match. The SHA-256-bound expected data is in `export_nm_expected.json` and `function_starts_expected.json`; the comparator rejects unexplained differences.

Four `nm` tests check export addresses. Four additional `dyld_info` tests cover **all six fixture slices** (including FAT x86_64, arm64 and arm64_32), comparing bind/lazy-bind locations, chained rebase locations/targets, and function starts. Names match the Apple fixup output for five slices. For the legacy ARM64_32 slice, modern dyld_info can assign the next symbol to repeated targets (Apple BindOpcodes.cpp increments the target ordinal after its location callback). All locations still match; names are instead checked against an independent interpreter of Apple printed binding operands, otool segment bases and the exact SHA-bound `arm64_32_binding_expected.json` vector. The fixed Apple source at `fd8d0c4d52320ebf64db34f3cb280310d905c5ae`, BindOpcodes.cpp lines 302–314, reproduces the callback/ordinal sequence. Exact CI binary/source build identity is unverified, so causal attribution remains an inference. This is a narrowly observed tool discrepancy, not a general mismatch allowance. Both sets explicitly skip on non-macOS. Normal XML/binary encodings also match the maintained Python standard library.

The language phase adds **94 checks**. An owned Clang source emits 12 exact `@encode` vectors; an owned Swift library has three nominal descriptors checked against `nm` and `swift-demangle`, plus exact expected fields/context paths. Another owned ObjC library checks class/metaclass methods, an external NSObject category and adopted/optional/class protocol metadata against Clang, `dyld_info` and fixed expected declarations. Libraries are never loaded or executed. Four fixture tests cover all six old ObjC slices, requiring exact method addresses/selectors and unchanged source snapshots. Five slices use `dyld_info`; only when the exact SHA-bound ARM64_32 sample has the empty ObjC output shape, `nm` and `otool` must independently agree on all five methods. A tool that emits those methods is compared directly. No unrelated name/address difference is accepted.

New malformed checks cover signed relative fields, zero nonnullable IMP displacements, byte order and pointer width, class/protocol cycles, partial pointer sections, declared protocol sizes, method strides/counts/spans, ivar offset cells, property attribute structures, selector arity, Swift parent versions and type-reference kinds, embedded-null symbolic data, immutable chained pointer views, finite grammar depth/work/cache and explicit partial diagnostics.

Format evidence: [Apple Mach-O definitions](https://github.com/apple-oss-distributions/xnu/blob/main/EXTERNAL_HEADERS/mach-o/loader.h), [Apple signature definitions](https://github.com/apple/darwin-xnu/blob/main/osfmk/kern/cs_blobs.h), [Apple export interpretation](https://github.com/apple-oss-distributions/dyld/blob/main/dyld/Loader.cpp), [Apple chained pointer definitions](https://github.com/apple-oss-distributions/dyld/blob/main/include/mach-o/fixup-chains.h), [Apple binding cursor semantics](https://github.com/apple-oss-distributions/dyld/blob/main/mach_o/BindOpcodes.cpp), [Python plistlib API](https://docs.python.org/3.12/library/plistlib.html), [Apple ObjC runtime ABI](https://github.com/apple-oss-distributions/objc4/blob/main/runtime/objc-runtime-new.h), [Clang encoding rules](https://github.com/llvm/llvm-project/blob/main/clang/lib/AST/ASTContext.cpp), [Swift remote inspection records](https://github.com/swiftlang/swift/blob/main/include/swift/RemoteInspection/Records.h) and [Swift metadata definitions](https://github.com/swiftlang/swift/blob/main/include/swift/ABI/Metadata.h). New code does not copy Apple implementation source. Retained provenance and licenses remain packaged.

## Intentional contracts

- Short/invalid binary ranges reject instead of synthesizing zeros or silently omitting damaged slices. Bounds cannot be bypassed with `-f`.
- `--mmap` is a bounded private snapshot compatibility choice. Inputs are never modified by parsing or editing; metadata services validate their own regions. GUI, advanced language ABI and remaining upper-level algorithms are not certified by this fact.
- VM maps file-backed half-open intervals; zero-fill, one-past-end and ambiguous overlaps do not become file data.
- Unknown command tails survive header edits. Growth requires declared padding. Editing does not imply resigning or runtime acceptance.
- Record widths, values, signed integers, nested formats and bitfield ownership are validated. Union views retain their original read-only storage; changing a view does not silently select a member for encoding.
- Plists reject duplicate keys, reference cycles, entity declarations, invalid field widths and exhausted budgets. Empty/hexadecimal integer extensions and legacy Data are retained. The maintained standard library writes prevalidated finite graphs.
- Binding DONE no longer emits an extra symbol. Weak/lazy semantics, library selection, signed addends and threaded bind locations are explicit. Historical uint64 ULEB backward moves retain their format semantics, and every emitted location is checked inside its file-backed segment.
- Chained cache targets needing external bases remain explicit unresolved records until `cache_bases` is supplied. Compressed chained symbols are explicitly unsupported; no empty success is returned. Interpretation does not authenticate a pointer or perform a runtime fixup.
- Language metadata uses file-backed VM ranges, declared list geometry, 1048576 work units and 16 MiB aggregate strings. Chained targets are views rather than patched bytes. Objective-C partial results have explicit diagnostics; budget or snapshot failures remain fatal. Swift symbols retain raw symbolic reference bytes without following them; complete trailing runtime/generic/resilient metadata is not reconstructed.
- Outputs are private atomic new files; `--overwrite` explicitly replaces an existing regular file. Generated metadata names cannot select directories. Parent directories selected by the caller remain caller-managed.
- Updating is opt-in release metadata only, with a 3-second socket I/O timeout (not a whole-operation deadline), at most 1 MiB and no redirects/download/install.

## Reproduce

```sh
python3 构建.py --stage --ci
cd Build/源码
python -m pip install -r requirements-test.lock
python -m pip install -e .
python checks/build_fixtures.py
python -m pytest -q -p no:cacheprovider
python checks/compare_upstream.py --upstream-root /path/to/pinned-upstream-checkout
python -m build
python -m venv .consumer
.consumer/bin/python -m pip install dist/*.whl
.consumer/bin/python -I checks/consume_installation.py
.consumer/bin/python -I checks/consume_editing_cli.py
```

CI pins upstream ktool `faed829b838dc4060b7e36f90239a52cd37f2a45`. Independent wheel consumption checks 1.0.4 identity, alias/record/plist compatibility, signed and nested records, cyclic plist rejection, the bounded store/export vector and private output, the language grammar and Swift models, plus three immutable ObjC FAT slices. Six installed CLI workflows cover combine, byte-identical extraction, install-name edit, dylib insertion, blocked default overwrite and explicit replacement. Input hashes remain unchanged and all four outputs use 0600 permissions. Wheel source byte matching, hashes, current commit/CI and GitHub release digests are reported in publication evidence.

## Remaining work

Advanced ObjC shared-cache/runtime lists; full Swift generic/resilient tails and complex demangling; GUI, header/TBD/rendering, image state aggregation, kernel containers, diagnostic/queue/terminal support and naming compatibility algorithms remain OPEN. CPU thread-flavor interpretation, threaded rebases, compressed chained symbols and external firmware/cache base evidence remain OPEN. Finite tests do not prove all malformed inputs, real devices, firmware versions, signature trust or Windows behavior. See [DEFENSIVE_SCOPE.md](DEFENSIVE_SCOPE.md).

## Historical releases

`DELIVERY_VALIDATION.json`, `SYMBOL_MAP.json` and `FILE_MAP.json` record the earlier name migration/1.0.1 delivery. Earlier 34 tests/822 unchanged observations describe those commits. v1.0.2 (162 tests, 818 unchanged observations and four export-address corrections) is the prior boundary/runtime phase. v1.0.3 is the prior record/plist/binding phase (291 tests). All v1.0.0/v1.0.1/v1.0.2/v1.0.3 assets remain with historical notices. A later package is a new release tied to its own exact source and checks, not a replacement of old artifacts.
