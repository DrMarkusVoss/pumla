import sys
import os
sys.path.append(os.curdir + "/../../")

from modules.control.cmd_utils import *

def printSeparation():
    print("---------------------------------")

def test_findAllPumlaFiles():
    print("test_findAllPumlaFiles()")
    expected_result = ['./../examples/displayTemp/displayTemp.puml', './../examples/tempConv/tempConverter.puml']
    result = findAllPumlaFiles("./../examples")
    if (result == expected_result):
        print("test passed!")
    else:
        print("test failed!")
    printSeparation()

if __name__ == "__main__":
    test_findAllPumlaFiles()

