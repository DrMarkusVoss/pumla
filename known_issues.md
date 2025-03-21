# Known Issues and Bugs

### Boxes for "internals" and "internals hidden" are shown at the same time wrongly
There is a bug in some PlantUML versions, where the "internals" and "internals hidden"
rectangles from nested elements inside re-usable assets are not properly removed.

This is a side-effect of using "allowmixing".

Here is the bug report and an example on the PlantUML website:

https://forum.plantuml.net/19823/allowmixing-has-side-effect-on-remove

#### Observed on `pumla` example:
[test/examples/simple/hierarchicalSystem/sysArch_with_some_internals.puml](test/examples/simple/hierarchicalSystem/sysArch_with_some_internals.puml)

#### affected PlantUML version:
- v1.2024.7 and newer (possibly also older versions)

#### older PlantUML version without this bug:
- v1.2022.6 (maybe also newer versions)

#### allegedly fixed with PlantUML version:
- v1.2024.8


