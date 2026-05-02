"""Unit tests for the ARCA parser module."""
import pytest
from pathlib import Path

from pumla.control.arca_parser import parse_arca_file


@pytest.fixture()
def example_arc_path():
    return Path(__file__).parent.parent / "examples" / "arcacode" / "firstExample.arc"


def _find_by_alias(elements, alias):
    for e in elements:
        if e.getAlias() == alias:
            return e
    return None


def test_parse_first_example_counts(example_arc_path):
    diagram, elements, relations, connections = parse_arca_file(str(example_arc_path))

    assert diagram is not None
    assert diagram.alias == 'arcasimple'

    # The example contains 8 block elements (display, sensorA, compute, x, y, z, z1, z2)
    assert len(elements) == 8

    # expected aliases
    aliases = set(e.getAlias() for e in elements)
    assert aliases == {"display", "sensorA", "compute", "x", "y", "z", "z1", "z2"}

    # relationships / connections counts are implementation-dependent but should match the example's parsing
    assert len(relations) >= 1
    assert len(connections) >= 1


def test_elements_and_ports(example_arc_path):
    _, elements, _, _ = parse_arca_file(str(example_arc_path))

    display = _find_by_alias(elements, 'display')
    assert display is not None
    assert display.getName() == 'Display'

    sensor = _find_by_alias(elements, 'sensorA')
    assert sensor is not None
    assert sensor.getName() == 'TempSensor A'

    compute = _find_by_alias(elements, 'compute')
    assert compute is not None
    assert compute.getName() == 'Compute Unit'

    x = _find_by_alias(elements, 'x')
    assert x is not None
    assert len(x.getPorts()) == 2

    y = _find_by_alias(elements, 'y')
    assert y is not None
    assert len(y.getPorts()) == 3

    z2 = _find_by_alias(elements, 'z2')
    assert z2 is not None
    assert len(z2.getPorts()) == 2


def test_connections_and_relations_details(example_arc_path):
    _, _, relations, connections = parse_arca_file(str(example_arc_path))

    # check that a connection sensorA -> compute exists (arrow '--->')
    assert any((c.getStart() == 'sensorA' and c.getEnd() == 'compute' and c.getConType() == '--->') for c in connections)

    # check that the named connection myCon1 from the example is present with the expected text
    mycon = next((c for c in connections if c.getID() == 'myCon1'), None)
    assert mycon is not None, 'expected connection with id myCon1'
    assert mycon.getConTxt() == 'data flowing here'

    # check that a relation with stereotype 'delegates' is present (myCon2)
    myrel = next((r for r in relations if r.getID() == 'myCon2'), None)
    assert myrel is not None, 'expected relation with id myCon2'
    tvs = myrel.getTaggedValues()
    assert 'stereotype' in tvs
    assert 'delegates' in tvs['stereotype']

