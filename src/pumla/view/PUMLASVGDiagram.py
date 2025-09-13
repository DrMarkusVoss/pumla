from pumla.model.PUMLAElement import PUMLAElement
from pumla.model.PUMLADiagram import PUMLADiagram
from pumla.view.PUMLASVGElement import PUMLASVGElement

"""Class defining the SVG view of a pumla diagram."""
class PUMLASVGDiagram:
    ''' Class defining the SVG view of a pumla diagram. '''
    def __init__(self, diagram):
        self.diagram = diagram
        self.svg_elements = []
        self.filename = "defaultHTMLwithSVGfilename.html"
        for e in self.diagram.elements:
            self.svg_elements.append(PUMLASVGElement(e))

    def generateSVG(self):
        svg_code = '<svg id="' + self.diagram.alias + '" width="' + str(len(self.svg_elements)*180) + '" height="1200" xmlns="http://www.w3.org/2000/svg">\n'
        svg_code = svg_code + '<text id="' + self.diagram.alias + '_titletxt" x="50%" y="10" dominant-baseline="middle" text-anchor="middle" font-size="20" font-family="Arial, sans-serif" fill="black">' + self.diagram.title + '</text>\n'

        cnt = 0
        for e in self.svg_elements:
            el_code = e.generateSVG(cnt, 30)
            svg_code = svg_code + el_code
            cnt += 1

        svg_code = svg_code + '</svg>\n'

        return svg_code


    def generateHTMLembeddedSVG(self):
        html_code = '<html>\n<body>\n<h1>' + self.diagram.title
        html_code = html_code + '</h1>\n\n'
        html_code = html_code + self.generateSVG()
        html_code = html_code + '\n</body>\n</html>\n'

        return html_code

    def generateHTMLfile(self, filename=""):
        with open(self.filename, "w") as f:
            f.write(self.generateHTMLembeddedSVG())


