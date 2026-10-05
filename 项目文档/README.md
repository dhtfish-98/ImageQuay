> 目录已整理：文档在「项目文档」，构建、缓存与暂存输入在「Build」。从仓库根目录运行 `python3 构建.py --build`；如需使用本文原有源码命令，先运行 `python3 构建.py --stage --ci`，再进入 `Build/源码`。暂存会恢复原输入路径。现有版本和历史验证记录按各自提交理解。

# ImageQuay

防御用途、实际能力及本轮验证范围见 [DEFENSIVE_SCOPE.md](<DEFENSIVE_SCOPE.md>)。

An attributed derivative of **ktool**, retaining legitimate local analysis, editing and combination features with rewritten input, output and selected metadata services. See [ORIGIN.md](<ORIGIN.md>) for source, copyright and licensing.

ImageQuay inspects Mach-O containers, load commands, linked images, code-signing data, Objective-C metadata and Swift metadata. Its command line also retains the upstream image editing, slice combination and header/stub generation commands. The Python implementation is separated into image/container services, layout records, Swift records, support codecs and an explicit naming compatibility boundary.

The upstream terminal interface and device-specific firmware layouts require environment-specific validation; the measured local checks are listed in VALIDATION.md. Parsing and image editing operate on files supplied by the caller.

## Install

```sh
python -m pip install .
imagequay --help
```

## Development

```sh
python -m pip install '.[test]'
python checks/build_fixtures.py
python -m pytest
python -m build
```

New implementation names are listed in `SYMBOL_MAP.json`, and module/file mappings in `FILE_MAP.json`. External data labels and public compatibility aliases are kept at an explicit adapter boundary. The `guides` directory contains clearly attributed historical upstream documentation; its original commands refer to the upstream project.

See [VALIDATION.md](<VALIDATION.md>) for measured checks and remaining environmental limits.

## Compare with upstream

```sh
python checks/compare_upstream.py --upstream-root /path/to/pinned-upstream-checkout
```

The source checkout is supplied explicitly; no developer machine paths are embedded. The public CI pins the original upstream commit and repeats tests, comparison, build and installed consumption.

The macOS/Xcode fixture step compiles the three attributed upstream Objective-C
test sources into ignored `Build/fixtures`. It checks all four outputs against
the previously published fixture hashes; a different compiler result fails
closed rather than silently changing the historical parser corpus. The source
checkout and source distribution contain the fixture sources, not compiled
Mach-O files. The installed runtime does not need these test fixtures.

## Current defensive defaults (1.0.8)

Inputs are finite private snapshots up to 1 GiB; shared reads check file ranges and the rewritten metadata services check their declared regions. Editing, combining and report generation write private atomic outputs; choose a new output path or explicitly add `--overwrite` before the subcommand. Ordinary commands run offline. `imagequay --check-updates -V` explicitly reads this repository's release metadata. `--mmap` remains accepted and uses snapshot I/O. `-f` does not bypass range checks.

The source includes rewritten container/signature/I/O/VM/export services plus record and plist cores, binding/threaded-bind interpretation, chained pointer metadata, symbol-table bounds and loader dependency order. Version 1.0.5 corrected only the offline ARM64_32 Apple-tool test for an exact empty placeholder display. Version 1.0.6 moves historical upstream guide support files into 项目文档. Version 1.0.7 corrects the version shown when running directly from uninstalled source. Version 1.0.8 generates the existing test corpus under Build from attributed sources; none of these patches change Mach-O parsing behavior. External cache targets remain unresolved until the caller provides their bases; compressed chained symbols remain explicitly unsupported. Objective-C type/graph readers and Swift static nominal/field readers use a finite immutable metadata view. Advanced ObjC shared-cache layouts, Swift generic/resilient tails and full demangling, GUI, header/TBD/rendering/support algorithms and CPU/firmware interpretation still require work; see [VALIDATION.md](<VALIDATION.md>). It does not claim CVP eligibility or complete project rewriting.
