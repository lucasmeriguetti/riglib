import maya.cmds as cmds
import maya.api.OpenMaya as om 

import riglib.mutil as mutil
reload (mutil)

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

			#create node
			mdagmod = om.MDagModifier()
			moChainJoint = mdagmod.createNode("joint")
			mdagmod.doIt()
		
			#set name
			dagNodeChainJoint = mutil.DagNode(moChainJoint)
			dagNodeChainJoint.setName(name)

			#align
			inputJointTransform = mutil.Transform(jnt)
			jointTransform = mutil.Transform(moChainJoint)	

			jointTransform.setTranslation(inputJointTransform.translation(), mutil.Space.WORLD)
			jointTransform.setEulerRotation(inputJointTransform.eulerRotation())

			self._joints.append(name)

			#################################
			#BUILD THE HIERARCHY


	def getJoints(self):
		return self._joints

	@classmethod
	def getChainCount(cls):
		return Chain._count

	@classmethod
	def resetCount(cls):
		Chain._count = 0
		return True



