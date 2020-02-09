import maya.cmds as cmds
import maya.api.OpenMaya as om
import unittest
import math

import riglib.mutil
reload(riglib.mutil)
from riglib.mutil import *
def deleteSceneNodes():
	selection =  cmds.ls(transforms = True, v = True)
	if len(selection) > 0:
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

class TestTransform(unittest.TestCase):

	def setUp(self):
		deleteSceneNodes()
		cmds.polyCube(name = "box")
		self.transform = Transform("box")

	def tearDown(self):
		deleteSceneNodes()
		pass

	def test_translation(self):
		self.transform.setTranslation((10,0,0), Space.WORLD)
		result = self.transform.translation(Space.WORLD)
		self.assertEqual(result.x, 10)

	def test_rotation(self):
		rotation = om.MVector(90,0,0)
		self.transform.setEulerRotation(rotation)
		
		result = self.transform.eulerRotation()
		self.assertEqual(result.x, 90)

	def test_vectorRadiansToDegrees(self):
		result = self.transform.vectorRadiansToDegrees((math.pi/2,0,0))
		self.assertEqual(result.x, 90)

	def test_vectorDegreesToRadians(self):
		result = self.transform.vectorDegreesToRadians((90,0,0))
		self.assertEqual(result.x, math.pi/2)


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestSelectionList)
	unittest.TextTestRunner().run(suite)

	suite = unittest.TestLoader().loadTestsFromTestCase(TestSpace)
	unittest.TextTestRunner().run(suite)

	suite = unittest.TestLoader().loadTestsFromTestCase(TestTransform)
	unittest.TextTestRunner().run(suite)
