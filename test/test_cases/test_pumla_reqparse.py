"""pumla unit tests."""
import pytest
from pathlib import Path

from pumla.control.reqparse import *


@pytest.fixture
def examples_path():
    """get the path to the examples for the tests."""
    return Path(__file__).parent.parent / "examples/WeatherStation"


def test_01_findAllOUMLAReqFiles(examples_path):
    """test the method: findAllPUMLAReqFiles(...)"""
    expected_result = sorted(
        [
            examples_path / "req.yaml",
            examples_path / "CWeather/req.yaml",
            examples_path / "tempSensorA/req.yaml",
        ]
    )
    result = findAllPUMLAReqFiles(str(examples_path))
    result = sorted(map(Path, result))

    assert result == expected_result


def test_02_parsePUMLAReqFile(examples_path):
    """test the method: parsePUMLAReqFile(...)"""
    filename = examples_path / "tempSensorA/req.yaml"
    exp_result_tyoe = "Requirement"
    exp_result_alias = "REQ_SensorA1"
    exp_result_derivedfrom = ["REQ_WS1"]


    pels = parsePUMLAReqFile(str(filename))
    result_elem = pels[0]
    print(result_elem)

    assert result_elem["type"] == exp_result_tyoe

    assert result_elem["alias"] == exp_result_alias

    assert result_elem["derived_from"] == exp_result_derivedfrom



