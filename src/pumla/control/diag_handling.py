"""functions to handle pumla diagrams and pumla-specific .svg diagram generation."""
from pumla.model.PUMLADiagram import PUMLADiagram
from pumla.model.PUMLAElement import PUMLAElement
from pumla.view.PUMLASVGDiagram import PUMLASVGDiagram

def genpumladiag(mainpath, inputpuml, outputname, layoutoverride):
    print("feature not yet implemented. sorry.")

    d = PUMLADiagram("diag1", "My first pumla SVG Diagram")
    e1 = PUMLAElement()
    e1.setAlias("huhu")
    e1.setName("Huhu")
    e1.addStereotype("system")
    e1.addStereotype("block")

    e2 = PUMLAElement()
    e2.setAlias("trara")
    e2.setName("Trara Trara")

    d.addElement(e1)
    d.addElement(e2)

    svg_d = PUMLASVGDiagram(d)
    svg_d.generateHTMLfile()




def parsePUMLADRFile(file):
    pass
