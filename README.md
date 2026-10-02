# ImageQuay

防御用途、实际能力及本轮验证范围见 [DEFENSIVE_SCOPE.md](DEFENSIVE_SCOPE.md)。

An attributed derivative of **ktool**, retaining legitimate local analysis, editing and combination features with rewritten input, output and selected metadata services. See [ORIGIN.md](ORIGIN.md) for source, copyright and licensing.

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
python -m pytest
python -m build
```

New implementation names are listed in `SYMBOL_MAP.json`, and module/file mappings in `FILE_MAP.json`. External data labels and public compatibility aliases are kept at an explicit adapter boundary. The `guides` directory contains clearly attributed historical upstream documentation; its original commands refer to the upstream project.

See [VALIDATION.md](VALIDATION.md) for measured checks and remaining environmental limits.

## Compare with upstream

```sh
python checks/compare_upstream.py --upstream-root /path/to/pinned-upstream-checkout
```

The source checkout is supplied explicitly; no developer machine paths are embedded. The public CI pins the original upstream commit and repeats tests, comparison, build and installed consumption.

## Current defensive defaults (1.0.2)

Inputs are finite private snapshots up to 1 GiB; shared reads check file ranges and the rewritten metadata services check their declared regions. Editing, combining and report generation write private atomic outputs; choose a new output path or explicitly add `--overwrite` before the subcommand. Ordinary commands run offline. `imagequay --check-updates -V` explicitly reads this repository's release metadata. `--mmap` remains accepted and uses snapshot I/O. `-f` does not bypass range checks.

This release rewrites the shared container layer, signature reader, file/output services, VM mapping/cache and export trie, with region/work bounds for binding/function metadata. Full ObjC/Swift, chained-fixup, remaining loader, GUI, document generation and support-core rewrites are still required; see [VALIDATION.md](VALIDATION.md). It does not claim CVP eligibility or complete algorithm rewriting.
