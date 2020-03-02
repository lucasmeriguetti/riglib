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

class NumData(object):
	data = om.MFnNumericData
	FLOAT = data.kFloat 
	DOUBLE = data.kDouble
	INT = data.kInt
	BOOL = data.kBoolean

	@classmethod
	def fromString(cls, numDataString):
		if "float":
			return NumData.FLOAT

		if "double":
			return NumData.DOUBLE

		if "int":
			return NumData.INT 

		if "bool":
			return NumData.BOOL

class DagNode(object):
	def __init__(self, name):
		if type(name) == type(self):
			self = name

		else:
			self._dag = SelectionList.getDagPath(name)
			self._mobj = SelectionList.getDependNode(name)

		self._fnDagNode = om.MFnDagNode(self._dag)
		self._fnNumAttr = om.MFnNumericAttribute()

	def addChild(self, child):
		if type(child) == type(self):
			child = child.getName()

		mobj = SelectionList.getDependNode(child)
		self._fnDagNode.addChild(mobj, 0, False)

	def setName(self, name):
		self._fnDagNode.setName(name)

	def getName(self):
		return self._fnDagNode.name()

	def getPath(self):
		return self._fnDagNode.getPath()

	def getMObject(self):
		return self._fnDagNode.object()

	def listAttr(self):
		pass

	def setAttr(self, attribute, value):
		if not self.attributeExists(attribute):
			return cmds.error("Attribute does not exist.")

		mplug = self.findPlug(attribute)
		mplug.setFloat(value)

	def getAttr(self, attribute):
		if not self.attributeExists(attribute):
			return cmds.error("Attribute does not exist.")

		mplug = self.findPlug(attribute)
		return mplug.asFloat()

	def attributeExists(self, attribute):
		if self._fnDagNode.hasAttribute(attribute):
			return True 

		return False 
		
	def addAttr(self,longName = None, shortName = None, 
		type = "float", maxValue = 1.0,	minValue = 0.0,
		defaultValue = 0.0,	keyable = True	):

		if shortName == None:
			shortName = longName

		attr = self._fnNumAttr.create(longName, shortName, NumData.fromString(type))
		
		if keyable:
			self._fnNumAttr.keyable = True

		self._fnNumAttr.setMax(maxValue)
		self._fnNumAttr.setMin(minValue)
		self._fnNumAttr.default = defaultValue
		self._fnDagNode.addAttribute(attr)

	def connect(self, sourceAttr, destObject, destAttr):

		if isinstance(destObject, DagNode):
			destObject = destObject.getMObject()

		if isinstance(destObject, basestring):
		 	destObject = SelectionList.getDependNode(destObject)

		mfndep = om.MFnDependencyNode(destObject)
		destAttr = mfndep.attribute(destAttr)

		sourceAttr = self._fnDagNode.attribute(sourceAttr)

		mdgmod = om.MDGModifier()
		mdgmod.connect(self.getMObject(), sourceAttr, destObject, destAttr)
		mdgmod.doIt()

	def findPlug(self, plugName):
		return self._fnDagNode.findPlug(plugName, True)

	@staticmethod
	def create(dagtype = "transform", name = "default"):
		mdagmod = om.MDagModifier()
		mobj = mdagmod.createNode(dagtype)
		mdagmod.doIt()

		dagnode = DagNode(mobj)
		dagnode.setName(name)
		return dagnode







