import maya.cmds as cmds 
import maya.api.OpenMaya as om 

import riglib.chain 
reload(riglib.chain)
from riglib.chain import Chain 

import riglib.mutil as mutil 
reload (mutil)

class Rigger(Chain):

	def __init__(self, chain, name = "DefaultRigger"):
		self._chain = chain 
		self._name  = name

		super(Rigger, self).__init__(joints = self._chain.getJoints(), name = self._name)
		self.addWeightAttrToChain()
		self.connectWeightAttrToChainConstraint()

	def getChain(self):
		return self._chain

	def addWeightAttrToChain(self):
		chainContainer = self._chain.getContainer()
		chainContainer.addAttr(self._name, self._name)

	def connectWeightAttrToChainConstraint(self):
		pass

