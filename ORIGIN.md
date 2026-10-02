# Origin and attribution

ImageQuay is a derived, reorganized version of ktool.

- Source: https://github.com/0cyn/ktool.git
- Baseline commit: `faed829b838dc4060b7e36f90239a52cd37f2a45`
- Baseline tree: `fd8ba431159b265bc539cb185daf597a92cd469c`
- License: MIT; the original license and copyright are retained.

The original algorithms and project history belong to their upstream authors. This derivative introduces renamed implementation bindings resolved by lexical scope, renamed modules, and explicit adapters separating public data labels from internal implementation names. It does not claim independent authorship of upstream code or approval by any verification program.

Public CLI flags, structured data keys, enum identifiers, Python framework hooks, legacy external API aliases, resource formats and compatibility labels are deliberate naming exceptions. The compatibility module provides separate wire/display labels; it is not a hidden copy of the old implementation.

## 1.0.2 runtime rewrite

The container/byte layer and signature reader were substantively rewritten, with new local I/O/release metadata/byte-region services, interval VM mapping, typed record cache, lossless header editing and export decoding. The CLI uses these services while retaining legal local editing/combination/report functionality. Remaining inherited algorithms are listed in DEFENSIVE_SCOPE.md. Earlier name mapping files are historical migration records; they do not certify new source equivalence or authorship. Copyright and MIT notices remain. Implementation and review were assisted by Codex; this does not establish the CVP applicant's independent authorship of upstream code.

## 1.0.3 record and metadata rewrite

The record and plist engines were replaced with new finite layout/XML/object-graph architectures. New binding and chained-fixup modules separate declared metadata, pointer locations and unresolved external targets; loader dependency registration and symbol-string regions were rewritten. Maintained Python plistlib writes validated finite graphs; the retained CPython license and upstream copyrights remain included. Normal capabilities and independent Apple/stdlib evidence are recorded in VALIDATION.md. ObjC/Swift, UI, document rendering and remaining support algorithms remain inherited and OPEN. This is Codex-assisted maintenance of an attributed derivative, not evidence of independent authorship or CVP approval.
