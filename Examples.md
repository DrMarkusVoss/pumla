# `pumla` usage examples
These are diagrams from the `./test/examples` section. You find the
source code of the .puml files that form the example model repository
there. In order to get the example running on your computer, you need
to run first `pumla init`, then `pumla update`" in the examples directory, 
because the paths in the model repo file (./test/examples/modelrepo_json.puml)
need to be updated to the directory structure on your computer. Currently
the model repo file has the paths from the structure as I have it on my
machine. You can't run the pumla update from the main path of pumla, as
it is setup to update the architecture model repo of the pumla tool itself.
The examples section will be ignored from the top level. So you have to go
down to the examples and call the pumla update from that directory.

If you are changing the contents of the examples to play around, in order for a
change to become alive, you need to call `pumla update` again. cd 

## E#0: Create Re-usable Elements
Here are examples for defining elements, that can be easily re-used on different
diagrams with the possibility to switch on different levels of detail.

## E#0.1: General Re-usable Asset
See here an example for the definition of a Re-usable Element using the
`PUMLAReUsableAsset` macro:
[./test/examples/tempSensorA/tempSensorA.puml](test/examples/WheatherStation/tempSensorA/tempSensorA.puml)

![](test/examples/WheatherStation/pics/tempSensorA.png)

## E#0.2: Re-usable Class
Here is an example for the definition of a Re-usable Class using the
`PUMLAReUsableClass` macro:
[./test/examples/anotherClass/anotherClass.puml](test/examples/WheatherStation/anotherClass/anotherClass.puml)

![](test/examples/WheatherStation/pics/anotherClass.png)

## E#0.3: Re-usable, fully-instantiable Class
Here is an example for the definition of a Re-usable Class using the
`PUMLAFullyInstantiatableClass` macro:
[./test/examples/CWeather/CWeather.puml](test/examples/WheatherStation/CWeather/CWeather.puml)

![](test/examples/WheatherStation/pics/CWeather.png)

## E#1: Show all Elements
See, how classes and other elements are mixed on this diagram. That works only
when internals are not shown. If you want to expose internals, you need to wrap
the classes into notes. Use the "`PUMLAPutAllElementsMix()`" macro for that
purpose (see example from the main page).

[./test/examples/allElements.puml](test/examples/WheatherStation/allElements.puml)

![](test/examples/WheatherStation/pics/allElements.png)

## E#2: Cheat Sheet
### E#2.1: Simple Cheat Sheet
[./test/examples/cheatSheet.puml](test/examples/WheatherStation/cheatSheet.puml)


![](test/examples/WheatherStation/pics/cheatSheet.png)

### E#2.2: Cheat Sheet with all attributes
[./test/examples/cheatSheetAdvanced.puml](test/examples/WheatherStation/cheatSheetAdvanced.puml)


![](test/examples/WheatherStation/pics/cheatSheetAdvanced.png)


## E#3: Instantiation

[./test/examples/instantiationExample.puml](test/examples/WheatherStation/instantiationExample.puml)

### E#3.1: `$PUMVarShowInstantiationRel = %true()`
<img src="./test/examples/pics/instantiationExample_true.png" width="50%"/>


### E#3.2: `$PUMVarShowInstantiationRel = %false()`
<img src="./test/examples/pics/instantiationExample_false.png" width="50%"/>

### E#4: Show dedicated elements, hide some unwanted internal ones
See this example diagram description, putting
all elements of the example model repository with stereotype "block" 
onto the diagram. Then some relations are added and unnecessary elements
removed.

[./test/examples/easyAllElementsOverview.puml](test/examples/WheatherStation/easyAllElementsOverview.puml)

... leading to this diagram:

![](test/examples/WheatherStation/pics/easyAllElementsOverview.png)


### E#5: Definition of a re-usable model element
[./test/examples/wirelessUnit/wirelessUnit.puml](test/examples/WheatherStation/wirelessUnit/wirelessUnit.puml)

![](test/examples/WheatherStation/pics/wirelessUnit.png)

### E#6: Element injection
Only element "tempSys" is put on the diagram, but internals are shown.
If you look at the definition of the "tempSys" model element, you do not see the internals
defined. They are injected via the "PUMLAInjectChildElements" macro. This tells
`pumla` to insert into this element all other elements that call "tempSys" their parent in
the second line of the .puml file. That way, the parent element definition does
not need to be changed when another child has been created. The children themselves are
designed for usage in the parent context, so they should not be used without their parent.

See the "PUMLAInjectChildElements" macro call in this file:

[./test/examples/tempSys.puml](test/examples/WheatherStation/tempSys.puml)

See the reference to the parent element "tempSys" in the
second line of this file. That makes it appear as part
within the "tempSys" element when the internals of "tempSys"
are shown:

