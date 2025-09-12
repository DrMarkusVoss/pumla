"""pumla unit tests."""
import pytest
from pathlib import Path

from pumla.control.cmd_utils import *


@pytest.fixture
def examples_path():
    """get the path to the examples for the tests."""
    return Path(__file__).parent.parent / "examples/WeatherStation"


def test_01_findAllPUMLAFiles(examples_path):
    """test the method: findAllPUMLAFiles(...)"""
    expected_result = sorted(
        [
            examples_path / "tempSys.puml",
            examples_path / "reusableClass1.puml",
            examples_path / "tempSysInstances.puml",
            examples_path / "tempSensorB/tempSensorB.puml",
            examples_path / "tempSensorB/publicState.puml",
            examples_path / "anotherClass/anotherClass.puml",
            examples_path / "CWeather/CWeather.puml",
            examples_path / "CWeather/FurtherWeatherInstances.puml",
            examples_path / "CWeather/WeatherInstances.puml",
            examples_path / "wirelessUnit/wirelessUnit.puml",
            examples_path / "connections/connections_tempSys_Var_B.puml",
            examples_path / "connections/connections_tempSys_Var_A.puml",
            examples_path / "connections/connections_tempSys_Var_B2.puml",
            examples_path / "tempSensorA/tempSensorA.puml",
            examples_path / "tempSensorA/internalSequence.puml",
            examples_path / "tempSensorBdC/tempSensorBdC.puml",
            examples_path / "displayTemp/displayTemp.puml",
            examples_path / "tempConv/tempConverter.puml",
        ]
    )
    result, diagfiles = findAllPUMLAFiles(str(examples_path))
    result = sorted(map(Path, result))

    assert result == expected_result


def test_02_parsePUMLAFile(examples_path):
    """test the method: parsePUMLAFile(...)"""
    filename = examples_path / "tempConv/tempConverter.puml"
    exp_result_name = "Temp. Converter"
    exp_result_alias = "tempConverter"
    exp_result_parent = "tempSys"
    exp_result_filename = "tempConverter.puml"

    pels, rels, cons, tvs = parsePUMLAMRFile(str(filename))
    result_elem = pels[0]

    assert result_elem.name == exp_result_name

    assert result_elem.alias == exp_result_alias

    assert result_elem.parent == exp_result_parent

    assert result_elem.filename == exp_result_filename


def test_03_findStereoTypesInLine():
    """test the method: findStereoTypesInLine(...)"""
    line = 'rectangle "huhu" <<block>> <<component>><<external System>> as hu {'
    expected_result = ["block", "component", "external System"]
    result = findStereoTypesInLine(line)

    assert result == expected_result


def getAliasFromFileContent(line):
    global glob_alias
    glob_alias = None

    gd = {"glob_alias": glob_alias}
    alias_code = line.strip("'").strip(" ")
    # print("ac = " + alias_code)
    # will fill the alias variable with content from file.
    exec(alias_code, gd)

    # print(gd["alias"])

    return gd["glob_alias"]


def getExpectedResultFromFileContent(line):
    global glob_expected_result
    glob_expected_result = None
    exp_res_code = line.strip("'").strip(" ")
    erd = {"glob_expected_result": glob_expected_result}
    # will fill the expected result variable with content from file.
    exec(exp_res_code, erd)
    # print("er code = " + exp_res_code)
    # print(erd["expected_result"])

    return erd["glob_expected_result"]


def test_04_findElementNameAndTypeInText():
    test_04_pathname = Path(__file__).parent / "test_files_04"
    for fn in sorted(test_04_pathname.glob("*.puml")):
        print(f"Test file = {fn}")
        all_lines = fn.read_text().splitlines(False)

        # first line will contains the expected result
        alias = getAliasFromFileContent(all_lines[0])
        # second line will contain the expected result
        expected_result = getExpectedResultFromFileContent(all_lines[1])
        lines = all_lines[2:]
        result = findElementNameAndTypeInText(lines, alias)

        assert result == expected_result

def test_05_checkalias(examples_path):
    """test the method: checkElsRelsConsForAliasExistence(...)"""

    (success, efn, elements, relations, connections) = updatePUMLAMR(str(examples_path),
                                                                     str(examples_path) + "/modelrepo_json.puml")

    expected_result_huhu = False
    expected_result_CWeather = True
    expected_result_CWheather = False
    expected_result_rel1 = True
    expected_result_rel2 = False
    expected_result_con1 = True
    expected_result_con2 = False

    observed_result_huhu = checkElsRelsConsForAliasExistence(elements, relations, connections, "huhu")
    observed_result_CWeather = checkElsRelsConsForAliasExistence(elements, relations, connections, "CWeather")
    observed_result_CWheather = checkElsRelsConsForAliasExistence(elements, relations, connections, "CWheather")
    observed_result_rel1 = checkElsRelsConsForAliasExistence(elements, relations, connections, "REL#w3CWeather")
    observed_result_con1 = checkElsRelsConsForAliasExistence(elements, relations, connections, "CON#_SYS_VAR_B2")
    observed_result_rel2 = checkElsRelsConsForAliasExistence(elements, relations, connections, "REL#w3CWheather")
    observed_result_con2 = checkElsRelsConsForAliasExistence(elements, relations, connections, "CON_SYS_VAR_B2")



    assert observed_result_huhu == expected_result_huhu

    assert observed_result_CWeather == expected_result_CWeather

    assert observed_result_CWheather == expected_result_CWheather

    assert observed_result_rel1 == expected_result_rel1

    assert observed_result_rel2 == expected_result_rel2

    assert observed_result_con1 == expected_result_con1

    assert observed_result_con2 == expected_result_con2
