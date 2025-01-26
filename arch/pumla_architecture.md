# `pumla` Architecture

## Design Principles

- **Keep `pumla` as an extension of PlantUML, do not invent 
  a separate language and generate PlantUML code.**
  - **Rationale:** When inventing a separate language and 
    then processing it to generate PlantUML code, then
    in order to make use of each PlantUML feature it would
    need to be added to the separate language first. Without
    a separate language, but with using PlantUML and only its
    preprocessor, automatically all features of PlantUML can be
    used, no extra effort needed. `pumla` just adds some
    additional capabilities.
  - **Implementation:** Still, just the preprocessor without any
    other extension was not sufficient for the re-use Use Case,
    therefore, an additional python command line tool was needed,
    but it does not introduce a new language but just gathers 
    necessary (but still PlantUML conforming coded) information
    in another PlantUML-conforming and readable representation
    (global variables in JSON format).
- **Keep the scope of `pumla` to the "re-use" aspect, do not try
  to extend it for other use cases.**
  - **Rationale:** Typically, if you try to make a tool to serve
    a lot of different and more and more purposes, it gets worse 
    and worse. I try to stick here to the "re-use" use case. Other
    use cases can then be added by using/including other projects.

  - **Implementation:** E.g. a feature-tree-based variant handling
    mechanism will not be included in `pumla`. Of course it is 
    somehow related to "re-use", but not really the systematic re-use
    of PlantUML description, but it is a very general "re-use"
    problem. So if I will address that problem, I will setup a separate
    project for that.
  
## Context
Re-use of model elements that are described using PlantUML.

See the following image to get an idea of the big picture:

![](./01_context/pumla_context.png)

## Command line tool `pumla.py`

### Cheat Sheets

![](./00_pics/overview_allcheatsheets.png)

### All Elements

![](./00_pics/overview_allelements.png)

### Internal Static Structure 

![](./00_pics/overview_structure_hierarchy.png)

![](./00_pics/overview_internalstructure.png)

## `pumla` Requirements as Code approach
In systems engineering, architecture typically is highly connected to requirements engineering. The requirements
are the base to tell you what is expected from the system. Tests are written against requirements (or are a means
to describe a requirement). The traceability from architecture elements to requirements is crucial for knowing which
part of the implementation is intended to do what and why at all. When product variants come into play, the
start point of the variance is typically already on the requirements. So, not every product variant needs to have
each requirement fulfilled.

Therefore, bringing requirements engineering and architecture together into one docs-as-code/models-as-code approach
has the potential to ease the implementation of traceability and therefore simplify systems engineering in software intense
systems.

### Design Principles & Ideas
- [ ] requirements as YAML text: YAML better editable and readable for req. documentation as text than JSON
  - transform internally to JSON to be able to use contents with PlantUML Preprocessing
- [ ] traceability: in docs only one-directional trace from the lower requirement to the higher requirement (where it has been derived from)
- [ ] generate bi-directional traceability in „pumla update“ step. create a reqrepo_json.puml file with all collected req from whole project
    - [ ] have for each req „derived to“ and „derived from“ as keys. „derived to“ is created during the update step
    - [ ] „derived from“ is documented as key in the YAML files
- [ ] traceability to architecture artifacts. which arch element realizes a certain requirement.
    - [ ] realizes is a part of the architecture model, not of the requirement.
    - [ ] requirements are independent of their implementation
    - [ ] a requirement belongs to a scope; within the scope it gets broken down
- [ ] requirements can be structured in features.
    - [ ] req that belong to a feature can have a loose or high coupling
    - [ ] loose coupling will be realized with the „child injection“ mechanism
    - [ ] high coupling by a feature table that directly names reqs that belong to the feature
    - [ ] feature structure is kind of an architectural step with a composite breakdown view
- [ ] automatic scope alignment if the req doc is next a single RUA arch spec? or manual scope connection? do we need the scope at all?
- [ ] PUMLA macros to create diagrams that show all requirements fulfilled by a certain architecture element
- [ ] PUMLA macros to create feature structure & breakdown views
- [ ] PUMLA macros to create traceability views
- [ ] status „aligned“, „new“, „decided“
    - [ ] whether it is „realized/implemented“ will be decided with the respective test passing
    - [ ] „rejected“ can be a commit message for deleting the req
    - [ ] new: indicated a new unreviewed requirement which is there but not yet considered somewhere
    - [ ] aligned: requirement is reviewed and aligned to be usable, but not yet decided how to be realized
    - [ ] decided: there is a design decision done on to where and how the requirement shall be realized.
  
