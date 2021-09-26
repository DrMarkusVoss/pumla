# `pumla` Modelling Guideline

*Rationale:*

Why do we need a modelling guideline giving us rules to follow?


In order to make re-use of single-source PlantUML models, it is necessary to
follow some modelling rules in order to be easily able to create a tool that
enables the re-use. So these rules and guidelines help us to keep the re-use
tooling `pumla` simple in its implementation. Without these rules, a lot 
more effort would need to go into the tooling to allow the same 
functionality.

Furthermore, this guideline will give you hints on how to achieve certain use 
cases using `pumla`, like e.g. variant management.

## Some Principles
### Static vs. Dynamic 
When modelling the elements, first model the static aspect with the atomic 
definition of the element. Then, in separate files, add the dynamic aspects.
Put internal dynamic behaviour descriptions of an element into its
internals definition.

Define instances in separate files. Instance files may contain more than one
instance definition for convenience, also that brings with it
some drawbacks: when putting an instance from a file with more
instances defined in it onto a diagram, then all the instances
appear on the diagram. You then have to remove the unwanted instances
by hand (via PlantUML "remove" command).

PlantUML has limitations regarding the mixing of static and dynamic
elements. `pumla` works around that with macros that encapsulate the 
dynamic aspects into notes so that they can be mixed with or embedded
in static elements. Of course, for pure dynamic diagrams this is not
needed, and also pure dynamic element definitions can be re-used.

### Relations vs. Connections
Connections are typed dataflows. Therefore, a connection is only valid
between two interfaces. 

Relations are between two elements. Also a general information flow can be a
relation, but as relation it is not concretely defined with what information
flows in detail as specified by an interface.

### Diagrams
Diagrams can be created using elements of the model repository, as well as by 
adding also all kinds of extra stuff to the diagram using standard PlantUML code.

`pumla` offers a lot of convenience commands, that let you put the contents of 
the model repository onto a diagram in a very efficient way. So, if you want to
keep track of all the architecture elements that are modelled in your repository,
you can just use the command `"PUMLAPutAllElements()"` and you get all the model
elements of your model repository put onto the diagram. After e.g. a git pull 
you just need to run `pumla update`, the model repo will be updated and
after that your diagram will automatically contain all elements of the updated version.
So this feature can really help you keeping an overview on your architecture if
you are working with a bigger team with a lot of different people adding re-usable
architecture elements.

You can also expose different parts of the re-usable elements by using the different
`pumla`-specific global variables. E.g. you can decide to show or not to show the
note with the description of a re-usable element, or show/not show the internals of
a re-usable element.

## Lightweight Variant Management
- use tagged values (also on relations and connections)
- create variants by creating a diagram with a filter on the respective
  tagged values of the elements
- see the examples for filtering and tagged values on the examples page

# Rules

## Rule: `pumla` files are valid PlantUML files 
We only use PlantUML language in the `pumla` architecture descriptions.
The `pumla` macros are valid PlantUML code (PlantUML and its preprocessor
commands). Therefore, using `pumla` macros of course is also valid usage.

### *Rationale*
That way, we can re-use the `pumla` model elements in each and every PlantUML diagram
(of course, as long as the `pumla_macros.puml` are included).

## Rule: Atomicity of Model Element descriptions
In the model files where the re-usable elements are modelled, do 
model only one element, do not model further other model elements
or dependencies to other elements. Therefore, do not include other
model files from here. You should have one file per model element.

### *Rationale*
When we want to re-use a model element in a diagram, we need to include
it's *.puml file into our diagram puml file. If another file is included 
by the model element file of the element we want to have on our
diagram, then automatically also the other (dependent) model element of 
the included puml file gets onto our diagram (which we may not want).
So, in order to be able to re-use elements on element level, these files
describing/modelling the elements should be atomic, meaning no other files
are included. Dependencies of this element to other elements are to be
modelled in a separate file, therefore.

### *Example*

Wrong:
```PlantUML
file: helloworld.puml
@startuml
!include displayText.puml

component "Hello World" as helloworld {

}

helloworld-->displayText : uses
@enduml
```
Problem here: *displayText* is included in the definition
of the helloWorld component.

Right:
```PlantUML
file: helloworld.puml

@startuml
component "Hello World" as helloworld {
}

file: helloworld_rel.puml

@startuml
' File describing the relations/dependencies 
' of the helloWorld component

!include helloworld.puml
!include displayText.puml

helloworld-->displayText : uses
@enduml
```

