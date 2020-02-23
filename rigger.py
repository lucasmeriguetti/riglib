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
		super(Rigger, self).__init__(joints = self._chain.getJoints(), name = name)

	def addWeightAttrToChain(self):
		pass 
