import maya.cmds as cmds
import maya.api.OpenMaya as om 

import riglib.mutil as mutil
reload (mutil)

class Chain(object):
	_count = 0
	
	def __init__(self, joints = [], name = "DefaultChain"):
		self._name = "i{}_{}".format(self.__class__._count, name)
		self._inputJoints = joints
		self._joints = []
		self._parentConstraint = []
		self._scaleConstraint = []
		self._chainGroup = None
		self._chainOffsetGroup = None

		self.createJoints()
		self.constraintInputJoints()
		self.createContainer()

		self.__class__._count += 1

	def getName(self):
		return self._name

	def getWeightAlias(self, constraintName = None):
		if cmds.objectType(constraintName) == "parentConstraint":
			return cmds.parentConstraint(constraintName, 
				query = True, weightAliasList = True)

		if cmds.objectType(constraintName) == "scaleConstraint":
			return cmds.scaleConstraint(constraintName, 
				query = True, weightAliasList = True)

	def createContainer(self):
		self._chainGroup = mutil.DagNode.create("transform", 
			name = "{}_Grp".format(self._name))

		self._chainOffsetGroup = mutil.DagNode.create("transform", 
			name = "{}_Offset_Grp".format(self._name))

		self._chainGroup.addChild(self._chainOffsetGroup)
		self._chainOffsetGroup.addChild(self._joints[0])

	def getContainer(self, offset = False):
		if offset:
			return self._chainOffsetGroup

		return self._chainGroup

	def createJoints(self):
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
			jointTransform.setTranslation(inputJointTransform.getTranslation(), mutil.Space.WORLD)
			jointTransform.setRotation(inputJointTransform.getRotation())

			self._joints.append(name)

	def constraintInputJoints(self):
		for i, j in zip(self._inputJoints, self._joints):
			self._parentConstraint.append(cmds.parentConstraint(j, i, name = "{}_parentConstraint".format(j))[0])
		
		for i, j in zip(self._inputJoints, self._joints):
			self._scaleConstraint.append(cmds.scaleConstraint(j, i, name = "{}_scaleConstraint".format(j))[0])

	def getScaleConstraints(self, index = None):
		if index != None:
			return self._scaleConstraint[index]

		return self._scaleConstraint

	def getParentConstraints(self, index = None):
		if index != None:
			return self._parentConstraint[index]
		return self._parentConstraint

	def getJoints(self):
		return self._joints

	@classmethod
	def getCount(cls):
		return cls._count

	@classmethod
	def resetCount(cls):
		cls._count = 0