[./test/examples/displayTemp/displayTemp.puml](test/examples/WheatherStation/displayTemp/displayTemp.puml)

See that there is only one element, the "tempSys" element,
put onto the diagram of this file:

[./test/examples/injectedElementsExample.puml](test/examples/WheatherStation/injectedElementsExample.puml)

See the resulting diagram for that file:

![](test/examples/WheatherStation/pics/injectedElementsExample.png)

### E#7: Classes
This example shows how classes can be re-used.

See this file, for how the public and private methods are handled differently in the
definition of a re-usable class:

[./test/examples/CWeather/CWeather.puml](test/examples/WheatherStation/CWeather/CWeather.puml)

See here, how instances of the class element are created, which is similar to the
creation of other instances. But with this mechanisms the instances do not get the
methods and attributes from its parent class:

[./test/examples/CWeather/WeatherInstances.puml](test/examples/WheatherStation/CWeather/WeatherInstances.puml)

As CWeather is modelled as "FullyInstantiatableClass", you can also create instances
that inherit the methods and attributes of CWeather, see the definition of these
instances here:

[./test/examples/CWeather/FurtherWeatherInstances.puml](test/examples/WheatherStation/CWeather/FurtherWeatherInstances.puml)

See here how the class, the class instances and another non-class-diagram-compatible
element are mixed on one diagram. You also see the difference between the two different
instantiation mechanisms.

[./test/examples/classesExample1.puml](test/examples/WheatherStation/classesExample1.puml)

![](test/examples/WheatherStation/pics/classesExample1.png)

### E#8: Dynamic Behaviour - State Machine
In the following example, we just put the "Temperature Sensor B" element onto the
diagram.
[./test/examples/exampleDynBehStateMachine.puml](test/examples/WheatherStation/exampleDynBehStateMachine.puml)

This leads to this nice diagram, as internals are shown for that element, both
static and dynamic internals:

![](test/examples/WheatherStation/pics/exampleDynBehStateMachine.png)

That element has both, static and dynamic elements in its inside, see here in this file:

[./test/examples/tempSensorB/tempSensorB.puml](test/examples/WheatherStation/tempSensorB/tempSensorB.puml)

In order to be able to mix static and dynamic elements (PlantUML has limited capabilities regarding that),
the different `pumla` macros take care of that by wrapping the dynamic element details diagram into
a note. That way, static and dynamic world can co-exist. In order to create traceability between
the elements, pumla doubles the dynamic element as a rectangle and attaches the note to it.
That way you can also create links between the static and dynamic elements.

See here, how the dynamic element is defined, which is conceptually similar to the static
re-usable element definitions:

[./test/examples/tempSensorB/publicState.puml](test/examples/WheatherStation/tempSensorB/publicState.puml)

So basically, it uses the same `pumla` mechanism, the file marking and the PUMLAPARENT. The parent
mechanism is not really necessary for this example, but it fits logically. Additionaly, re-usable
description files of dynamic elements must be marked with PUMLADYN. That is because it is almost
impossible to differentiate a static and a dynamic description from one another. On the other hand
there are a lot of pitfalls when you try to mix them, which is a problem for the re-use use case. 
That is why in `pumla` you explicitly mark the dynamic descriptions.


### E#9: Dynamic Behaviour - Sequence Diagram
In the following example, we just put the "Temperature Sensor A" element onto the
diagram.
[./test/examples/exampleDynBehSequence.puml](test/examples/WheatherStation/exampleDynBehSequence.puml)

This leads to this nice diagram, as internals are shown for that element, both
static and dynamic internals:

![](test/examples/WheatherStation/pics/exampleDynBehSequence.png)

That element has both, static and dynamic elements in its inside, see here in this file:

[./test/examples/tempSensorA/tempSensorA.puml](test/examples/WheatherStation/tempSensorA/tempSensorA.puml)

In order to be able to mix static and dynamic elements (PlantUML has limited capabilities regarding that),
the different `pumla` macros take care of that by wrapping the dynamic element details diagram into
a note. That way, static and dynamic world can co-exist. In order to create traceability between
the elements, pumla doubles the dynamic element as a rectangle and attaches the note to it.
That way you can also create links between the static and dynamic elements.

See here, how the dynamic element is defined, which is conceptually similar to the static
re-usable element definitions:

[./test/examples/tempSensorA/internalSequence.puml](test/examples/WheatherStation/tempSensorA/internalSequence.puml)

