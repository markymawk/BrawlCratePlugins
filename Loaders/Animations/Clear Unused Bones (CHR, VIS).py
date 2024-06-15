__author__ = "mawwwk"
__version__ = "1.0.2"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem

SCRIPT_NAME = "Clear Unused Bone Entries"

## Start enable check functions
# Wrapper: CHR0Wrapper, VIS0Wrapper
def EnableCheckANIM(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.Children)

## End enable check functions
## Start of main script

def clear_unused_bones(sender, event_args):
	# Get parent brres
	selNode = BrawlAPI.SelectedNode
	brresNode = BrawlAPI.SelectedNode.Parent.Parent
	allBoneNames = []
	entriesToDelete = []
	
	modelsGroup = brresNode.FindChild(MDL_GROUP)
	
	if not modelsGroup:
		BrawlAPI.ShowMessage("No models found in this BRRES. No entries removed.")
		return
	
	# Populate list of all bones
	for mdl0 in modelsGroup.Children:
		bonesGroup = mdl0.FindChild("Bones")
		
		if not bonesGroup:
			continue
		
		for bone in bonesGroup.GetChildrenRecursive():
			allBoneNames.append(bone.Name)
	
	# Populate list of unused bone references in anim
	for animEntry in selNode.Children:
		if animEntry.Name not in allBoneNames:
			entriesToDelete.append(animEntry)
	
	# Dialog box confirming list of names to delete, if any
	unusedCount = len(entriesToDelete)
	if unusedCount:
		msg = str(unusedCount) + " unused bone entries found: \n\n"
		msg += listToString(entriesToDelete, 15)
		msg += "\nPress OK to delete."
		
		# If user selects OK, delete bones
		if BrawlAPI.ShowOKCancelPrompt(msg, SCRIPT_NAME):
			for b in reverseResourceList(bonesToDeleteList):
				b.Remove()
	
	# If no bones to delete
	else:
		BrawlAPI.ShowMessage("No unused bone entries found.", SCRIPT_NAME)

LONG_TEXT = "Clear any bone entries not used in this brres node"

BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", LONG_TEXT, EnableCheckANIM, ToolStripMenuItem("Clear unused entries", None, clear_unused_bones))
BrawlAPI.AddContextMenuItem(VIS0Wrapper, "", LONG_TEXT, EnableCheckANIM, ToolStripMenuItem("Clear unused entries", None, clear_unused_bones))