## Rule: Atomic model element desciptions shall not contain a title.
The rule says it all. You shall not define a (diagram) title in an atomic model 
element description.

### *Rationale*
The model element will be included in diagrams. Therefore, if the atomic
element descriptions would contain a title, the included elements would 
override the diagram title, and the last element included/put on a diagram
would win and define the title of the diagram. As we want to re-use the
elements on different diagrams and the diagram title to be defined by the 
diagram itself, the atomic model element descriptions need to be free of 
a title definition.


## Rule: Mark your model repository
The files that form your re-usable model repository shall be explicitly
marked with the following first line in the puml file:
```
'PUMLAMR
```
This PlantUML comment line exposes the following PlantUML description as
a re-usable asset of the model repository.

### *Rationale*
This explicit marking as a re-usable artefact is needed in order to be
able to separate your re-usable model from other PlantUML diagram files
in your repository. Developers might use other diagrams for e.g.
planning or discussion purposes that should not be part of the re-usable
model. `pumla` will only consider files that are marked like that for the
re-use. There may exist PlantUML diagrams within the repo, where you do 
not want the restrictions of `pumla`, and the other files would otherwise
possibly disturb the model-re-use. Still, you can include `pumla` files
into any other *non-pumla* PlantUML diagram file, as it only contains and
includes PlantUML compatible language.

## Rule: `pumla` files end with ".puml"
Each valid `pumla` file is a valid PlantUML file, and it shall end with ".puml".

### *Rationale*
This is used as simplification to scan and parse through the source code repo.
This restriction is not important for the concept or design, but just simplifies
parsing and scanning. Therefore, it might be removed later.

## Rule: Each `pumla` file should have the name of the alias of the model element.
Each `pumla` file should have the name of the alias of the model element it is describing.
If in a `pumla` file the model element has no alias, then it should have no whitespaces 
or special characters in it and therefore the name can and should be used as filename.

### *Rationale*
Same as previous rule, it simplifies the implementation of the parser and file
scanner and it makes sense as a naming convention anyway.

## Rule: No layout adaptations in atomic `pumla` files
`pumla` files for atomic model elements should not contain layout, coloring and skin definitions.

### *Rationale*
In order to be able to put different skins, layouts and coloring to the elements later, these kinds of things
should not be included in the atomic model element definitions.

## Rule: Do not use the shortcut definition for components, e.g. `[comp]` in pumla files.
The shortcut for the definition of a component like e.g. `[comp]` shall not be used
in pumla files, e.g. for the definition of internal elements. Use the explicit
definition like `component comp` instead.

### *Rationale*
It doesn't work. Somehow the shortcut is handled differently by PlantUML and leads to 
not understandable errors in some PlantUML diagrams. As the pumla files contain elements
that shall be re-used in different contexts, the shortcut definition might work in your
current examples and the asset definition itself, but might cause trouble in
future re-use scenarios or diagrams that will be created later. 

## Rule: Do not use implicit PlantUML type definitions for re-usable model element definitions
Instead, explicitly specify the type of the element by writing it down.

### *Rationale*
PlantUML allows a lot of shortcuts for creating elements, where the type is implictly derived based on assumptions.
Example:
```PlantUML

@startuml
hello ..> huhu
@enduml
```
In this example both "hello" and "huhu" become classes. If you change the arrow to "-->" they become objects in 
a sequence diagram. If you add a ">" directly after the "huhu" like "huhu>", you end up with an activity diagram
with "hello" and "huhu" being activities. 

This is fine in order to be able to quickly sketch a diagram with minimum number of characters typed. But it is 
really hard to process and parse. 

Therefore, it is necessary to exlicitly specify the type for elements that you describe as
pumla re-usable elements. Example:

```PlantUML

@startuml
class hello
class huhu
hello ..> huhu
@enduml
```
Then you can also exchange the names or the arrows without the diagram changing its character
and without having the elements "huhu" and "hello" switch their type. Instead you might get 
a PlantUML error, because mixing elemts like activities and classes might not be allowed.
And for pumla it is much easier to parse this element definition. So in order not to 
rewrite the complete PlantUML parser, this is a mandatory rule for pumla files. For 
re-usable element definitions, the "save every character"-use-case might also not be so 
relevant, because in that use-case I guess you prefer clarity and explicity.

