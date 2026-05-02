"""Simple parser for the small ARCA language used in examples.

This parser implements a best-effort interpreter of the example grammar
found in `test/examples/arcacode/firstExample.arc` and produces
PUMLA model objects: PUMLAElement, PUMLARelation, PUMLAConnection and
PUMLADiagram.

The goal is not to be a full language implementation but to cover the
constructs used in the example: `block` definitions with nested
contents, ports, tags/values, descriptions and connection arrow lines
that may be chained.
"""

# AI (github copilot) generated this code based on the example ARCA file and the PUMLA model classes. It uses regex
# and some heuristics to parse the ARCA syntax and build the corresponding PUMLA model objects.

import re
import ast
from pumla.model.PUMLAElement import PUMLAElement
from pumla.model.PUMLARelation import PUMLARelation
from pumla.model.PUMLAConnection import PUMLAConnection
from pumla.model.PUMLADiagram import PUMLADiagram


def _strip_comment(line):
    # ARCA examples use '#' for comments
    if '#' in line:
        return line.split('#', 1)[0]
    return line


def _parse_values_token(token):
    """Parse a values token which may be a JSON-like list or a quoted string."""
    token = token.strip()
    try:
        # try literal_eval for lists like ["A", "B"]
        val = ast.literal_eval(token)
        return val
    except Exception:
        # strip quotes if present
        return token.strip('"')


def _find_stereotypes_in_declaration(line):
    sts = []
    for m in re.findall(r'<<([^>]+)>>', line):
        sts.append(m.strip())
    return sts


def _create_element(alias, name=None, el_type='block', stereotypes=None, parent=None, filename='-', path='-'):
    el = PUMLAElement()
    el.setAlias(alias)
    el.setName(name if name else alias)
    el.setType(el_type)
    if stereotypes:
        for s in stereotypes:
            el.addStereotype(s)
    if parent:
        el.setParent(parent)
    el.setFilename(filename)
    el.setPath(path)
    return el


