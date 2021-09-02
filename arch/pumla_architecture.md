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
    necessary (but still PlantUML conformant coded) information
    in another PlantUML-conformant and readable representation
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

![](./01_context/pumla_context.png)

## Command line tool `pumla.py`

### Cheat Sheets

![](./00_pics/overview_allcheatsheets.png)

### All Elements

![](./00_pics/overview_allelements.png)

### Internal Static Structure 

![](./00_pics/overview_structure_hierarchy.png)

![](./00_pics/overview_internalstructure.png)


