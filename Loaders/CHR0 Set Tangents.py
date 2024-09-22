__author__ = "mawwwk"
__version__ = "2.0"

from System.Windows.Forms import ToolStripMenuItem # Needed for all loaders
from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from mawwwkLib import *

SCRIPT_TITLE = "Set Tangents"

## Start enable check functions
# Wrapper: MDL0Wrapper
def EnableCheckCHR0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.HasChildren)

def EnableCheckCHR0Entry(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None

## End enable check functions
## Start helper functions

def tangentPrompt():
	newTangent = BrawlAPI.UserStringInput("Enter new tangent value")
	if newTangent == "None" or newTangent == "" or newTangent == None:
		return None
	return float(newTangent)

## End helper functions
## Start loader functions

def set_tangents(sender, event_args):
	node = BrawlAPI.SelectedNode
	newTangent = tangentPrompt()
	if newTangent == None:
		return
	
	# Use Lib function
	setAllTangents(node, newTangent)
	
	# Results
	BrawlAPI.ShowMessage("All tangents in " + node.Name + " set to " + str(newTangent), SCRIPT_TITLE)

## End loader functions
## Start context menu add

# From CHR0 node
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Set animation tangents to a given value", EnableCheckCHR0, ToolStripMenuItem("Set tangents to...", None, set_tangents))

# From CHR0Entry node
BrawlAPI.AddContextMenuItem(CHR0EntryWrapper, "", "Set animation tangents to a given value", EnableCheckCHR0Entry, ToolStripMenuItem("Set tangents to...", None, set_tangents))