# Third-party notices

`src/imagequay_support/plist_codec.py` derives from the upstream modified CPython stdlib plistlib implementation. The upstream source marks this origin; Python's license is preserved in `EXTERNAL_LICENSES/CPYTHON_LICENSE`.

The retained chained-fixup layouts include upstream MachOView-derived portions. Their Apache license is preserved in `EXTERNAL_LICENSES/MACHOVIEW_CHAINEDFIXUP_APACHE_LICENSE`. The project-wide upstream MIT copyright remains in LICENSE and the original source header notices are retained.

The Mach-O fixture bytes in checks/bins were compiled locally from upstream MIT test sources for deterministic parser verification, with modern linker header padding where required. They are data fixtures, not executables invoked by the tests.
