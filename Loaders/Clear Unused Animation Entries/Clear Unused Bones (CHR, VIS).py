__author__ = "mawwwk"
__version__ = "1.0.1"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem

bonesNamesList = []

# Returns child node whose name contains the given nameStr
def getChildFromName(node, nameStr):
	if node.Children:
		for child in node.Children:
			if str(nameStr) in child.Name:
				return child
	return 0	# If not found, return 0

def EnableCheckANIM(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and len(BrawlAPI.SelectedNode.Children))

# Basic impl of list.reverse() to accommodate ResourceNode lists
def reverseResourceList(nodeList):
	nodeListReverse = []
	for i in nodeList:
		nodeListReverse.append(i)
	
	nodeListReverse.reverse()
	return nodeListReverse

# Given a ModelData brres, iterate through mdl0 and generate a list of bone names
def parseModelData(brres):
	# Iterate through models, populate bonesNamesList[]
	modelsGroup = getChildFromName(brres, "3DModels")
	
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			parseMDL0(mdl0)
	
# Given a mdl0 node, iterate through bones
def parseMDL0(mdl0):
	bonesGroup = getChildFromName(mdl0, "Bones")
	
	if bonesGroup:
		# Iterate through bones in mdl0
		for b in bonesGroup.Children:
			addBoneName(b)

# Given a bone node inside a mdl0, add the bone name to bonesNamesList[], and recursively call all children
def addBoneName(bone):
	bonesNamesList.append(bone.Name)
	if len(bone.Children):
		for b in bone.Children:
			#message(b.Name)debug
			addBoneName(b)

## End of helper methods
## Start of main script

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
	
	# Dialog box confirming list of names to delete, if any
	if len(bonesToDeleteList) > 0:
		msg = str(len(bonesToDeleteList)) + " unused bone entries found: \n\n"
		for b in bonesToDeleteList:
			msg += b.Name + "\n"
		msg += "\nPress OK to delete."
		
		# If user selects OK, delete bones
		if BrawlAPI.ShowOKCancelPrompt(msg, "Clear Unused Bone Entries"):
			for b in reverseResourceList(bonesToDeleteList):
				b.Remove()
	# If no bones to delete
	else:
		BrawlAPI.ShowMessage("No unused bone entries found", "Clear Unused Entries")
	
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Clear any bones not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_bones))

BrawlAPI.AddContextMenuItem(VIS0Wrapper, "", "Clear any bones not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_bones))