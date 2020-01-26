import maya.cmds as cmds
import maya.api.OpenMaya as om

import riglib.mautil
reload (riglib.mautil)

from riglib.mautil import SelectionList, Transform

class SelectionListTests(object):
	def __init__(self):
		self.getDagPathTest()

	def getDagPathTest(self):
		#test1
		try:
			cmds.delete("box1")
		except:
			pass

		cmds.polyCube(name = "box1")
		dag = SelectionList.getDagPath("box1")
		assert type(dag) == om.MDagPath, "test1: not a MDagPath"

		cmds.delete("box1")
		print("No errors in getDagPathTest()")

class TransformTests(object):
	def __init__(self):
		self.translationTest()

	def translationTest(self):
		try:
			cmds.delete("box1")
		except:
			pass

		cmds.polyCube(name = "box1")
		cmds.move(10, 5, 6, "box1")
		transform = Transform("box1")
		
		#test1
		assert type(transform.translation()) == om.MVector, "test1, not a MVector"

		#test2
		mvector = transform.translation()
		assert mvector.x == 10, "test2"

		print("No errors in translationTest()")




SelectionListTests()
TransformTests()