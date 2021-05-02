# `pumla` usage examples
These are diagrams from the `./test/examples` section. You find the
source code of the .puml files that form the example model repository
there.

## E#1: Show all Elements
See, how classes and other elements are mixed on this diagram. That works only
when internals are not shown. If you want to expose internals, you need to wrap
the classes into notes. Use the "`PUMLAPutAllElementsMix()`" macro for that
purpose (see example from the main page).

[./test/examples/allElements.puml](./test/examples/allElements.puml)

![](./test/examples/pics/allElements.png)

## E#2: Cheat Sheet
### E#2.1: Simple Cheat Sheet
[./test/examples/cheatSheet.puml](./test/examples/cheatSheet.puml)


![](./test/examples/pics/cheatSheet.png)

### E#2.2: Cheat Sheet with all attributes
[./test/examples/cheatSheetAdvanced.puml](./test/examples/cheatSheetAdvanced.puml)


![](./test/examples/pics/cheatSheetAdvanced.png)


## E#3: Instantiation

[./test/examples/instantiationExample.puml](./test/examples/instantiationExample.puml)

### E#3.1: `$PUMVarShowInstantiationRel = %true()`
<img src="./test/examples/pics/instantiationExample_true.png" width="50%"/>


### E#3.2: `$PUMVarShowInstantiationRel = %false()`
<img src="./test/examples/pics/instantiationExample_false.png" width="50%"/>

### E#4: Show dedicated elements, hide some unwanted internal ones
[./test/examples/easyOverviewSysVarB.puml](./test/examples/easyOverviewSysVarB.puml)

![](./test/examples/pics/easyOverviewSysVarB.png)

### E#5: Definition of a re-usable model element
[./test/examples/wirelessUnit/wirelessUnit.puml](./test/examples/wirelessUnit/wirelessUnit.puml)

![](./test/examples/pics/wirelessUnit.png)

### E#6: Element injection
Only element "tempSys" is put on the diagram, but internals are shown.
If you look at the definition of the "tempSys" model element, you do not see the internals
defined. They are injected via the "PUMLAInjectChildElements" macro. This tells
pumla to insert into this element all other elements that call "tempSys" their parent in
the second line of the .puml file. That way, the parent element definition does
not need to be changed when another child has been created. The children themselves are
designed for usage in the parent context, so they should not be used without their parent.

See the "PUMLAInjectChildElements" macro call in this file:

[./test/examples/tempSys.puml](./test/examples/tempSys.puml)

See the reference to the parent element "tempSys" in the
second line of this file. That makes it appear as part
within the "tempSys" element when the internals of "tempSys"
are shown:

[./test/examples/displayTemp/displayTemp.puml](./test/examples/displayTemp/displayTemp.puml)

See that there is only one element, the "tempSys" element,
put onto the diagram of this file:

[./test/examples/injectedElementsExample.puml](./test/examples/injectedElementsExample.puml)

See the resulting diagram for that file:

![](./test/examples/pics/injectedElementsExample.png)

### E#7: Classes
This example shows how classes can be re-used.

See this file, for how the public and private methods are handled differently in the
definition of a re-usable class:

[./test/examples/CWeather/CWeather.puml](./test/examples/CWeather/CWeather.puml)

See here, how instances of the class element are created, which is similar to the
creation of other instances:

[./test/examples/CWeather/WeatherInstances.puml](./test/examples/CWeather/WeatherInstances.puml)

See here how the class, the class instances and another non-class-diagram-compatible
element are mixed on one diagram:

[./test/examples/classesExample1.puml](./test/examples/classesExample1.puml)

![](./test/examples/pics/classesExample1.png)