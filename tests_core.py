import maya.cmds as cmds
import riglib.core
reload(riglib.core)

from riglib.core import Chain

class TestScene(object):
	def __init__(self, count):
		self._count = count
		self._joints = []
		self.cleanScene()
		self.createScene()

	def getJoints(self):
		return self._joints

	def createScene(self):
		if self._joints != {}:
			self.cleanScene()

		for i in range(self._count):
			j = cmds.joint(name = "joint_{}".format(i), position = (i*3,0,0))
			self._joints.append(j)


	def cleanScene(self):
		if len(cmds.ls(type = "joint")) > 0:
			cmds.delete(cmds.ls(type = "joint"))
		self._joints = []

class ChainTests(object):
	def __init__(self):
		self.countTest()
		self.createChainJointsTest()

	def countTest(self):
		#test1
		Chain.resetCount()
		Chain()
		assert(Chain.getChainCount() == 1), "Test1, count != 1"

		#test2
		assert(type(Chain.getChainCount()) == int), "Test2, not a int"

		#test3
		Chain.resetCount()
		for i in range(5):
			Chain()
		assert(Chain.getChainCount() == 5), "Test3, count != 5"

		print("No errors in countTest()")

	def createChainJointsTest(self):
		Chain.resetCount()
		scene = TestScene(5)

		for joint in scene.getJoints():
			cmds.xform(joint, os = True, ro = (5,5,5))
			
		cmds.select(cl = True)
		chain = Chain(joints = scene.getJoints(), name = "Main")

		#test1
		assert chain.getJoints() != [], "test1, empty joint list"

		#test2
		assert cmds.objectType(chain.getJoints()[0], isType = "joint"), "test2, is not a joint"

		#test3
		for input, joint in zip(scene.getJoints(), chain.getJoints()):
			inputTranslation = cmds.xform(input, query = True, ws = True, t = True)
			inputRotation = cmds.xform(input, query = True, ws = True, ro = True)

			chainTranslation = cmds.xform(joint, query = True, ws = True, t = True)
			chainRotation = cmds.xform(joint, query = True, ws = True, ro = True)

			for a,b in zip(inputTranslation, chainTranslation):
				assert round(a, 3) == round(b,3), "test3, translation is not the same"
			
			for a,b in zip(inputRotation, chainRotation):
				assert round(a, 3) == round(b,3), "test3, translation is not the same"

		print("No errors in createChainJointsTest()")

		#scene.cleanScene()
		


ChainTests()
	