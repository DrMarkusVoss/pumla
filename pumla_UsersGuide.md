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

### `pumla update`
This is the most important command. It scans the source code repository starting
at the current folder location and traverses from here through all underlying
folders for all `.puml` files. If you want to exclude certain folders from the search,
you can name these in a `pumla_blacklist.txt` file. The .puml files found will be parsed and if they are 
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

## File Markings

### `'PUMLAMR`
This comment put into the first line of a `.puml` file marks the file
as `pumla` model element description that shall be part of the re-usable
model repository.

### tbd: `'PUMLADR`
This comment put into the first line of a .puml file marks the file
as pumla diagram element description that shall be part of the re-usable
diagram repository.

### `'PUMLAPARENT: <elem_alias>`
This comment in the second line under the `'PUMLAMR` marks that
the model element described in this file is a child of the element 
referenced to by its alias `elem_alias`. So, when the parent element
is put onto a diagram and the internals are configured to be shown, 
then this element will appear inside the parent element.

### `'PUMLAINSTANCES`
This comment in the second line under the `'PUMLAMR` marks that this
file contains definitions of re-usable instances of re-usable elements.
Other than model elements, it is allowed to define multiple instances
in one file. That is why there is a dedicated marking for such a file.

### `'PUMLADYN`
This comment marks the file as a re-usable asset of a dynamic behaviour 
element description. In a file marked like that, only the dynamic aspect
should be modelled, by e.g. a sequence, state or activity diagram.

---

## Extension Macros
The following macros (that are PlantUML unquoted functions and procedures) can be
used within each PlantUML file by including `pumla_macros.puml`. They are the
user "API" of `pumla`.

## Creating Re-usable Elements 

### `PUMLAReUsableAsset($name : string, $alias : string, $type : string, $stereotypes : string (optinal)) {...}`
Creates a re-usable asset (RUA). The asset can be of any PlantUML type, like class, component, node, rectangle, ...
You can only define one re-usable asset within a file.

For classes there are also specialized macros to make use of the special differences between classes and the
other types. 

### `PUMLAReUsableClass($name_alias : string, $stereotypes : string (optional)) {...}`
Create a re-usable class asset. One special thing here is that name and alias are the same.
This means you can only use characters for the name that also work for the alias (no whitespace, no special characters).
You do not need to specify the type as parameter, just the name which acts also as alias and stereotypes if needed.

### `PUMLAFullyInstantiatableClass($classname : string, $stereotypes : string (optional)) {...}`
Create a special re-usable class asset. If you create a class with this macro, it allows its instances to inherit the
methods and attributes defined in this class.

### `PUMLARUADescr($alias_descr, $pos (optional))`
Links a description with the given alias to the re-usable asset. With `$pos` you can define the
position of the note in relation to the re-usable asset. It can be "u" for "up" (above the element), 
"l" for "left" (of the element), "r" for "right" (of the element) and "d" for "down" (below the
element). If $pos is not set, the default is "d".

### `PUMLARUAInternals() {...}`
Creates an "internals" section within the re-usable asset. The internals can be filtered out with the global variable
`$PUMVarShowBodyInternals` set to `%false()`. The internals must be defined
within the brackets `{ ... }`.

### `PUMLAReUsableAssetFinalize()`
Needs to be called at the end of a file with a re-usable asset description before `@enduml`. This cleans up internal
global variables and allows multiple re-usable assets to be used, even multiple 
instances of one re-usable asset.

### `PUMLAFullInstanceOf($classalias : string, $instalias : string)`
Creates an instance that inherits the internals (methods, attributes) of a class that has been
created with the `PUMLAFullyInstantiatableClass(...)` macro. If you try to apply this macro
to a $classalias which has been created in a different way, you will experience errors.


