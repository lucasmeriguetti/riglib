import maya.cmds as cmds
import maya.api.OpenMaya as om
import unittest

import riglib.rigger 
reload (riglib.rigger)
from riglib.rigger import Rigger

import riglib.chain 
reload (riglib.chain)
from riglib.chain import Chain 

import riglib.tests_functions
reload (riglib.tests_functions)
from riglib.tests_functions import deleteSceneNodes, createSceneJoints

class TestRigger(unittest.TestCase):
	def setUp(self):
		deleteSceneNodes()
		Chain.resetCount()
		Rigger.resetCount()
		self.joints = createSceneJoints()
		self.chainName = "newChain"
	 	self.chain = Chain(self.joints, name = self.chainName)

	def tearDown(self):
		deleteSceneNodes()
	 	Chain.resetCount()
	 	pass

	def test_addWeightAttrToChain(self):
		rigger = Rigger(self.chain, name = "NewRig")
		container = rigger.getChain().getContainer().getName()
		result = cmds.listAttr(container, string = rigger.getName())[0]
		self.assertEqual(result, rigger.getName())

	def test_connectWeightAttrToConstraints(self):
		rigger = Rigger(self.chain, name = "NewRig")
		chain = rigger.getChain()
		containerAttr =chain.getContainer().findPlug(rigger.getName())
		containerAttrConnections = cmds.listConnections(containerAttr)

		pConst = chain.getParentConstraints()
		sConst = chain.getParentConstraints()

		result  = len(pConst) + len(sConst)

		self.assertEqual(len(containerAttrConnections), result)

	
def runTests():
	print ("\n TEST RIGGER")
	testCases = [TestRigger]
	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
	runTests()