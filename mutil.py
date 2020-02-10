import maya.cmds as cmds
import maya.api.OpenMaya as om 

class SelectionList(object):
	@staticmethod
	def getDagPath(name):
		list_selection = om.MSelectionList()
		
		if type(name) == om.MObject:
			dagnode = om.MFnDagNode(name)
			return dagnode.getPath()

		list_selection.add(name)
		return list_selection.getDagPath(0)

	@staticmethod
	def getDependNode(name):
		list_selection = om.MSelectionList()
		list_selection.add(name)
		return list_selection.getDependNode(0)


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
		if type(vector) != om.MVector:
			vector = om.MVector(vector)

		self._fnTransform.setTranslation(vector, space)

	def eulerRotation(self, radians = False):
		rotation =  self._fnTransform.rotation(Space.WORLD, True).asEulerRotation().asVector()
		
		if radians == False:
			rotation = self.vectorRadiansToDegrees(rotation)

		return rotation
		

	def setEulerRotation(self, vector, radians = False):
		if radians == False:
			rotation = self.vectorDegreesToRadians(vector)

		eulerAngle = om.MEulerRotation(rotation, RotOrder.XYZ)
		self._fnTransform.setRotation(eulerAngle.asQuaternion(), Space.WORLD)

	def vectorRadiansToDegrees(self, vector):
		vector = om.MVector(vector)
		vector.x = om.MAngle(vector.x, unit = om.MAngle.kRadians).asDegrees()
		vector.y = om.MAngle(vector.y, unit = om.MAngle.kRadians).asDegrees()
		vector.z = om.MAngle(vector.z, unit = om.MAngle.kRadians).asDegrees()
		return om.MVector(vector)

	def vectorDegreesToRadians(self, vector):
		vector = om.MVector(vector)
		vector.x = om.MAngle(vector.x, unit = om.MAngle.kDegrees).asRadians()
		vector.y = om.MAngle(vector.y, unit = om.MAngle.kDegrees).asRadians()
		vector.z = om.MAngle(vector.z, unit = om.MAngle.kDegrees).asRadians()
		return om.MVector(vector)


class DagNode(object):
	def __init__(self, name):
		self._dag = SelectionList.getDagPath(name)
		self._fnDagNode = om.MFnDagNode(self._dag)

	def addChild(self, child):
		mobj = SelectionList.getDependNode(child)
		self._fnDagNode.addChild(mobj, 0, False)

	def setName(self, name):
		self._fnDagNode.setName(name)

	def getName(self):
		return self._fnDagNode.name()


	def getPath(self):
		return self._fnDagNode.getPath()









