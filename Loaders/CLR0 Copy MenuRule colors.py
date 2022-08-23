__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Copy MenuRule colors"

## Start enable check functions
# Wrapper: CLR0Wrapper
def EnableCheckCLR0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and "MenMainIcon0" in node.Name \
	and node.Parent and node.Parent.Parent \
	and node.Parent.Parent.Parent \
	and "MenuRule_" in node.Parent.Parent.Parent.Name)

## End enable check functions
## Start loader functions

def menurule_color_copy(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	CLR0_SUFFIX = selNode.Name[-3:]
	
	nodesToChange = []
	for node in selNode.Parent.Children:	
		if node.Name.startswith("MenMainIcon0") and node.Name.endswith(CLR0_SUFFIX):
			nodesToChange.append(node)
	
	msg = "Copying the selected animation to " + str(len(nodesToChange))
	msg += " CLR animations ending in " + CLR0_SUFFIX + "\n\nPress OK to continue."
	
	if not showMsg(msg, SCRIPT_NAME, 1):
		return
	
	for node in nodesToChange:
		node.Replace(selNode)
	
## End loader functions
## Start context menu add

# Reset frequency
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Copy this CLR animation to its matching nodes", EnableCheckCLR0, ToolStripMenuItem("Copy MenuRule colors", None, menurule_color_copy))
