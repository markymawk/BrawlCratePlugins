__author__ = "mawwwk"
__version__ = "0.9"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem

materialsNamesList = []

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
	# Iterate through models, populate materialsNamesList
	modelsGroup = getModelsGroup(brres)
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
				parseMDL0(mdl0)
	
# Given a mdl0 node, delete any unused materials, then log any texture references
def parseMDL0(mdl0):
	materialsGroup = getModelMaterialsGroup(mdl0)
	
	if materialsGroup:
		# Iterate through bones in mdl0
		for m in materialsGroup.Children:
			materialsNamesList.append(m.Name)
	
# Given a brres node, return its "3DModels" group. Return 0 if not found		
def getModelsGroup(brres):
	for group in brres.Children:
		if "3DModels" in group.Name:
			return group
	return 0

# Given a mdl0 node, return its "Bones" group. Return 0 if not found		
def getModelMaterialsGroup(mdl0):
	for group in mdl0.Children:
		if "Materials" in group.Name:
			return group
	return 0

############################################
########### Start of main script ###########
############################################
def clear_unused_bones(sender, event_args):
	# Get parent brres
	THIS_ANIM = BrawlAPI.SelectedNode
	PARENT_BRRES = BrawlAPI.SelectedNode.Parent.Parent
	entriesToDeleteList = []
	
	# Populate lists of used textures, and delete any unused materials
	parseModelData(PARENT_BRRES)
	
	# Gather list of bone references in chr0 that aren't in bonesNamesList
	for m in THIS_ANIM.Children:
		if m.Name not in materialsNamesList:
			entriesToDeleteList.append(m)
	
	doClearMats = (len(entriesToDeleteList) > 0)
	
	# Dialog box confirming list of names to delete, if any
	if doClearMats:
		msg = str(len(entriesToDeleteList)) + " unused entries found: \n\n"
		for m in entriesToDeleteList:
			msg += m.Name + "\n"
		msg += "\nPress OK to delete."
		doClearMats = BrawlAPI.ShowOKCancelPrompt(msg, "Clear Unused Entries")
	else:
		BrawlAPI.ShowMessage("No unused bone entries found", "Clear Unused Entries")
	
	# If clearing bones, reverse list, then delete them
	if doClearMats:
		entriesToDeleteList = reverseResourceList(entriesToDeleteList)
		for m in entriesToDeleteList:
			m.Remove()
		#BrawlAPI.ShowMessage("Unused bone entries deleted", "Success")
	
BrawlAPI.AddContextMenuItem(SRT0Wrapper, "", "Clear any materials not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_bones))
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Clear any materials not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_bones))
BrawlAPI.AddContextMenuItem(PAT0Wrapper, "", "Clear any materials not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_bones))