So basically, it uses the same `pumla` mechanism, the file marking and the PUMLAPARENT. The parent
mechanism is not really necessary for this example, but it fits logically. Additionaly, re-usable
description files of dynamic elements must be marked with PUMLADYN. That is because it is almost
impossible to differentiate a static and a dynamic description from one another. On the other hand
there are a lot of pitfalls when you try to mix them, which is a problem for the re-use use case. 
That is why in `pumla` you explicitly mark the dynamic descriptions.

### E#10: Dynamic Behaviour - Re-using and extending a Sequence Diagram
If you have a dynamic element like "internalSequence" and put it onto a diagram like here...

[./test/examples/exampleSimpleReUseSequence.puml](test/examples/WheatherStation/exampleSimpleReUseSequence.puml)

... then you get automatically a sequence diagram which looks like this:

![](test/examples/WheatherStation/pics/exampleSimpleReUseSequence.png)

Now, you can extend this diagram, by referencing the elements from inside this re-usable description and
using it for further messages/calls or additional notes.

Look into this example, that takes the "internalSequence" and extends it with several
notes and additional messages:

[./test/examples/exampleReUseAndModifyBehaviour.puml](test/examples/WheatherStation/exampleReUseAndModifyBehaviour.puml)

The result is then the following diagram:

![](test/examples/WheatherStation/pics/exampleReUseAndModifyBehaviour.png)

### E#11: Dynamic Behaviour - Re-using and extending a State Machine 
Look into this example, that takes the "publicState" state machine and extends it with several
additional states and transitions:
[./test/examples/exampleReUseAndModifyStateMachine.puml](test/examples/WheatherStation/exampleReUseAndModifyStateMachine.puml)

The result is then the following diagram:

![](test/examples/WheatherStation/pics/exampleReUseAndModifyStateMachine.png)


### E#12: Using Tagged Values as selection mechanism
See the following example, where all elements with the Tag/Value pair
"Vendor"/"C Ltd." are put on the diagram.

Example code:

[./test/examples/taggedValuesFromMR.puml](test/examples/WheatherStation/taggedValuesFromMR.puml)

Example diagram:

![](test/examples/WheatherStation/pics/taggedValuesFromMR.png)


### E#13: Cheat Sheets for Connections and Relations
See the following example for putting cheat sheets showing
all connections and all relations of the model repository
onto a diagram. The cheat cheets are encapsulated in nodes
just to be able to make the layout "top-down" instead
of next to each other.

[./test/examples/exampleCheatSheetsConsAndRels.puml](test/examples/WheatherStation/exampleCheatSheetsConsAndRels.puml)

Example diagram:

![](test/examples/WheatherStation/pics/exampleCheatSheetsConsAndRels.png)

### E#14: Using tagged values for selecting relations to put on the diagram
See the following example that puts 3 elements onto the diagram. After that, for one element its dependent relations that additionally
have the right tag/value combination attached are put onto the diagram.


[./test/examples/taggedRelationExample.puml](test/examples/WheatherStation/taggedRelationExample.puml)

Example diagram:

![](test/examples/WheatherStation/pics/taggedRelationExample.png)


### E#15: Using Diagram Filters
### E#15.1: Filter-Out Elements
See the following PlantUML code where two diagram filters are
applied to elements of type "node" and elements of stereotype
"external System". Therefore, out of the 4 elements put onto
the diagram only 2 are shown, the other 2 are filtered out:

[./test/examples/elementFilterExample.puml](test/examples/WheatherStation/elementFilterExample.puml)

Example diagram:

![](test/examples/WheatherStation/pics/elementFilterExample.png)

### E#15.2: Filter-In Elements
The following example uses Filter-In macros with tag/value filtering.
Furthermore in this example, the filter values are changes in the mid
of the diagram.

[./test/examples/advancedFilterExample.puml](test/examples/WheatherStation/advancedFilterExample.puml)

See the note in the diagram for details:

![](test/examples/WheatherStation/pics/advancedFilterExample.png)


### E#16: Error Notes
Error notes appear if you try to access (e.g. put) an element of the pumla
model repository that does not exist. In that case, pumla puts a red note
onto the diagram explaining the error and naming the alias of the element 
that you tried to access and that does not exist.

See the following example, where we put 3 elements onto the diagram that 
exist, and then try to put another element with alias `w5` onto the diagram,
and that element does not exist. That is why you get the red error note.


[./test/examples/errorNotesExample.puml](test/examples/WheatherStation/errorNotesExample.puml)

Example diagram:

![](test/examples/WheatherStation/pics/errorNotesExample.png)

Error notes are only created if you directly try to access an element that 
you name by its alias. They will not occur e.g. if you call the macro 
`PUMLAPutAllClasses()` and there are no classes in the repository. In that 
case, it is not an error. You may call this macro to explore the content of 
the repository, and if no classes are in there then it is no error. And then
showing just nothing is also no error, but a correct behaviour.


