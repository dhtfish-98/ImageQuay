# Third-party notices

`src/imagequay_support/plist_codec.py` derives from the upstream modified CPython stdlib plistlib implementation. The upstream source marks this origin; Python's license is preserved in `EXTERNAL_LICENSES/CPYTHON_LICENSE`.

The retained chained-fixup layouts include upstream MachOView-derived portions. Their Apache license is preserved in `EXTERNAL_LICENSES/MACHOVIEW_CHAINEDFIXUP_APACHE_LICENSE`. The project-wide upstream MIT copyright remains in LICENSE and the original source header notices are retained.

The attributed upstream MIT Objective-C fixture sources and entitlements are
retained under `checks/sources/ktool/` from pinned ktool commit
`faed829b838dc4060b7e36f90239a52cd37f2a45`. On macOS, the local fixture
builder compiles them under ignored `Build/fixtures` for parser verification,
with linker header padding where required. These are data inputs to the tests;
the tests do not execute them. The four compiled Mach-O fixtures from earlier
releases are no longer tracked or included in source distributions. Their
published SHA-256 values remain a strict build gate. If a newer toolchain
produces different bytes, the builder reads those exact hash-checked historical
test inputs from fixed public commit `aa76377254fdb2f18286f452bbeb1512a4b034a5`
into ignored Build and reports that fallback.
