import maya.cmds as cmds
import maya.api.OpenMaya as om
import unittest

import riglib.mutil
reload(riglib.mutil)
from riglib.mutil import *
def deleteSceneNodes():
	cmds.delete(cmds.ls(transforms = True, v = True))

class TestSelectionList(unittest.TestCase):

	def setUp(self):
		deleteSceneNodes()
		self.transform = cmds.polyCube(name = "box")[0]

	def tearDown(self):
		deleteSceneNodes()

	def test_getDagPath(self):
		result = SelectionList.getDagPath(self.transform)
		self.assertEquals(type(result), om.MDagPath)

	def test_getDependNode(self):
		result = SelectionList.getDependNode(self.transform)
		self.assertEquals(type(result), om.MObject)


class TestSpace(unittest.TestCase):

 	def setUp(self):
 		deleteSceneNodes()
 		parent = cmds.createNode("transform", name = "parent")
 		child = cmds.createNode("transform", name = "child")
 		cmds.parent(child, parent)
 		cmds.xform(parent, translation = (10, 0,0))
 		
 		self.dag = SelectionList.getDagPath(child)
		self.fnTransform = om.MFnTransform(self.dag)

	def tearDown(self):
		deleteSceneNodes()

 	def test_World(self):
 		result = self.fnTransform.translation(Space.WORLD)
 		self.assertEqual(result.x, 10)

 	def test_Object(self):
 		result = self.fnTransform.translation(Space.OBJECT)
 		self.assertEqual(result.x, 0)



if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestSelectionList)
	unittest.TextTestRunner().run(suite)

	suite = unittest.TestLoader().loadTestsFromTestCase(TestSpace)
	unittest.TextTestRunner().run(suite)
