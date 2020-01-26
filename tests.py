import maya.cmds as cmds
import riglib.core
reload(riglib.core)

from riglib.core import Chain

class TestScene(object):

	def __init__(self, count):
		self._count = count
		self._joints = []
		self.create_scene()

	def get_joint():
		return self._joints

	def create_scene(self):
		if self._joints != {}:
			self.clean_scene()

		for i in range(self._count):
			j = cmds.joint(name = "joint_{}".format(i), position = (i*3,0,0))
			self._joints.append(j)


	def clean_scene(self):
		cmds.delete(cmds.ls(type = "joint"))
		self._joints = []

class Tests(object):
	def __init__(self):
		self.chain_count_tests()

	def chain_count_tests(self):
		#test1
		Chain.reset_count()
		Chain(TestScene(5))
		assert(Chain.get_chain_count() == 1), "Test1, count != 1"

		#test2
		assert(type(Chain.get_chain_count()) == int), "Test2, not a int"

		#test3
		Chain.reset_count()
		for i in range(5):
			Chain(TestScene(5))
		assert(Chain.get_chain_count() == 5), "Test3, count != 5"

		print("No errors in chain_count_test()")

Tests()
	