# puma
puma = PlantUML Manager

## Idea
In order to enable systematic re-use for architecture models with PlantUML, 
*puma* is intended to be an extension around PlantUML to organize this systematic re-use.

### Use Cases
- Architecture Modelling of a bigger solution using PlantUML
- Have the same model elements in different diagrams as single source entities
- create an arc42 architecture documentation based on common PlantUML description patterns

### Solution Ideas
The following concepts are to be implemented:
- PlantUML modelling guideline
- common templates using subroutines in a common way
- file manager, gathering all modelling PlantUML files from a repository
- instantiation mechanism, which allows to instantiate the model elements in different diagrams
- arc42 template with arc42 generator