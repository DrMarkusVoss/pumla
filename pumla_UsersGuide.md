# `pumla` User's Guide
This guide shall explain how to use `pumla`. As it is an extension to PlantUML,
it is assumed that PlantUML is known well enough. If not, please refer to the 
online available documentation on PlantUML.

## The `pumla` Concept
- Re-use by describing single atomic model elements in PlantUML file/diagram.
- Introduction of special Global Variables to control what parts of a model element are
  shown on a diagram.
- Modelling guideline to enable re-use and simplify scanning and parsing.
- Scanning and parsing of `pumla` files, storing the contents in a JSON-based
  model repository, that can be accessed from within PlantUML.
- PlantUML macros (unquoted functions and procedures) used to access the data
  from the JSON model repository.
- Templates showing the usage of the Global Variables and Extension Macros to
  describe a re-usable model element according to `pumla`.
- A python-based command line tool that parses and scans the `.puml` files in the
  source tree and puts the relevant content into the model repository JSON files.
  The tool also offers  convenience commands to easily search the model repository.

## `pumla` Command Line Tool
The following commands are offered:

### `pumla`
Called without any other argument, pumla writes out to the console a
list of all `.puml` files that are `pumla` files (marked with either `'PUMLAMR`
(PUMLA-ModelRepo) or `'PUMLADR` (PUMLA-DiagramRepo) in the first line of the file).

### `pumla listelements`
Writes out to the console all `pumla` model elements and diagrams of 
the model repository and diagram repository, with all their relevant 
attributes.

### `pumla update <filename optional>`
This is the most important command. It scans the source code repository starting
at the current folder location and traverses from here through all underlying
folders for all `.puml` files. The .puml files will be parsed and if they are 
pumla files, their relevant content will be extracted and stored in the 
`modelrepo_json.puml` (and tbd: `diagramrepo_json.puml`) file or the the given
filename. Each call will overwrite the existing `{modelrepo | diagramrepo}_json.puml`
files, therefore they should not be modified by hand,
because changes will get lost. These repository files are the basis for the
PlantUML extension macros. The macros help to get data out of these repositories
and thereby re-use the once defined model elements and diagrams in a structured 
way.

---

## PlantUML Extension
The following special comments (file markings), macros and global variables are made as extension to PlantUML. 

### File Markings

### `'PUMLAMR`
This comment put into the first line of a `.puml` file marks the file
as `pumla` model element description that shall be part of the re-usable
model repository.

### `'PUMLADR`
This comment put into the first line of a .puml file marks the file
as pumla diagram element description that shall be part of the re-usable
diagram repository.

### `'PUMLAPARENT: <elem_alias>`
This comment in the second line under the `'PUMLAMR` marks that
the model element described in this file is a child of the element 
referenced to by its alias `elem_alias`. So, when the parent element
is put onto a diagram and the internals are configured to be shown, 
then this element will appear inside the parent element.

---

### Extension Macros
These macros (that are PlantUML unquoted functions and procedures) can be
used within each PlantUML file by including `pumla_macros.puml`.

### `PUMLACheatSheet()`
This macro creates a note with a table that shows the contents of the model
repository, the names and aliases of all model elements. That way you easily
can see which model elements you can re-use and what their alias to access it
is.

### `PUMLACheatSheetAllAttributes()`
This macro creates a note with a table that shows the contents of the model
repository. It puts all elements with all attributes into a table to help
you manage your architecture artefacts.

### `PUMLAPutElement( elem_alias )`
This macro puts the model element with the given alias `elem_alias` onto the diagram.
The referenced element must exist somewhere in the source tree as a model element
described in a `pumla` model repository file.

### `PUMLAPutElement( elem_alias, lod )`
Same as above, but limits the displaying of nested elements to the level number 
defined by `lod` (level of detail). This overrides the global variable
`$PUMVarShowBodyInternals`. Even when that variable is set to false, only the 
referenced element will be shown with the defined levels of nested internals.

### `PUMLAPutAllElements()`
Puts all elements from the model repository on the diagram. Useful to get an
overview on all elements inside the source tree.

### `PUMLACreateInstanceOf( model_elem_alias : string, inst_name : string)`
Creates an instance of a model element with alias `model_elem_alias` that is
inside the model repository and names the instances `inst_name`. The instance
gets the same type as the model element from the repository but gets in
addition the stereotype `<<instance>>`. On diagrams that do not show
the `instance of` relation to the model element, the name of the instance will
be extended by `::<model element name>`.

### `AddTaggedValue( tag : string, value : string )`
Adds a tag/value pair to the tagged value table of the
next model element to be defined.

Requires including `pumla_tagged_values.puml`.


### `PUMLAPutTaggedValues()`
Puts the tagged value table enclosed by a rectangle in place.

Requires including `pumla_tagged_values.puml`.

### TODO
- Put macros that vary showing interface, description, internals
  and tagged values as option, overriding the globals
  
---

### Global Variables
These following global variables have an impact on the visualization 
of all pumla model elements that are put onto the diagram.

### `$PUMVarShowDescr : boolean` 
Defines whether the model elements descriptions are shown on
the diagram or not. 

### `$PUMVarShowInterfaces : boolean`
Defines whether the interfaces of the model elements are shown
on the diagram or not.

### `$PUMVarShowBody : boolean`
Defines whether the model elements body is shown on the diagram
or not. The body is the main model element. In most cases it 
does not make sense to hide the body, so this will be most
likely almost on every diagram true. But there may be some 
rare exceptions where you want it. ;-)

### `$PUMVarShowBodyInternals : boolean`
Defines whether the internals of the model elements are shown.
Internals can be elements directly modelled into the body or
elements belonging inside indirectly, by using the
`'PUMLAPARENT` marking.

### `$PUMVarShowTaggedValues : boolean`
Defines whether the tagged values table of the model element
are shown within the model elements body or not.

### `$PUMVarShowInstantiationRel : boolean`
Defines whether the `instance of` relation created by the 
macro `PUMLACreateInstanceOf(...)` is shown on the diagram 
or not. Furthermore it influences the shown name of the 
instance. When set to "false", the instance name is enhanced
by the model element that it is instantiated from.

### TODO
- global level of detail for internals

### Example
```PlantUML
file: ./test/examples/easyAllElementsOverview.puml

@startuml
!include modelrepo_json.puml
!include ./../../pumla_macros.puml
!include ./../../templates/sysml/skin.puml

!$PUMVarShowDescr = %true()
!$PUMVarShowInterfaces = %false()
!$PUMVarShowBody = %true()
!$PUMVarShowBodyInternals = %false()
!$PUMVarShowTaggedValues = %true()
!$PUMVarShowInstantiationRel = %true()

title Overview on all model elements in repository

'put all elements of json-modelrepo onto the diagram
PUMLAPutAllElements()

@enduml
```
---

### Files to be included

### `pumla_macros.puml`
Include this file in your PlantUML diagram files or 
`pumla` model element description files to use the
`pumla` extension macros.

### `pumla_tagged_values.puml`
Include this file to make use of the pumla tagged value
extension. This only needs to be included where the tagged
values are defined, not on every diagram where the
element containing the tagged values is placed.

### `modelrepo_json.puml`
Include this file wherever you access the model repository
with the `pumla` Extension Macros.

### `diagramrepo_json.puml`
Include this file wherever you access the diagram repository
with the `pumla` Extension Macros.

