import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")

from test_cases.test_pumla_cmd_utils import getTestClass as getCmdUtilsTestClass

def testAll():
    tc = getCmdUtilsTestClass()
    tci = tc()
    tci.executeTests()

    # next

if __name__ == "__main__":
    testAll()

