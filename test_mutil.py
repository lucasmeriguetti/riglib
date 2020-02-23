import maya.cmds as cmds
import maya.api.OpenMaya as om
import unittest
import math

import riglib.mutil
reload(riglib.mutil)
from riglib.mutil import *

print ("\n TEST MUTIL")

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

class TestDagNode(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		deleteSceneNodes()
		cmds.createNode("transform", name = "parent")
 		cmds.createNode("transform", name = "child")
 		

 	@classmethod	
	def tearDownClass(cls):
		deleteSceneNodes()
		

	def setUp(self):
		self.dag = DagNode("parent")

	def test_addChild(self):
		self.dag.addChild("child")
		result = cmds.listRelatives("parent", children = True)[0]
		self.assertEqual(result, "child")

	def test_setGetName(self):
		self.dag.setName("NewNameParent")
		result = self.dag.getName()
		self.assertEqual(result, "NewNameParent")

	def test_getPath(self):
		dag = self.dag.getPath()
		self.assertEqual(type(dag), om.MDagPath)

	def test_create(self):
		dag = DagNode.create("transform")
		self.assertEqual(type(dag), DagNode)

	def test_addAttr(self):
		attrName = "newAttr1"
		self.dag.addAttr(attrName, "float", keyable = True)

		result = cmds.listAttr("parent", string = attrName)[0]
		self.assertEqual(result, attrName)


def runTests():
	testCases = [TestSelectionList, 
		TestSpace,
		TestTransform,
		TestDagNode]

	for case in testCases:
		suite = unittest.TestLoader().loadTestsFromTestCase(case)
		unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
	runTests()



