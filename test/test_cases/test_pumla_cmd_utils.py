import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
#print(os.path.dirname(os.path.abspath(__file__)) + "/../../../")
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

    def test_findAllPumlaFiles(self):
        print("test_findAllPumlaFiles()")
        expected_result = ['./../examples/tempSys.puml', './../examples/tempSensorA/tempSensorA.puml', './../examples/displayTemp/displayTemp.puml', './../examples/tempConv/tempConverter.puml']
        result = findAllPumlaFiles("./../examples")
        print(result)
        if (result == expected_result):
            print("test passed!")
        else:
            print("test failed!")
        self.printSeparation()

    def backToOldPath(self):
        os.chdir(self.oldpath)

    def cleanup(self):
        self.backToOldPath()

    def executeTests(self):
        self.test_findAllPumlaFiles()

        # needs to be at the end of this method
        self.cleanup()


def getTestClass():
    return TestPumlaCmdUtils

if __name__ == "__main__":
    tc = TestPumlaCmdUtils()
    tc.test_findAllPumlaFiles()

