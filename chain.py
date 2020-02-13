import maya.cmds as cmds
import maya.api.OpenMaya as om 

import riglib.mutil as mutil
reload (mutil)

class Chain(object):
	_count = 0
	
	def __init__(self, joints = [], name = "DefaultChain"):
		self._name = "{}_{}".format(name, Chain._count)
		self._inputJoints = joints
		self._joints = []
		self._parentConstraint = []
		self._scaleConstraint = []

		self.createChainJoints()

		self.constraintInputJoints()

		Chain._count += 1
		
	def createChainGroup(self):
		Dag

	def createChainJoints(self):
		""" Create chain joints from input joints"""
		for i, jnt in enumerate(self._inputJoints):
			name ="{}_joint_{}".format(self._name, i)

			#set name
			dagNodeChainJoint = mutil.DagNode.create("joint", name)

			#hierarchy
			if i > 0:
				parentDagNode.addChild(dagNodeChainJoint)

			parentDagNode = dagNodeChainJoint

			#align
			inputJointTransform = mutil.Transform(jnt)
			jointTransform = mutil.Transform(dagNodeChainJoint.getPath())	
			jointTransform.setTranslation(inputJointTransform.translation(), mutil.Space.WORLD)
			jointTransform.setEulerRotation(inputJointTransform.eulerRotation())

			self._joints.append(name)

	def constraintInputJoints(self):
		for i, j in zip(self._inputJoints, self._joints):
			self._parentConstraint.append(cmds.parentConstraint(j, i, name = "{}_parentConstraint".format(j))[0])
		
		for i, j in zip(self._inputJoints, self._joints):
			self._scaleConstraint.append(cmds.scaleConstraint(j, i, name = "{}_scaleConstraint".format(j))[0])

	def getScaleConstraints(self):
		return self._scaleConstraint

	def getParentConstraints(self):
		return self._parentConstraint

	def getJoints(self):
		return self._joints

	@classmethod
	def getChainCount(cls):
		return Chain._count

	@classmethod
	def resetCount(cls):
		Chain._count = 0
		return True