### `PUMLAInstanceOf( model_elem_alias : string, inst_alias : string, inst_name : string (optional))`
Creates a re-usable instance of a model element with alias `model_elem_alias` that is
inside the model repository and names the instances `inst_name` with the alias.
This is only allowed to be called within an instance definition file (marked with
`'PUMLAINSTANCES` in the second line of the file.

### `PUMLAInterface( "ifname": string, ifalias : string, elemalias : string, $type="":string)`
Creates an interface with name and alias that belongs to element referenced by
`elem_alias`. `type` is the kind of connection between the interface and
the model element and can be `in`, `out`, `inout` or empty which translates to
a non-directional connections ("--").

### `PUMLARUAInterface( "ifname": string, ifalias : string, $type="":string)`
Same as `PUMLAInterface(...)` but the element the interface is applied to is 
automatically the re-usable asset of the current definition (file), so its element
alias does not need to be explicitly mentioned. So it does only work if previously
in the same file the `PUMLAReUsableAsset/Class` has been called.

## Creating Re-usable Relations and Connections

### `PUMLARelation(startalias : string, endalias : string, "reltype" : string, "reltxt" : string (optional), "relid" : string (optional))`
Creates a re-usable relation between the two elements starting at element with alias
`startalias` and end at element with alias `endalias`. The type of relation can be any PlantUML
compatible relation like `"--", "-->", "..>", "<..>", ...`. `reltxt` is a description of the relation that
will be put next to the relation when put on a diagram. `relid` can be used as
unique identifier to reference to the relation. If not given, `pumla` automatically creates the
id by combining start and end alias. This relation is created only in the model repo and will be
filled with a text drawing the relation when put onto a diagram with `PUMLAPutRelation(...)` (or PutAll...). 

### `PUMLAConnection(startalias : string, endalias : string, "contype" : string, "contxt" : string (optional), "conid" : string (optional))`
Creates a connection between the two interfaces starting at interface with alias
`startalias` and end at interface with alias `endalias`. The type of connection can be any PlantUML
compatible relation or connection like `"--", "-->", "..>", "<..>", ...`. `contxt` is a description of the connection that
will be put next to the relation when put on a diagram. `conid` can be used as
unique identifier to reference to the connection. If not given, `pumla` automatically creates the
id by combining start and end alias. This connection is created only in the model repo and will be
filled with a text drawing the relation when put onto a diagram with `PUMLAPutConnection(...)` (or PutAll...). 

## Overview on the Model Repository of Re-usable Elements

The easiest way to get an overview on the contents of the model repository
is the usage of Cheat Sheets. With the following macros you can get
information about the contents of the model repository directly on a
diagram as a table within a note. If you do not need the information anymore,
you can just comment the macro out.


### `PUMLACheatSheet()`
This macro creates a note with a table that shows the contents of the model
repository, the names and aliases of all model elements. That way you easily
can see which model elements you can re-use and what their alias to access it
is.

### `PUMLACheatSheetAllAttributes()`
This macro creates a note with a table that shows the contents of the model
repository. It puts all elements with all attributes into a table to help
you manage your architecture elements and artefacts.

### `PUMLARelCheatSheetAllAttributes()`
This macro creates a note with a table that shows the contents of the relations
of the model repository. It puts all relations with all attributes into a table to help
you manage your architecture relations and artefacts.

### `PUMLAConCheatSheetAllAttributes()`
This macro creates a note with a table that shows the contents of the connections
of the model repository. It puts all relations with all attributes into a table to help
you manage your architecture relations and artefacts.


## Putting Re-usable Elements onto Diagrams

### `PUMLAPutElement( elem_alias )`
This macro puts the model element with the given alias `elem_alias` onto the diagram.
The referenced element must exist somewhere in the source tree as a model element
described in a `pumla` model repository file.

Both, static and dynamic elements, can be put onto a diagram with this macro. But be
aware, that with this macro you cannot mix the static and dynamic world. If you want
to put static and dynamic elements onto the same diagram, then use the 
`PUMLAPutDynamicElement( alias : string )` macro (see down below) to put the dynamic
elements onto the same diagram as you put the static elements with this macro
here.

### `PUMLAPutAllElements()`
Puts all elements from the model repository on the diagram. Useful to get an
overview on all elements inside the source tree. This macro automatically
overrides the `$PUMVarShowBodyInternals` with false, in order to allow the
mixing of class and component elements. At the end of the macro the value of 
`$PUMVarShowBodyInternals` is restored to the previous value.

This macro only puts static elements onto the diagram, as this is a typical 
use case. If you want an overview of really all elements, static and dynamic,
the cheat sheet is the right thing to use. When it comes to architectural 
documentations, you would always want to have separate overviews for static
and dynamic elements, and special diagrams where you show the collaboration of
static and dynamic world with the scope on specific or single elements only.

TBD: I am thinking whether it makes sense to mark the repository as "software" or
"system", so that you can put all "software elements" onto a diagram. Because class
elements can be embedded into packages etc. you could use the inject mechanism also
for that. 

### `PUMLAPutAllElementsMix()`
Puts all elements from the model repository on the diagram. Useful to get an
overview on all elements inside the source tree. This macro automatically
overrides the `$PUMVarShowBodyInternals` with false, in order to allow the
mixing of class and component elements. At the end of the macro the value of 
`$PUMVarShowBodyInternals` is restored to the previous value.

When the model repository is mixed with class and component elements, then this 
macro puts a note around the class elements. With PlantUML it is not possible to
mix classes onto a component diagram and vice versa. Therefore, in order to keep 
up the functionality of putting really all elements onto a diagram, the 
classes need to be wrapped in a note in order to be put onto the component diagram, 
that this macro call will create. A side-effect of this is, that you cannot 
reference the classes on that diagram by their alias or in any other way. So you
cannot attach additional notes or relations to them when put on a diagram
with this macro. If you want to work with classes, you should use the 
`PUMLAPutAllClasses()` macro, which will create a class diagram with only all 
class elements onto the diagram.

### `PUMLAPutAllClasses()`
Puts all class elements of the model repository onto the diagram. The diagram
will become a class diagram. So you cannot mix it with component elements. That
is a PlantUML limitation. You can partly work around it by adding the command
`allowmixing`, but this does still not allow to have elements like `[some component]`
on the diagram, so it leads to an error.

### `PUMLAPutAllElementsOfStereotype( st : string )`
Put all elements with stereotype `st` onto the diagram.

### `PUMLAPutAllElementsWithTagValue($tag : string, $value : string (optional))`
Put all elements with the given tag value combination onto the diagram. This command
is intended to be used on component and deployment diagrams, therefore classes elements
will be wrapped in notes, so that they can coexist with other element types
on the same diagram. The `value` argument is optional, so you can also use only tags
without giving the values argument a concrete value. This command will then see
that the tag argument is set, the value argument is treated as empty string by default.

### `PUMLAPutDynamicElement( alias : string )`
Put a dynamic element onto the diagram in a way that it can be mixed with static
diagram elements. PlantUML has a lot of pitfalls when it comes to mixing elements
of different diagram types. With `pumla` these macros help you to create the 
traceability between the dynamic and static world. 

This macro basically wraps the dynamic description details into a note, and 
creates a static element, a rectangle, representing the dynamic aspect. The
wrapping note is linked to the static rectangle element. That way
you have the bridge between static and dynamic world.

If you just need a diagram with dynamic aspects of the same kind, you can
also just use the standard `PUMLAPutElement(...)` to put also dynamic elements 
onto the diagram.

### `PUMLAPutInternalDynElement( alias : string )`
Same as previous macro, but wraps the call of the previous macro into a 
dependency on the boolean value of the global variable `$PUMVarShowBodyInternalsDyn`.

### `PUMLACreateAndPutInstanceOf( model_elem_alias : string, inst_alias : string, inst_name : string (optional))`
This macro is intented to be called outside of the model repository, meaning on diagrams
that use re-usable elements but a diagram that is not a re-usable element
itself. 

Creates an instance of a model element with alias `model_elem_alias` that is
inside the model repository and names the instances `inst_name` with the alias
`inst_alias`. Then this instance is put on the diagram.
The name can have whitespaces, it will be but in '"', for the alias
the same rules apply as to PlantUML alias. If no name is provided, then
the name will be the same as the alias. The instance
gets the same type and stereotype(s) as the model element from the repository but gets in
addition the stereotype `<<instance>>`. On diagrams that do not show
the `instance of` relation to the model element, the name of the instance will
be extended by `::<model element name>`. The `instance of` relation
will not appear in the model repository, as this method is
not intended to create a re-usable element but to create a 
non-re-usable instance of a re-usable element. So it is a convencience function
simplifying the instantiation process with at the same time creating
the proper relation between instance and class element.


## Putting Re-usable Relations and Connections onto Diagrams

### `PUMLAPutRelation("relid" : string)`
Puts the relation with the given ID onto the diagram. The ID must refer to a relation
in the model repository.

### `PUMLAPutRelationsForElement(elemalias : string, "reltype" : string (optional), "tag" : string (optional), "value" : string (optional))`
Puts all relations from the relations repository onto the diagram, that are associated
with the model element with the given `elemalias`, meaning it starts or ends at that element.
If also a relation type is given with `reltype`, then only the relations of that type
will be put onto the diagram.

When a tag is given, then only relations that additionally have the given tag will be put
on the diagram. If also a value is given, then also the value must be the same for the relation
to be put onto the diagram. Giving only a value without a tag will ignore the tag/value
filtering.

### `PUMLAPutAllRelations()`
Puts all relations from the model repository onto the diagram.

### `PUMLAPutAllStaticRelations()`
Puts only all these relations from the model repository onto the 
diagram, for which both, the start and the end element are static 
elements.

This is a convenience function for the case that you want to deal
only with static elements on your diagram, and want to put only 
those relations onto it.

### `PUMLAPutConnection("conid" : string)`
Puts the connection with the given ID onto the diagram. The ID must refer to a relation
in the model repository.

### `PUMLAPutConnectionsForElement(elemalias : string)`
Puts all connections from the model repository onto the diagram, that are associated
with the model element with the given `elemalias`, meaning it starts or ends with an interface
of that element. 

### `PUMLAPutAllConnections()`
Puts all connections from the model repository onto the diagram.


## Adding Tagged Values to Elements, Relations and Connections

### `PUMLAAddTaggedValue( alias : string, tag : string, value : string )`
Adds a tag/value pair to the tagged value table of the
 re-usable model element, relation or connection with
 the given alias.

### `PUMLARUAAddTaggedValue( tag : string, value : string )`
Adds a tag/value pair to the tagged value table of the
 re-usable model element defined in the same file.

### `PUMLAPutTaggedValues( elemalias : string)`
Puts the tagged value table enclosed by a rectangle in place.

Requires including `pumla_tagged_values.puml`.

### `PUMLARUAPutTaggedValues( )`
Puts the tagged value table enclosed by a rectangle in place.

Requires including `pumla_tagged_values.puml`.

## Diagram Filters

### `PUMLASetElementFilterOutType($type : string)`
With this command you can set a filter that is applied to all
"PutElement" macros that are following after this filter command.

This command filters out all data elements with the given type 
(see cheat sheet to find out which types the elements have). 
Therefore, elements of that type will not appear on the diagram.
Typically types are "node", "component", "rectangle", "class", 
"state", etc.

### `PUMLASetElementFilterInType($type : string)`
With this command you can set a filter that is applied to all
"PutElement" macros that are following after this filter command.

This command filters in all data elements with the given type 
(see cheat sheet to find out which types the elements have).
That means, all elements of the given type will appear on the diagram
when put there, for all other types the elements will not appear
even if they are explicitly put on the diagram.
Typically types are "node", "component", "rectangle", "class", 
"state", etc.

You can change the filters throughout the specification of the 
diagram. The filter only affects the following lines after this
macro, until this macro is called again with another type. If it
shall be deactivated for further lines, set type to the empty string,
"".

### `PUMLASetElementFilterOutStereotype($stereotype : string)`
tbd

### `PUMLASetElementFilterInStereotype($stereotype : string)`
tbd

### `PUMLASetElementFilterOutTag($tag : string)`
tbd

### `PUMLASetElementFilterInTag($tag : string)`
tbd

### `PUMLASetElementFilterOutTagValue($tag : string, $value : string)`
tbd

### `PUMLASetElementFilterInTagValue($tag : string, $value : string)`
tbd

### `PUMLAResetFilters()`
Reset all filter values to default, which is "" or %false().

## Working around some PlantUML limitations

### `PUMLASetAsComponentDiagram()`
tbd

### `PUMLASetAsClassDiagram()`
tbd

---

## Global Variables
These following global variables have an impact on the visualization 
of all pumla model elements that are put onto the diagram after the 
redefinition.

### `$PUMVarShowDescr : boolean` 
*Default*: `%true()`

Defines whether the model elements descriptions are shown on
the diagram or not. 

### `$PUMVarShowInterfaces : boolean`
*Default*: `%true()`

Defines whether the interfaces of the model elements are shown
on the diagram or not.

### `$PUMVarShowBody : boolean`
*Default*: `%true()`

Defines whether the model elements body is shown on the diagram
or not. The body is the main model element. In most cases it 
does not make sense to hide the body, so this will be most
likely almost on every diagram true. But there may be some 
rare exceptions where you want it. ;-)

