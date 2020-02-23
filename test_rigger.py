import maya.cmds as cmds
import maya.api.OpenMaya as om
import unittest

import riglib.rigger 
reload (riglib.rigger)
from riglib.rigger import Rigger



import riglib.tests_functions
reload (riglib.tests_functions)
from riglib.tests_functions import deleteSceneNodes, createSceneJoints
	
class TestRigger(unittest.TestCase):
	pass 


def runTests():
	print ("\n TEST RIGGER")
	testCases = [TestRigger]

	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner().run(suite)

if __name__ == "__main__":

	runTests()