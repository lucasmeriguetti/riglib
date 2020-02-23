import maya.cmds as cmds 

def deleteSceneNodes():
	selection =  cmds.ls(transforms = True, v = True)
	if len(selection) > 0:
		cmds.delete(cmds.ls(transforms = True, v = True))

def createSceneJoints():
	joints = []
	for i in range(5):
		jnt = cmds.joint(name = "joint_{}".format(i), 
			position = [0,i,0] )

		joints.append(jnt)

	cmds.select(cl = True)

	return joints