### `$PUMVarShowBodyInternals : boolean`
*Default*: `%true()`

Defines whether the internals of the model element are shown.
Internals can be elements directly modelled into the body or
elements belonging inside indirectly, by using the
`'PUMLAPARENT` marking.

### `$PUMVarShowBodyInternalsDyn : boolean`
*Default*: `%true()`

Defines whether the dynamic internals of the model element are
shown. That way you can decide to show only dynamic internals 
or only static internals (previous global variable) or both.

### `$PUMVarShowTaggedValues : boolean`
*Default*: `%true()`

Defines whether the tagged values table of the model element
are shown within the model elements body or not.

### `$PUMVarShowInstantiationRel : boolean`
*Default*: `%true()`

Defines whether the `instance of` relation created by the 
macro `PUMLACreateInstanceOf(...)` is shown on the diagram 
or not. Furthermore it influences the shown name of the 
instance. When set to "false", the instance name is enhanced
by the model element that it is instantiated from.

### `$PUMVarShowConnections : boolean`
*Default*: `%true()`

### `$PUMTaggedValuesNoteToElementAlignment : string`
*Default*: `right`

### `$PUMVarShowPUMLAFooterNote : boolean`
*Default*: `%true()` (Configuration in `pumla_global_cfg.puml`)

Turn on (true) or off (false) the default
pumla advertising footer. Can also be
overwritten in each diagram with own
footer.

### `$PUMVarShowPUMLAErrorNotes : boolean`
*Default*: `%true()` (Configuration in `pumla_global_cfg.puml`)

Turn on (true) or off (false) the
Error Note generation. With error
notes you get information about a
failed pumla command in a red note
on the diagram.

### `$PUMColorTaggedValues : boolean`
*Default*: `lightgreen` (Configuration in `pumla_global_cfg.puml`)

Choose the color of the tagged values
table. Color names have to be written
in small letters.




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

## Files to be included

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

### tbd: `diagramrepo_json.puml`
Include this file wherever you access the diagram repository
with the `pumla` Extension Macros.

