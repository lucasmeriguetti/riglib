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
		self._transform = om.MFnTransform(self._dag)

	def translation(self, space = Space.WORLD):
		return self._transform.translation(space)







