# `pumla` Modelling Guideline

*Rationale:*

Why do we need a modelling guideline giving us rules to follow?


In order to make re-use of single-source PlantUML models, it is necessary to
follow some modelling rules in order to be easily able to create a tool that
enables the re-use. So these rules and guidelines help us to keep the re-use
tooling `pumla` simple in its implementation. Without these rules, a lot 
more effort would need to go into the tooling to allow the same 
functionality.

## Some Principles
### Static vs. Dynamic 
Modelling elements first the static aspect with the atomic 
definitions.

Instances in separate files, that may contain more than one
instance definition for convenience, also that brings with it
some drawbacks: when putting an instance from a file with more
instances defined in it onto a diagram, then all the instances
appear on the diagram. You have to remove the unwanted instances
then by hand (via PlantUML "remove" command).

Dynamic aspects tbd

### Relations vs. Connections
Connections are typed dataflows. Therefore, a connection is only valid
between two interfaces. 

Relations are between two elements. also a general information flow can be a
relation, but as relation it is not concretely defined with what information
flows in detail as specified by an interface.

### Diagrams
tbd.

### Scaling the model repository
A model repository is basically a file containing re-usable element, connection 
and relation information in JSON format readable by PlantUML. For big source 
code repositories that also contain a lot of re-usable element information, 
it might be inconvenient to have all that information in one (big) file. In that 
case, a distribution into sub-spaces of the architecture and therefore 
sub-model-repositories might make sense.

This is supported by pumla with the TBD mechanism.


## Rule: `pumla` files are valid PlantUML files 
We only use PlantUML language in the `pumla` architecture descriptions.

###*Rationale*
That way, we can re-use the `pumla` model elements in each and every PlantUML diagram.

## Rule: Atomicity of Model Element descriptions
In the model files where the re-usable elements are modelled, do 
model only one element, do not model further other model elements
or dependencies to other elements. Therefore, do not include other
model files from here. You should have one file per model element.

###*Rationale*
When we want to re-use a model element in a diagram, we need to include
it's *.puml file into our diagram puml file. If another file is included 
by the model element file of the element we want to have on our
diagram, then automatically also the other (dependent) model element of 
the included puml file gets onto our diagram (which we may not want).
So, in order to be able to re-use elements on element level, these files
describing/modelling the elements should be atomic, meaning no other files
are included. Dependencies of this element to other elements are to be
modelled in a separate file, therefore.

###*Example*

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
## Rule: Mark your model repository
The files that form your re-usable model repository shall be explicitly
marked with the following first line in the puml file:
```
'PUMLAMR
```
This PlantUML comment line exposes the following PlantUML description as
a re-usable asset of the model repository.

###*Rationale*
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

###*Rationale*
This is used as simplification to scan and parse through the source code repo.
This restriction is not important for the concept or design, but just simplifies
parsing and scanning. Therefore, it might be removed later.

## Rule: Each `pumla` file should have the name of the alias of the model element.
Each `pumla` file should have the name of the alias of the model element it is describing.
If in an `pumla` file the model element has no alias, then it should have no whitespaces 
or special characters in it and therefore the name can and should be used as filename.

###*Rationale*
Same as previous rule, it simplifies the implementation of the parser and file
scanner and it makes sense as a naming convention anyway.

## Rule: No layout adoptions in atomic `pumla` files
`pumla` files for atomic model elements should not contain layout, coloring and skin definitions.
###*Rationale*
In order to be able to put different skins, layouts and coloring to the elements later, these kinds of things
should not be included in the atomic model element definitions.
