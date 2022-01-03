__author__ = "mawwwk"
__version__ = "1.0.1"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem

materialsNamesList = []

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

# Given a ModelData brres, iterate through mdl0s
def parseModelData(brres):
	# Iterate through models to populate materialsNamesList
	modelsGroup = getChildFromName(brres, "3DModels")
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			parseMDL0(mdl0)
	
# Given a mdl0 node, iterate through materials and add to materialsNamesList[]
def parseMDL0(mdl0):
	materialsGroup = getChildFromName(mdl0, "Materials")
	
	if materialsGroup:
		# Iterate through bones in mdl0
		for m in materialsGroup.Children:
			materialsNamesList.append(m.Name)

## End of helper methods
## Start of main script

def clear_unused_mats(sender, event_args):
	# Get parent brres
	THIS_ANIM = BrawlAPI.SelectedNode
	PARENT_BRRES = BrawlAPI.SelectedNode.Parent.Parent
	entriesToDeleteList = []
	
	# Populate materialsNamesList[] with used mats
	parseModelData(PARENT_BRRES)
	
	# Gather list of bone references in chr0 that aren't in bonesNamesList
	for m in THIS_ANIM.Children:
		if m.Name not in materialsNamesList:
			entriesToDeleteList.append(m)
	
	# Dialog box confirming list of names to delete, if any
	if len(entriesToDeleteList) > 0:
		msg = str(len(entriesToDeleteList)) + " unused material entries found: \n\n"
		for m in entriesToDeleteList:
			msg += m.Name + "\n"
		msg += "\nPress OK to delete."
		
		# If user selects OK, delete mats
		if BrawlAPI.ShowOKCancelPrompt(msg, "Clear Unused Material Entries"):
			for m in reverseResourceList(entriesToDeleteList):
				m.Remove()
	# If no mats to delete
	else:	
		BrawlAPI.ShowMessage("No unused material entries found", "Clear Unused Entries")
	
BrawlAPI.AddContextMenuItem(SRT0Wrapper, "", "Clear any materials not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_mats))
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Clear any materials not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_mats))
BrawlAPI.AddContextMenuItem(PAT0Wrapper, "", "Clear any materials not found in the brres", EnableCheckANIM, ToolStripMenuItem("Clear Unused Entries", None, clear_unused_mats))