import maya.cmds

class Chain(object):
	_count = 0
	
	def __init__(self, joints = None):
		Chain._count += 1
		self._input_joints = joints
		self._joints = []

	def duplicate_input_joints(self):
		pass 

	@staticmethod
	def get_chain_count():
		return Chain._count

	@staticmethod
	def reset_count():
		Chain._count = 0
		return True



