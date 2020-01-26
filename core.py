import maya.cmds as cmds
import maya.api.OpenMaya as om 

import riglib.mautil
reload (riglib.mautil)

from riglib.mautil import SelectionList, Transform

class Chain(object):
	_count = 0
	
	def __init__(self, joints = [], name = "DefaultChain"):
		Chain._count += 1
		self._name = "{}_{}".format(name, Chain._count)
		self._inputJoints = joints
		self._joints = []

		self.createChainJoints()

	def createChainJoints(self):
		"""Duplicate and constraint to input joints"""
		for i, j in enumerate(self._inputJoints):
			#get joint position
			mvec = Transform(j).translation()
			posAxes = mvec.x, mvec.y, mvec.z
			joint = cmds.joint(name = "{}_{}".format(self._name, i), position = posAxes )
			self._joints.append(joint)

	def getJoints(self):
		return self._joints

	@classmethod
	def getChainCount(cls):
		return Chain._count

	@classmethod
	def resetCount(cls):
		Chain._count = 0
		return True



