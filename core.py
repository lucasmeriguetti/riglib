import maya.cmds as cmds
import maya.api.OpenMaya as om 

import riglib.mautil as mautil
reload (mautil)

class Chain(object):
	_count = 0
	
	def __init__(self, joints = [], name = "DefaultChain"):
		Chain._count += 1
		self._name = "{}_{}".format(name, Chain._count)
		self._inputJoints = joints
		self._joints = []

		self.createChainJoints()

	def createChainJoints(self):
		""" Create chain joints from input joints"""
		for i, jnt in enumerate(self._inputJoints):
			name ="{}_joint_{}".format(self._name, i)
			
			#get input joint position
			mvec = mautil.Transform(jnt).translation()

			#create node
			mdagmod = om.MDagModifier()
			mobj = mdagmod.createNode("joint")
			mdagmod.doIt()
	
			joint = mautil.Transform(om.MFnDagNode(mobj).getPath())	
			joint.setName(name)
			joint.setTranslation(mvec, mautil.Space.WORLD)

			self._joints.append(name)

		for jnt, i in enumerate(self._joints):
			#BUILD HIERARCHY
			pass


	def getJoints(self):
		return self._joints

	@classmethod
	def getChainCount(cls):
		return Chain._count

	@classmethod
	def resetCount(cls):
		Chain._count = 0
		return True



