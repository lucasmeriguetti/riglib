import maya.cmds as cmds
import maya.api.OpenMaya as om
import unittest

import riglib.chain 
reload (riglib.chain)
from riglib.chain import Chain 

import riglib.tests_functions
reload (riglib.tests_functions)
from riglib.tests_functions import deleteSceneNodes, createSceneJoints

print ("\n TEST CHAIN")


class TestChain(unittest.TestCase):


	def setUp(self):
		deleteSceneNodes()
		Chain.resetCount()
		self.joints = createSceneJoints()
		self.chainName = "newChain"
	 	self.chain = Chain(self.joints, name = self.chainName)

	def tearDown(self):
		deleteSceneNodes()
	 	Chain.resetCount()

	def test_getJoints(self):
		chainJoints = self.chain.getJoints()
		self.assertEqual(len(chainJoints), len(self.joints))
		self.assertNotEqual(len(chainJoints), 0)

	def test_chainCount(self):
		self.assertEqual(Chain.getChainCount(), 1)

		chain2 = Chain(self.joints, name = self.chainName)
		self.assertEqual(Chain.getChainCount(), 2)

		Chain.resetCount()
		self.assertEqual(Chain.getChainCount(), 0)

	def test_createChainJoints(self):
		deleteSceneNodes()
		Chain.resetCount()
		self.joints = createSceneJoints()

		for jnt in self.joints:
			cmds.setAttr(jnt + ".rx", 20)

		self.chainName = "newChain"
	 	self.chain = Chain(self.joints, name = self.chainName)

		for index, chainJnt in enumerate(self.chain.getJoints()):
			name = "{}_{}".format(self.chainName, Chain._count -1 )
			result ="{}_joint_{}".format(name, index)
			self.assertEqual(chainJnt, result)

		for jnt, chainJnt in zip(self.joints, self.chain.getJoints()):
			
			chainTranslation = cmds.xform(chainJnt, query = True, ws = True, t = True)
			jntTranslation =  cmds.xform(jnt, query = True, ws = True, t = True)
			for a,b in zip(jntTranslation, chainTranslation):
				self.assertEqual(round(a,3), round(b,3))

			chainRotation = cmds.xform(chainJnt, query = True, ws = True, ro = True)
			jntRotation = cmds.xform(jnt, query = True, ws = True, ro = True)
			for a,b in zip(chainRotation, jntRotation):
				self.assertEqual(round(a,3), round(b,3))
	
	def test_getConstraints(self):
		lst = []
		result = self.chain.getParentConstraints()
		self.assertNotEqual(result,lst)

		result = self.chain.getScaleConstraints()
		self.assertNotEqual(result,lst)

		result = self.chain.getParentConstraints(index = 0)
		self.assertEqual(cmds.objectType(result), "parentConstraint")

		result = self.chain.getScaleConstraints(0)
		self.assertEqual(cmds.objectType(result), "scaleConstraint")

	def test_constraintInputJoints(self):
		self.assertNotEqual(len(self.chain.getParentConstraints()), 0)
		self.assertNotEqual(len(self.chain.getScaleConstraints()), 0)
		self.assertEqual(cmds.objectType(self.chain.getParentConstraints()[0]), "parentConstraint")
		self.assertEqual(cmds.objectType(self.chain.getScaleConstraints()[0]), "scaleConstraint")

	def test_createChainGroup(self):
		chainGrp = self.chain.getChainGroup()
		chainOffsetGrp = self.chain.getChainGroup(True)
		self.assertNotEqual(chainGrp, None)
		self.assertNotEqual(chainOffsetGrp, None)

		result = cmds.listRelatives(chainGrp.getName(), children = True)[0]
		self.assertEqual(result, chainOffsetGrp.getName())

		result = cmds.listRelatives(chainOffsetGrp.getName(), children = True)[0]
		self.assertEqual(result, self.chain.getJoints()[0])

	def test_getWeightAlias(self):
		constraintName =  self.chain.getParentConstraints(0)
		weights = self.chain.getWeightAlias(constraintName)
		self.assertNotEqual(weights, [])


def runTests():
	testCases = [TestChain]

	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
	runTests()

