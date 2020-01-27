import maya.cmds as cmds
import maya.api.OpenMaya as om 

class SelectionList(object):
	@staticmethod
	def getDagPath(name):
		list_selection = om.MSelectionList()
		if type(name) == om.MObject:
			dagnode = om.MFnDagNode(name)
			name = dagnode.getPath()

		list_selection.add(name)
		return list_selection.getDagPath(0)

class Space(object):
	WORLD = om.MSpace.kWorld
	OBJECT = om.MSpace.kObject
	TRANSFORM = om.MSpace.kTransform

class RotOrder(object):
	XYZ = om.MEulerRotation.kXYZ
	YXZ = om.MEulerRotation.kYXZ
	ZXY = om.MEulerRotation.kZXY
	ZYX = om.MEulerRotation.kZYX
	YZX = om.MEulerRotation.kYZX
	XZY = om.MEulerRotation.kXZY

class Transform(object):
	def __init__(self, name):
		self._dag = SelectionList.getDagPath(name)
		self._fnTransform = om.MFnTransform(self._dag)

	def translation(self, space = Space.WORLD):
		return self._fnTransform.translation(space)

	def setTranslation(self, vector, space = Space.WORLD):
		self._fnTransform.setTranslation(vector, space)

	def eulerRotation(self):
		return self._fnTransform.rotation(Space.WORLD, False).asVector()

	def setEulerRotation(self, vector):
		self._fnTransform.setRotation(om.MEulerRotation(vector, RotOrder.XYZ), Space.WORLD)


class DagNode(object):
	def __init__(self, name):
		self._dag = SelectionList.getDagPath(name)
		self._fnDagNode = om.MFnDagNode(self._dag)

	def addChild(self, childName):
		child = SelectionList.getDagPath(childName)
		self._fnDagNode.addChild(child, 0, False)

	def setName(self, name):
		self._fnDagNode.setName(name)










