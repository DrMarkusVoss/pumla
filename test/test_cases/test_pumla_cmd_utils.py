import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
from modules.control.cmd_utils import *

class TestPumlaCmdUtils:
    def __init__(self):
        self.oldpath = os.path.abspath(os.curdir)
        mypath = os.path.dirname(__file__)
        if (not(mypath == "")):
            os.chdir(mypath)
        pass

    def printSeparation(self):
        print("---------------------------------")

    def test_01_findAllPUMLAFiles(self):
        print("test_01_findAllPumlaFiles()")
        expected_result = ['./../examples/tempSys.puml',
                           './../examples/tempSysInstances.puml',
                           './../examples/tempSensorB/tempSensorB.puml',
                           './../examples/tempSensorB/publicState.puml',
                           './../examples/anotherClass/anotherClass.puml',
                           './../examples/CWeather/CWeather.puml',
                           './../examples/CWeather/WeatherInstances.puml',
                           './../examples/wirelessUnit/wirelessUnit.puml',
                           './../examples/connections/connections_tempSys_Var_B.puml',
                           './../examples/connections/connections_tempSys_Var_A.puml',
                           './../examples/connections/connections_tempSys_Var_B2.puml',
                           './../examples/tempSensorA/tempSensorA.puml',
                           './../examples/tempSensorA/internalSequence.puml',
                           './../examples/tempSensorBdC/tempSensorBdC.puml',
                           './../examples/displayTemp/displayTemp.puml',
                           './../examples/tempConv/tempConverter.puml']

        result = findAllPUMLAFiles("./../examples")
        #print(result)
        if (result == expected_result):
            print("test passed!")
        else:
            print("test failed!")
        self.printSeparation()

    def test_02_parsePUMLAFile(self):
        print("test_02_parsePUMLAFile()")
        filename = "./../examples/tempConv/tempConverter.puml"
        exp_result_name = "Temp. Converter"
        exp_result_alias = "tempConverter"
        exp_result_parent = "tempSys"
        exp_result_filename = "tempConverter.puml"

        test_passed = True

        pels, rels, cons = parsePUMLAFile(filename)
        result_elem = pels[0]

        if (not(result_elem.name == exp_result_name)):
            test_passed = False

        if (not(result_elem.alias == exp_result_alias)):
            test_passed = False

        if (not(result_elem.parent == exp_result_parent)):
            test_passed = False

        if (not(result_elem.filename == exp_result_filename)):
            test_passed = False

        if (test_passed):
            print("test passed!")
        else:
            print("test failed!")
        self.printSeparation()


    def test_03_findStereoTypesInLine(self):
        print("test_03_findStereoTypesInLine()")
        test_passed = False
        line = 'rectangle "huhu" <<block>> <<component>><<external System>> as hu {'
        expected_result = ['block', 'component', 'external System']
        result = findStereoTypesInLine(line)
        #print(result)
        if (result == expected_result):
            test_passed = True
        else:
            test_passed = False

        if (test_passed):
            print("test passed!")
        else:
            print("test failed!")
        self.printSeparation()

    def getAliasFromFileContent(self, line):
        alias = None
        alias_code = line.strip("'").strip(" ")
        # will fill the alias variable with content from file.
        exec(alias_code)

        return alias

    def getExpectedResultFromFileContent(self, line):
        expected_result = None
        exp_res_code = line.strip("'").strip(" ")
        # will fill the expected result variable with content from file.
        exec(exp_res_code)
        #print(expected_result)

        return expected_result

    def test_04_findElementNameAndTypeInText(self):
        print("test_04_findElementNameAndTypeInText()")

        test_04_pathname = "./test_files_04"
        for files in os.walk(test_04_pathname):
            for f in files[2]:
                # make sure not to test the README.md
                if (".puml" in f):
                    fn = test_04_pathname + "/" + f.strip(".")
                    print("Test file = " + fn)
                    file = open(fn)
                    text = file.read()
                    file.close()

                    all_lines = text.split("\n")
                    # first line will contains the expected result
                    alias = self.getAliasFromFileContent(all_lines[0])
                    # second line will contain the expected result
                    expected_result = self.getExpectedResultFromFileContent(all_lines[1])
                    lines = all_lines[2:]
                    result = findElementNameAndTypeInText(lines, alias)

                    if (result == expected_result):
                        test_passed = True
                    else:
                        test_passed = False
                    if (test_passed):
                        print("test passed!")
                    else:
                        print("test failed!")
                        print(result)
                        print(expected_result)
                    self.printSeparation()



    def backToOldPath(self):
        os.chdir(self.oldpath)

    def cleanup(self):
        self.backToOldPath()

    def executeTests(self):
        self.test_01_findAllPUMLAFiles()
        self.test_02_parsePUMLAFile()
        self.test_03_findStereoTypesInLine()
        self.test_04_findElementNameAndTypeInText()

        # needs to be at the end of this method
        self.cleanup()


def getTestClass():
    return TestPumlaCmdUtils

if __name__ == "__main__":
    tc = TestPumlaCmdUtils()
    tc.executeTests()