def parse_arca_file(filename):
    """Parse an ARCA file and return (diagram, elements, relations, connections).

    diagram: PUMLADiagram
    elements: list[PUMLAElement]
    relations: list[PUMLARelation]
    connections: list[PUMLAConnection]
    """
    text = open(filename, 'r').read()
    lines = text.splitlines()

    inside = False
    diagram_alias = 'arcasimple'
    diagram = None

    elements = []
    relations = []
    connections = []

    # helper maps to keep partially filled element dicts by alias
    element_map = {}

    # a simple stack to track current block parents based on indentation
    stack = []  # list of (indent_level, alias)

    for i, raw in enumerate(lines):
        line = raw.rstrip('\n')
        if '@startarcasimple' in line:
            inside = True
            diagram = PUMLADiagram(diagram_alias)
            continue
        if '@endarcasimple' in line:
            inside = False
            break
        if not inside:
            continue

        # remove comments
        code = _strip_comment(line)
        if code.strip() == '':
            continue

        indent = len(code) - len(code.lstrip(' '))
        stripped = code.strip()

        # block declaration
        m = re.match(r'block\s+(\w+)(?:\s+<<([^>]+)>>)?(?:\s+as\s+"([^"]+)")?\s*(:)?', stripped)
        if m:
            alias = m.group(1)
            stereo = m.group(2)
            name = m.group(3)
            stereotypes = []
            if stereo:
                stereotypes.append(stereo)
            # determine parent from stack
            parent = stack[-1][1] if stack and indent > stack[-1][0] else None
            el = _create_element(alias, name=name, el_type='block', stereotypes=stereotypes, parent=parent, filename=filename)
            element_map[alias] = {'element': el, 'ports': [], 'taggedvalues': {}}
            elements.append(el)
            # if block had colon, push to stack
            if m.group(4):
                stack.append((indent, alias))
            else:
                # ensure this alias is not considered parent for following indented lines
                pass
            continue

        # leave block when indentation reduces
        while stack and indent <= stack[-1][0] and stripped and not stripped.startswith('port'):
            stack.pop()

        # inside a block context, detect block internals, ports, tag, values, description
        if stack:
            current_alias = stack[-1][1]
            emap = element_map[current_alias]

            # internals:
            if stripped.startswith('internals:'):
                # following lines with greater indent contain aliases
                continue
            # an internal item line (alias only)
            if re.match(r'^[A-Za-z0-9_]+$', stripped):
                # assume an internal element alias
                emap['taggedvalues'].setdefault('internals', []).append(stripped)
                continue

            # tag "..."
            if stripped.startswith('tag '):
                tagm = re.match(r'tag\s+"([^"]+)"', stripped)
                if tagm:
                    emap['taggedvalues'].setdefault('tag', []).append(tagm.group(1))
                continue

            # values ... could be list or string
            if stripped.startswith('values '):
                vals = stripped.replace('values', '', 1).strip()
                parsed = _parse_values_token(vals)
                emap['taggedvalues'].setdefault('values', []).extend(parsed if isinstance(parsed, list) else [parsed])
                continue

            # description: multiline quoted string below
            if stripped.startswith('description:'):
                # read following indented quoted lines
                desc = ''
                j = i + 1
                while j < len(lines):
                    nxt = _strip_comment(lines[j]).rstrip('\n')
                    if nxt.strip() == '':
                        j += 1
                        continue
                    if len(nxt) - len(nxt.lstrip(' ')) <= indent:
                        break
                    # capture quoted content
                    q = nxt.strip()
                    if q.startswith('"') and q.endswith('"'):
                        desc = q.strip('"')
                    else:
                        # try to extract inside quotes
                        qm = re.search(r'"([^"]+)"', q)
                        if qm:
                            desc = qm.group(1)
                    j += 1
                if desc:
                    emap['taggedvalues'].setdefault('description', []).append(desc)
                continue

            # port definitions
            pm = re.match(r'port\s+(\w+)(?:\s+as\s+"([^"]+)")?\s*(:)?', stripped)
            if pm:
                palias = pm.group(1)
                pname = pm.group(2) if pm.group(2) else palias

                pcolon = pm.group(3)
                port = {"name": pname, "interfacetype": '-', "type": 'inout', "alias": palias, "taggedvalues": []}
                emap['ports'].append(port)
                # if port has colon, capture nested tag/values lines
                if pcolon:
                    j = i + 1
                    while j < len(lines):
                        nxt = _strip_comment(lines[j]).rstrip('\n')
                        if nxt.strip() == '':
                            j += 1
                            continue
                        if len(nxt) - len(nxt.lstrip(' ')) <= indent:
                            break
                        s = nxt.strip()
                        if s.startswith('tag '):
                            mtag = re.match(r'tag\s+"([^"]+)"', s)
                            if mtag:
                                port['taggedvalues'].append({"tag": mtag.group(1), "values": []})
                        if s.startswith('values '):
                            valtxt = s.replace('values', '', 1).strip()
                            v = _parse_values_token(valtxt)
                            if port['taggedvalues']:
                                port['taggedvalues'][-1]["values"].extend(v if isinstance(v, list) else [v])
                        j += 1
                continue

        # connection / relation lines are specified outside block contents in example
        # detect arrow lines anywhere
        if any(sym in stripped for sym in ['--->', '===>', '...>', '--r>', '<r--', '--c>']):
            # split into nodes and arrows preserving arrow tokens (and optional [...] bracket)
            parts = re.split(r'(\s*(?:===>|--->|\.{3}>|--r>|<r--|--c>)\s*(?:\[[^\]]+\])?\s*)', stripped)
            # parts: node, arrow, node, arrow, node ...
            for idx in range(1, len(parts), 2):
                start = parts[idx-1].strip()
                arrowpart = parts[idx].strip()
                end = parts[idx+1].strip()

                # extract arrow symbol and optional bracket
                am = re.match(r'(===>|--->|\.{3}>|--r>|<r--|--c>)(?:\s*(\[[^\]]+\]))?', arrowpart)
                if not am:
                    continue
                arrow = am.group(1)
                bracket = am.group(2)
                con_id = None
                con_text = ''
                con_stereos = []
                if bracket:
                    inner = bracket.strip('[]')
                    # alias maybe present
                    # alias as "text" or <<st>> or <<st>> with alias
                    # try to extract alias
                    m_alias = re.match(r'([^\s<\"]+)', inner)
                    if m_alias:
                        con_id = m_alias.group(1)
                    # extract as "text"
                    m_txt = re.search(r'as\s+"([^"]+)"', inner)
                    if m_txt:
                        con_text = m_txt.group(1)
                    # extract stereotypes
                    sts = re.findall(r'<<([^>]+)>>', inner)
                    for s in sts:
                        con_stereos.append(s)

                # assign an id if none
                if not con_id:
                    con_id = "CON#%d" % (len(connections) + len(relations) + 1)

                # decide whether this is a Connection or a Relation
                if arrow in ('--->', '===>'):
                    c = PUMLAConnection(con_id, start, arrow, end, con_text)
                    # add possible stereotype as tagged value
                    for s in con_stereos:
                        c.addTaggedValue('stereotype', s)
                    connections.append(c)
                else:
                    # treat as relation
                    r = PUMLARelation(con_id, start, arrow, end, con_text)
                    for s in con_stereos:
                        r.addTaggedValue('stereotype', s)
                    relations.append(r)
            continue

    # finalise element objects: fill ports and tagged values
    for alias, emap in element_map.items():
        el = emap['element']
        for p in emap['ports']:
            el.addPort(p)
        # tagged values: merge into element tagged values
        for k, v in emap['taggedvalues'].items():
            for val in v:
                el.addTaggedValue(k, val)
        # add to diagram
        if diagram:
            diagram.addElement(el)

    return diagram, elements, relations, connections


if __name__ == '__main__':
    # quick CLI for manual testing
    import sys
    if len(sys.argv) < 2:
        print('Usage: arca_parser.py <file.arc>')
        sys.exit(1)
    d, els, rels, cons = parse_arca_file(sys.argv[1])
    print('Diagram:', d.alias if d else None)
    print('Elements:')
    for e in els:
        print('-', e.getAlias(), 'name=', e.getName(), 'ports=', [p['name'] for p in e.getPorts()])
    print('Relations:', len(rels))
    print('Connections:', len(cons))

