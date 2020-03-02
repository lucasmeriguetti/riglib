import maya.cmds as cmds 
import maya.api.OpenMaya as om 

import riglib.chain 
reload(riglib.chain)
from riglib.chain import Chain 

import riglib.mutil as mutil 
reload (mutil)

class Rigger(Chain):
	def __init__(self, chain, name = "DefaultRigger", weightAttr = 1):
		self._chain = chain 
		self._weightAttr = weightAttr;

		super(Rigger, self).__init__(joints = self._chain.getJoints(), name = name)
		self.addWeightAttrToChain()
		self.connectWeightAttrToConstraints()
		Rigger._count += 1

	def getChain(self):
		return self._chain

	def addWeightAttrToChain(self):
		chainContainer = self._chain.getContainer()
		chainContainer.addAttr(self._name, self._name)

	def connectWeightAttrToConstraints(self):
		#get constraint with rigger name 
		##connect attributes 
		chainContainer = self._chain.getContainer()
		sourceAttrName = self._name
		
		for pConst, sConst in zip(self.getParentConstraints(), self.getScaleConstraints()):
			for pW, sW in zip(self.getWeightAlias(pConst), self.getWeightAlias(sConst)):
				if self._name in pW:
					chainContainer.connect(sourceAttrName, pConst, pW)

				if self._name in pW:
					chainContainer.connect(sourceAttrName, sConst, sW)

	def setRiggerWeightAttr(self, value):
		STILL NEED TO TEST IT 
		self._chain.getContainer().setAttr(self._name, value)

