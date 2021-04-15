__author__ = "mawwwk"
__version__ = "0.9"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem

bonesNamesList = []

# Debug message
def message(msg):
	BrawlAPI.ShowMessage(msg, "DEBUG")

def EnableCheckANIM(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and len(BrawlAPI.SelectedNode.Children))

# Basic impl of list.reverse() to accommodate ResourceNode lists
def reverseResourceList(nodeList):
	nodeListReverse = []
	for i in nodeList:
		nodeListReverse.append(i)
	
	nodeListReverse.reverse()
	return nodeListReverse

# Given a ModelData brres, iterate through mdl0 and generate a list of bone names. Then (do stuff with CHRs)
def parseModelData(brres):
	# Iterate through models, populate bonesNamesList
	modelsGroup = getModelsGroup(brres)
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
				parseMDL0(mdl0)
	
# Given a mdl0 node, delete any unused materials, then log any texture references
def parseMDL0(mdl0):
	bonesGroup = getModelBonesGroup(mdl0)
	
	if bonesGroup:
		# Iterate through bones in mdl0
		for b in bonesGroup.Children:
			addBoneName(b)

# Given a bone node inside a mdl0, add the bone name to bonesNamesList, and recursively call all children
def addBoneName(bone):
	bonesNamesList.append(bone.Name)
	if len(bone.Children):
		for b in bone.Children:
			#message(b.Name)debug
			addBoneName(b)

# Given a brres node, return its "3DModels" group. Return 0 if not found		
def getModelsGroup(brres):
	for group in brres.Children:
		if "3DModels" in group.Name:
			return group
	return 0

# Given a mdl0 node, return its "Bones" group. Return 0 if not found		
def getModelBonesGroup(mdl0):
	for group in mdl0.Children:
		if "Bones" in group.Name:
			return group
	return 0

############################################
########### Start of main script ###########
############################################
def clear_unused_bones(sender, event_args):
	# Get parent brres
	THIS_ANIM = BrawlAPI.SelectedNode
	PARENT_BRRES = BrawlAPI.SelectedNode.Parent.Parent
	bonesToDeleteList = []
	
	# Populate lists of used textures, and delete any unused materials
	parseModelData(PARENT_BRRES)
	
	# Gather list of bone references in chr0 that aren't in bonesNamesList
	for bone in THIS_ANIM.Children:
		if bone.Name not in bonesNamesList:
			bonesToDeleteList.append(bone)
	
	doClearBones = (len(bonesToDeleteList) > 0)
	
	# Dialog box confirming list of names to delete, if any
	if len(bonesToDeleteList) > 0:
		msg = str(len(bonesToDeleteList)) + " unused entries found: \n\n"
		for b in bonesToDeleteList:
			msg += b.Name + "\n"
		msg += "\nPress OK to delete."
		doClearBones = BrawlAPI.ShowOKCancelPrompt(msg, "Clear Unused Entries")
	else:
		BrawlAPI.ShowMessage("No unused bone entries found", "Clear Unused Entries")
	
	# If clearing bones, reverse list, then delete them
	if doClearBones:
		bonesToDeleteList = reverseResourceList(bonesToDeleteList)
		for b in bonesToDeleteList:
			b.Remove()
		#BrawlAPI.ShowMessage("Unused bone entries deleted", "Success")
	
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Clear any bones not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_bones))

# Originally wrote this for CHR0s but it works perfectly for VIS0s too (i think)
BrawlAPI.AddContextMenuItem(VIS0Wrapper, "", "Clear any bones not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_bones))