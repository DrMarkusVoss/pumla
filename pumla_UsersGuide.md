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
Called without any other argument, pumla writes out to the console the help
information for the usage of `pumla` that you would also get with
`pumla --help`.

### `pumla -h` or `pumla --help`
Prints out a help text with information on the correct usage of `pumla` to 
the command line.

### `pumla -v` or `pumla --version`
Prints out version information of `pumla` to 
the command line.

### `pumla init`
Initialises a source code repository where the search for pumla model files
shall start. At the location where it is called also the file `pumla_macros.puml`
is generated. You include this file in order to get the macros to access your
model repository. It is an "include-forward" to the relevant files containing
the macros of your pumla installation. 

When you use a version control system like e.g. git, you do not check in the 
`pumla_macros.puml` file, as its content is dependent on the specific deployment
of the pumla package in your file system (where you installed pumla). So, first
thing after you checkout a source code repository that also contains pumla-modelled
elements, you call `pumla init` in the root folder of that repository (if not
another folder is defined by the source code projects documentation).

### `pumla setup`
This command needs to be called right after installation of pumla with:

"`pip install .`" or "`pip install -e .`"

The command must be executed from the root folder of the pumla release archive or
pumla git repository. It makes sure, that the installation of the pumla python CLI
tool knows where the pumla folder with the macros is, as it needs to access for
certain commands, like e.g. `pumla init`. Also, a version consistency check is 
performed. 

The installation procedure should be followed as described on the README.md.

### `pumla checksetup`
Checks the pumla setup. Evaluates the consistency of the version numbers of the 
pumla python CLI tool and the macros, as well as the right setup of the paths.

### `pumla setupprj`
This command prepares your projects source code repository to use pumla architecture
models. It is a convenience command, as it creates some files for you as starting point,
that you would need to setup otherwise manually.

Currently, the following things will be done:
- an empty `pumla_blacklist.txt` file is created, where you can enter folders and files
  that shall be ignored during the `pumla update` scan. E.g. if you have examples folders
  you may want to exclude them from your official projects architecture documentation.
- a pumla config file `pumla_project_config.puml` that allows to have a project-specific
  override of default values for pumla global variables. E.g. here you can decide that you
  want to have "Error Notes" turned off for your whole project as default (of course you
  can override it again in a diagram in your project).
- the init step is executed. See above `pumla init` description to see what happens there.

### `pumla update`
This is the most important command. It scans the source code repository starting
at the current folder location and traverses from here through all underlying
folders for all `.puml` files. If you want to exclude certain folders from the search,
you can name these in a `pumla_blacklist.txt` file. You can also have comments in the
blacklist file using `#` as first character of the line. But comments must be
standalone lines, you cannot put a comment behind a path or filename. 
The .puml files found will be parsed
and if they are pumla architecture files, their relevant content will be extracted and stored in the 
`modelrepo_json.puml` file or the given
filename. For docs-as-code requirements files, the relevant content will be extracted and stored in the
`reqsrepo_json.puml` file.
Each call will overwrite the existing `modelrepo_json.puml` and `reqsrepo_json.puml`
file, therefore they should not be modified by hand,
because changes will get lost. These repository files are the basis for the
PlantUML extension macros. The macros help to get data out of these repositories
and thereby re-use the once defined model elements and diagrams in a structured 
way.

The generated `modelrepo_json.puml` as well as the `reqsrepo_json.puml`
should also not be checked-in into a version
control system, as it contains absolute paths that are different on every computer
where the source code is checked out. Therefore, after a fresh checkout/clone of 
a source code repository, first thing to do is call `pumla init` to create a link
to the pumla macros to access the model repository JSON database, the second
thing to do is call `pumla update` to scan the source code repository for pumla
files and create the `modelrepo_json.puml` and `reqsrepo_json.puml` file.
After that you can use the
model repository to create diagrams and are able to use all the macro commands 
explained in the following chapters.

### `pumla installplantuml`
Downloads a compatible version of the PlantUML JAR file and places it into
a dedicated folder within the pumla command line tool installation.

### `pumla gendiagram <filename_with_path> <picture_format>`
Generates a picture from the filename that is a PlantUML or pumla source file.
For the picture formats you can choose from the following website(just type the format,
without "-t" or "-"), chapter "Types of Output File":

