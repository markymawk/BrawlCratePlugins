__author__ = "mawwwk"
__version__ = "1.0.3"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Clear Unused Material Entries"

def EnableCheckANIM(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.HasChildren)

def clear_unused_mats(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	brresNode = selNode.Parent.Parent
	allMaterialNames = []
	entriesToDelete = []
	
	modelsGroup = brresNode.FindChild(MDL_GROUP)
	
	if not modelsGroup:
		BrawlAPI.ShowMessage("No models found in this BRRES. No entries removed.")
		return
	
	# Populate allMaterialNames[]
	for mdl0 in modelsGroup.Children:
		matsGroup = mdl0.FindChild("Materials")
		if matsGroup:
			for mat in matsGroup.Children:
				allMaterialNames.append(mat.Name)
	
	# Populate list of unused animation entries
	for mat in selNode.Children:
		if mat.Name not in allMaterialNames:
			entriesToDelete.append(mat)
	
	# Dialog box confirming list of names to delete, if any
	unusedCount = len(entriesToDelete)
	if unusedCount:
		msg = str(unusedCount) + " unused material entries found: \n\n"
		msg += listToString(entriesToDelete, 15)
		msg += "\nPress OK to delete."
		
		# If user selects OK, delete mats
		if BrawlAPI.ShowOKCancelPrompt(msg, SCRIPT_NAME):
			for m in reverseResourceList(entriesToDelete):
				m.Remove()
	
	# If no mats to delete
	else:	
		BrawlAPI.ShowMessage("No unused material entries found.", SCRIPT_NAME)

LONG_TEXT = "Clear any material entries unused in this brres node"
BrawlAPI.AddContextMenuItem(SRT0Wrapper, "", LONG_TEXT, EnableCheckANIM, ToolStripMenuItem("Clear unused entries", None, clear_unused_mats))
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", LONG_TEXT, EnableCheckANIM, ToolStripMenuItem("Clear unused entries", None, clear_unused_mats))
BrawlAPI.AddContextMenuItem(PAT0Wrapper, "", LONG_TEXT, EnableCheckANIM, ToolStripMenuItem("Clear unused entries", None, clear_unused_mats))