import maya.cmds as cmds
import maya.api.OpenMaya as om 

class SelectionList(object):
	@staticmethod
	def getDagPath(name):
		list_selection = om.MSelectionList()
		list_selection.add(name)
		return list_selection.getDagPath(0)

class Space(object):
	WORLD = om.MSpace.kWorld
	OBJECT = om.MSpace.kObject

class Transform(object):
	def __init__(self, name):
		self._dag = SelectionList.getDagPath(name)
		self._fnTransform = om.MFnTransform(self._dag)

	def translation(self, space = Space.WORLD):
		return self._fnTransform.translation(space)

	def setTranslation(self, vector, space = Space.WORLD):
		self._fnTransform.setTranslation(vector, space)

	def setName(self, name):
		self._fnTransform.setName(name)

class Dag(object):
	def __init__(self, name):
		self._dag = SelectionList.getDagPath(name)
		self._fnDagNode = om.MFnDagNode(self._dag)

	def addChild(self, childName):
		child = SelectionList.getDagPath(childName)
		self._fnDagNode.addChild(child, 0, False)