[https://plantuml.com/de/command-line](https://plantuml.com/de/command-line)

Hint: If you encounter problems during the generation of the picture, you can activate
the "verbose" logging feature of PlantUML. Instead of a picture format give "v" as
a parameter. It will then try to generate a .png file but the logging information
is put to the command line output.

### `pumla files`
Called without any other argument, pumla writes out to the console a
list of all `.puml` files that are `pumla` files (marked with either `'PUMLAMR`
(PUMLA-ModelRepo) or `'PUMLADR` (PUMLA-DiagramRepo) in the first line of the file).
Requirements are described in YAML files (`.yaml`) and will therefore not
be shown by this command, as they are not standalone PlantUML-compliant files.

### `pumla elements`
Writes out to the console all `pumla` model elements and diagrams of 
the model repository and diagram repository, with all their relevant 
attributes. This does not include requirements, for that we have the
call described next.

### `pumla reqs` - not yet implemented
Writes out to the console all `pumla` requirements elements and diagrams of 
the model repository and diagram repository, with all their relevant 
attributes. 

### `pumla getjson <subcommand>`
Prints out a JSON data structure containing the request elements (by subcommand).
There is no other output to the command line than the JSON data structure, so you can 
use this command to integrate pumla with other tools via a JSON data interface. As
the output to the command line shall be in-sync with the pumla model repository .puml
file, a `pumla update` is done implicitly also.

The following subcommands are supported:
- `pumla getjson elements`: Get a list in JSON format with all elements of the pumla
  model repository.
- `pumla getjson relations`: Get a list in JSON format with all relations of the pumla
  model repository.
- `pumla getjson connections`: Get a list in JSON format with all connections of the pumla
  model repository.

### `pumla checkalias <alias_name_to_check>`
First executes an update, then checks if the given `<alias_name_to_check>` is already existing/in use as alias
or id in the  current model repository. If not, it can be used as an alias for a new model element, relation
or connection.

---

## PlantUML Extension
The following special comments (file markings), macros and global variables are made as extension to PlantUML. 

## File Markings

### `'PUMLAMR`
This comment put into the first line of a `.puml` file marks the file
as `pumla` model element description that shall be part of the re-usable
model repository.

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

### `'PUMLARR`
This comment put into the first line of a `.yaml` file marks the file
as `pumla` requirement element description that shall be part of the re-usable
requirements repository.

---

## Extension Macros
The following macros (that are PlantUML unquoted functions and procedures) can be
used within each PlantUML file by including `pumla_macros.puml`. They are the
user "API" of `pumla`.

## Creating Re-usable Model Elements 

### `PUMLAReUsableAsset($name : string, $alias : string, $type : string, $stereotypes : string (optinal)) {...}`
Creates a re-usable asset (RUA). The asset can be of any PlantUML type, like class, component, node, rectangle, ...
You can only define one re-usable asset within a file.

For classes there are also specialized macros to make use of the special differences between classes and the
other types. 

### `PUMLAReUsableClass($name_alias : string, $stereotypes : string (optional)) {...}`
Create a re-usable class asset. One special thing here is that name and alias are the same.
This means you can only use characters for the name that also work for the alias (no whitespace, no special characters).
You do not need to specify the type as parameter, just the name which acts also as alias and stereotypes if needed.

### `PUMLAFullyInstantiableClass($classname : string, $stereotypes : string (optional)) {...}`
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

This needs not to be called at the end of a file where re-usable relations or connections have
been specified. 

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

### `PUMLARelation(startalias : string, "reltype" : string, endalias : string, "reltxt" : string, "relid" : string)`
Creates a re-usable relation between the two elements starting at element with alias
`startalias` and end at element with alias `endalias`. The type of relation can be any PlantUML
compatible relation like `"--", "-->", "..>", "<..>", ...`. `reltxt` is a description of the relation that
will be put next to the relation when put on a diagram. `relid` can be used as
unique identifier to reference to the relation. This relation is created only in the model repo and will be
filled with a text drawing the relation when put onto a diagram with `PUMLAPutRelation(...)` (or PutAll...). 

### `PUMLAConnection(startalias : string, "contype" : string, endalias : string, "contxt" : string, "conid" : string)`
Creates a connection between the two interfaces starting at interface with alias
`startalias` and end at interface with alias `endalias`. The type of connection can be any PlantUML
compatible relation or connection like `"--", "-->", "..>", "<..>", ...`. `contxt` is a description of the connection that
will be put next to the relation when put on a diagram. `conid` can be used as
unique identifier to reference to the connection. This connection is created only in the model repo and will be
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

### `PUMLACheatSheetTaggedValues()`
This macro creates a note with a table that shows the contents of the model
repository, the names and aliases of all model elements along with the tagged
values. That way you easily can see which model elements you can re-use and
what their alias and their attached tagged values are to access them. 

### `PUMLARelCheatSheetAllAttributes()`
This macro creates a note with a table that shows the contents of the relations
of the model repository. It puts all relations with all attributes into a table to help
you manage your architecture relations and artefacts.

### `PUMLARelCheatSheetTaggedValues()`
Similar to previous, but instead of information about file path and file name you
get the list of tagged values that are attached to each of the relations.

### `PUMLAConCheatSheetAllAttributes()`
This macro creates a note with a table that shows the contents of the connections
of the model repository. It puts all relations with all attributes into a table to help
you manage your architecture relations and artefacts.

### `PUMLAConCheatSheetTaggedValues()`
Similar to previous, but instead of information about file path and file name you
get the list of tagged values that are attached to each of the connections.

## Putting Re-usable Model Elements onto Diagrams

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

### `PUMLAInjectChildElements( alias : string )`
This macro puts all elements into this place, that call the given `alias` their parent (via the file markings mechanism
`'PUMLAPARENT: <elem_alias>`). Typically this is called
from within the definition of a re-usable element, where you want to inject elements that are defined somewhere else
and that you do not want to name explicitly here. That way, you can define in some other place the "child elements", 
and with this macro they are injected into the body of the parent (who calls this macro). This is a mechanism to allow
kind of a "responsibility/ownership" thing, to prevent that at some point in the git repo someone extends the model
of another owner with some internals just by naming "system" the parent.  So the "system" owner (as parent) has to
explicitly allow the children to come in, so the "PUMLAInjectChildElements(...)" is the kind of door-opener for that.

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


### `PUMLARUAPutTaggedValues( )`
Puts the tagged value table enclosed by a rectangle in place.

### `PUMLAPutTaggedValuesAsNoteToElement( elalias : string )`
Puts the tagged value table as a separate note to the outside of the element.
Especially helpful for classes, where the tagged value table cannot be 
shown inside the class element "box".

### `PUMLAPutTaggedValuesAsNoteToPort( elalias : string )`
Puts the tagged value table as a separate note to the outside of the port,
as the table cannot be shown within the port element (and would not
make sense). This is the only way to show the tagged value table
of a port.

### `PUMLAPutReqsBreakdownTraceFor($alias)`
Puts the requirement with the given alias onto the diagram and follows
its "derived" breakdown and puts further requirements onto the diagram
that the alias requirement is derived to. It connects the requirements
with a "realization" relation.

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
Filter-out all elements of the given stereotype on the following macro
calls that put elements on the diagram.

### `PUMLASetElementFilterInStereotype($stereotype : string)`
Filter-in all elements of the given stereotype on the following macro
calls that put elements on the diagram. All elements of other
stereotype are filtered out.

### `PUMLASetElementFilterOutTag($tag : string)`
Filter-out all elements that have the given tag (not caring about its
value) on the following macro calls that put elements on the diagram.

### `PUMLASetElementFilterInTag($tag : string)`
Filter-in all elements that have the given tag (not caring about its
value) on the following macro calls that put elements on the diagram.
All elements without the given tag will be filtered out.

### `PUMLASetElementFilterOutTagValue($tag : string, $value : string)`
Filter-out all elements that have the given tag/value combination
on the following macro calls that put elements on the diagram.


### `PUMLASetElementFilterInTagValue($tag : string, $value : string)`
Filter-in all elements that have the given tag/value combination
on the following macro calls that put elements on the diagram.
All elements without the given tag/value combination will be filtered out.

### `PUMLAResetFilters()`
Reset all filter values to default, which is "" or %false().

### `PUMLARUAHideInternalsOfElement( $alias : string )`
Allows to filter out/not show the internals of a re-usable asset element given with `$alias`, even if the 
global variable `$PUMVarShowBodyInternals` is true. With this macro, the given alias is added to the list of elements
of which not to show the internals. In order to show internals for that element within the scope of the same diagram
again, the "filter list" has to be resetted with the next macro.

## Creating Re-usable Requirements Elements 

### Creating a single re-usable docs-as-code requirement
Requirements are stored in YAML files (`.yaml`) with a file marking `#PUMLARR`in the first line.
Then, within the file, one or more requirements can be described. The requirements are elements
of a YAML list with at least the following attributes:
- alias: the unique short-ID 
- type: describing the kind of requirement. Can be set according to needs. Could be "Requirement", "Constraint", ...
- status: also here, the status model is not defined by PUMLA; put status values as you need and like.
- derived_from: the alias of the (parent) requirement where this requirement is derived from.
- content: The text content of the requirement itself.

The following attributes are optional:
- taggedvalues: a list of tag/values pairs, where values is list by itself.

Requirement files can be distributed across the folders in a git repository and therefore be
stored close to the code if wanted. The `pumla update`
command will find each of them, considering the blacklist.

Example:
```
File: req.yaml

#PUMLARR
- type: Requirement
  alias: REQ_WS1
  status: decided
  derived_from:
  taggedvalues:
    - tag: "Vendor"
      values:
      - A Inc.
      - C Ltd.
    - tag: "Variant"
      values: [SysA, SysB]
  content:
    This is a requirement towards my Weather Station. The Weather Station shall
    be able to measure the temperature.

- type: Requirement
  alias: REQ_WS2
  status: new
  derived_from:
  content:
    This is another requirement. The Weather Station housing shall be blue.
```

## Overview on the Requirements Repository of Re-usable Elements
### `PUMLAPutAllReqsTable()`
This macro puts all requirements of the `reqsrepo_json.puml` into a table on the diagram,
with a count of the requirements as well as the files where the requirements are stored in. It
is similar to the `CheatSheets` of the architecture model elements.

### `PUMLAPutReqByCount($count)`
This macro is solely meant for overview purposes, allowing you to quickly step through each
single requirement in the requirements repository by addressing it by its number (`$count`). 

Hint: The `$count` shall not be used to address a requirement a certain requirement or put
it onto a real diagram with a real purpose. The numbering in the requirements repository can 
change by calling `pumla update`, so that the `$count` may point to another requirement. 
In real diagram, requirements shall always be addressed by their unique short-ID, the `alias`.

## Putting Re-usable Requirements Elements onto Diagrams
### `PUMLAPutReq($alias)`
Puts the requirement with the given alias in form of a PlantUML JSON table with all its
attributes onto the diagram.

### `PUMLAPutAllReqs()`
Puts all the requirements of the requirements repository (`reqsrepo_json.puml`) onto the 
diagram.

### `PUMLAPutAllReqsWithStatusTable($value)`
Puts all requirements of the requirements repository, where the status has the given `$value`,
onto the diagram.

### `PUMLAPutAllReqsWithTypeTable($value)`
Puts all requirements of the requirements repository, where the type has the given `$value`,
onto the diagram.

### `PUMLAPutReqBrief($alias)`
Puts the requirement with the given alias onto the diagram, focussing on a limited amount of
attributes:
- type
- content
- status

### `PUMLAPutReqAsNote($alias)`
Puts the brief requirement with the given alias wrapped into a PlantUML note onto the diagram.

Hint: This macro can be useful to put the requirement onto diagrams along with classes, components or
dynamic behaviour descriptions.

### `PUMLAPutAllReqsBrief()`
Puts all the requirements of the requirements repository (`reqsrepo_json.puml`) onto the 
diagram, but only with the brief set of attributes (see `PUMLAPutReqBrief($alias)`).

## Working with Requirements Traceability
### `PUMLAPutReqsBreakdownTraceFor($alias)`
Puts the trace for a requirement with given alias down on the diagram. Each requirement along the
trace is put with its brief description. The trace is modelled with a "realizes" relation, so pointing
from a derived requirement to a parent requirement where it was derived from.

## Working around some PlantUML limitations

### `PUMLASetAsComponentDiagram()`
Workaround some "flexible behaviour" of PlantUML. You can call this
at the beginning of a diagram in order to state it clearly as component
diagram. Therefore, when putting classes on the diagram you will get
PlantUML errors (unless you use "allowmixing", which brings along other
downsides). This prevents PlantUML from automatically deciding upon the
first element which kind of diagram you have.

### `PUMLASetAsClassDiagram()`
Same as above, but makes the diagram a class diagram.


## C4 Model 
In order to enable the access to the C4 model **pumla** macros, you have 
to set the respective global variable to "true" in your project specific 
config file, like this:

```
!$PUMUseC4Model = %true()
```

This is needed to automatically include the necessary C4 preprocessor
files of the [C4 PlantUML extension](https://github.com/plantuml-stdlib/C4-PlantUML).
But that also comes with a drawback, as it automatically switches the
alignment in notes etc. to a "centered alignment". Therefore, **pumla**
makes it "switchable", so that you can turn on the C4 extension if you
want and need it.

When switched on, you can use all the macros of the C4-PlantUML extension, but they
are meant just for coding diagrams, not models. In order to make the C4 model elements
re-usable, you need to use the special **pumla** C4 macros described in the 
following sections. You can also mix them.

### Elements
The following C4 elements can be created in a re-usable way:
- ContainerContainerDb
- ContainerQueue
- Container_Ext
- ContainerDb_Ext
- ContainerQueue_Ext
- Container_Boundary
- Component
- ComponentDb
- ComponentQueue
- Component_Ext
- ComponentDb_Ext
- ComponentQueue_Ext
- Deployment_Node
- Deployment_Node_L
- Deployment_Node_R
- Node
- Node_L
- Node_R
- Person
- Person_Ext
- System
- System_Ext
- System_Boundary
- SystemDb
- SystemQueue
- SystemDb_Ext
- SystemQueue_Ext
- Enterprise_Boundary

The corresponding `pumla` elements just have a `PUMLAC4` as prefix. Furthermore,
almost all of these have the same syntax and sematics in their macro calls.
Therefore, it is explained just on a few examples:

### `PUMLAC4Container($alias, "$label", "$techn"="", "$descr"="", $sprite="", $tags="", $link="")`
Elements like "Container", "Component", etc. all have a syntax like this. The `$alias` is for
referencing the element, same as with all other **pumla** macros.
`$label` is the same as the name of the other **pumla** elements. It may contain 
whitespaces and special characters, but should be put in "". With C4-PlantUML, the description
is not done as a separate note, but put into the element itself. It is given not separately, but
at element construction time with the `$descr` argument. The `$techn` string argument is meant to
be a label for the technology used (e.g. "HTTPS").

### `PUMLAC4System_Boundary($alias, $label, $tags="", $link="")`
The "*_Boundary" elements have less arguments, like this macro here.

### Relations
The following C4 relations are supported:
- `Rel`, `Rel_U`, `Rel_D`, `Rel_R`, `Rel_L`, `Rel_Back`, `Rel_Neighbor`, `Rel_Back_Neighbor`
- `BiRel`, `BiRel_U`, `BiRel_D`, `BiRel_R`, `BiRel_L`, `BiRel_Neighbor`

Again, to create a re-usable version of the C4 relations you have to add
the prefix `PUMLAC4` before the respective relation name. They have all
the same syntax and semantics, like in this example:

### `PUMLAC4Rel($alias, $from, $to, "$label", "$techn"="", "$descr"="", $sprite="", $tags="", $link="")`
Like the standard relations and connections from **pumla**, also the re-usable C4 relations get
an `$alias` to reference them in order to re-use them. `$from` and `$to` are the aliases of the
source and target element for the relation. `$label` is for a short descriptive text (e.g. "uses"),
`$techn` is meant to describe the technology used (with a string) and `$descr` is meant to be a longer
description text.

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

### `modelrepo_json.puml`
Include this file wherever you access the model repository
with the `pumla` Extension Macros.



