import maya.cmds as cmds
import maya.api.OpenMaya as om
import unittest

import riglib.chain 
reload (riglib.chain)
from riglib.chain import Chain 


def deleteSceneNodes():
	selection =  cmds.ls(transforms = True, v = True)
	if len(selection) > 0:
		cmds.delete(cmds.ls(transforms = True, v = True))

def createSceneJoints():
	joints = []
	for i in range(5):
		jnt = cmds.joint(name = "joint_{}".format(i), 
			position = [0,i,0] )

		joints.append(jnt)

	cmds.select(cl = True)

	return joints



class TestChain(unittest.TestCase):

	def setUp(self):
		deleteSceneNodes()
		Chain.resetCount()
		self.joints = createSceneJoints()
		self.chainName = "newChain"
	 	self.chain = Chain(self.joints, name = self.chainName)

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


if __name__ == "__main__":
	testCases = [TestChain]

	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner().run(suite)


