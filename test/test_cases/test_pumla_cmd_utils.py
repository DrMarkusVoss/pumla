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

    def test_findAllPUMLAFiles(self):
        print("test_findAllPumlaFiles()")
        expected_result = ['./../examples/tempSys.puml', './../examples/wirelessUnit/wirelessUnit.puml',
                           './../examples/tempSensorA/tempSensorA.puml', './../examples/displayTemp/displayTemp.puml',
                           './../examples/tempConv/tempConverter.puml']
        result = findAllPUMLAFiles("./../examples")
        #print(result)
        if (result == expected_result):
            print("test passed!")
        else:
            print("test failed!")
        self.printSeparation()

    def test_parsePUMLAFile(self):
        print("test_parsePUMLAFile()")
        filename = "./../examples/tempConv/tempConverter.puml"
        exp_result_name = "Temp. Converter"
        exp_result_alias = "tempConverter"
        exp_result_parent = "tempSys"
        exp_result_filename = "tempConverter.puml"

        test_passed = True

        result_elem = parsePUMLAFile(filename)

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



    def backToOldPath(self):
        os.chdir(self.oldpath)

    def cleanup(self):
        self.backToOldPath()

    def executeTests(self):
        self.test_findAllPUMLAFiles()
        self.test_parsePUMLAFile()

        # needs to be at the end of this method
        self.cleanup()


def getTestClass():
    return TestPumlaCmdUtils

if __name__ == "__main__":
    tc = TestPumlaCmdUtils()
    tc.executeTests()

