import maya.cmds as cmds
import maya.api.OpenMaya as om
import unittest

import riglib.rigger 
reload (riglib.rigger)
from riglib.rigger import Rigger

print ("\n TEST RIGGER")

class TestRigger(unittest.TestCase):
	pass 

def runTests():
	testCases = [TestRigger]

	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
	runTests()