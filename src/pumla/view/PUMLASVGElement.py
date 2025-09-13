"""Class defining the SVG view of a model element."""
class PUMLASVGElement:
    """ class defining the SVG view of an atomic PUMLA model element """

    def __init__(self, element):
        self.element = element

    def generateSVG(self, count, y_offset):
        stps = ""
        for s in self.element.stereotypes:
            stps = stps + s + ", "

        stereotypes = "<< " + stps[:len(stps)-2] + " >>"
        svg_code = '<svg id="' + self.element.alias + '" width="600" height="400" xmlns="http://www.w3.org/2000/svg">\n'
        svg_code = svg_code + '<rect id="' + self.element.alias + '_rect" width="150" height="220" x="5" y="5" rx="20" ry="20" style="fill:yellow;stroke:black;stroke-width:3;opacity:0.5" />\n'
        svg_code = svg_code + '<text id="' + self.element.alias + '_txt" x="80" y="25" dominant-baseline="middle" text-anchor="middle" font-size="14" font-family="Arial, sans-serif" style="opacity:0.5" fill="black">' + self.element.name + '</text>\n'
        if self.element.stereotypes != []:
            svg_code = svg_code + '<text id="' + self.element.alias + '_txt" x="80" y="45" dominant-baseline="middle" text-anchor="middle" font-size="12" font-style="italic" font-family="Arial, sans-serif" style="opacity:0.5" fill="black">' + stereotypes + '</text>\n'
        svg_code = svg_code + '<set attributeName="x" to="' + str(count * (150 + 30) ) + '" /><set attributeName="y" to="' + str(y_offset) + '" /></svg>\n'

        return svg_code
