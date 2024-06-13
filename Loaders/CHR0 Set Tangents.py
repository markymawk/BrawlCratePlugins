__author__ = "mawwwk"
__version__ = "1.0.1"

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

def set_tangents_chr0(sender, event_args):
	node = BrawlAPI.SelectedNode
	newTangent = tangentPrompt()
	if newTangent == None:
		return
	
	# Loop through child nodes
	for i in node.Children:
		setTangents(i, newTangent)
	
	# Results
	BrawlAPI.ShowMessage("All tangents in " + node.Name + " set to " + str(newTangent), SCRIPT_TITLE)

def set_tangents_chr0entry(sender, event_args):
	node = BrawlAPI.SelectedNode
	newTangent = tangentPrompt()
	if newTangent == None:
		return
	
	# Set tangents for selected CHR0Entry only
	setTangents(node, newTangent)
	
	# Results
	BrawlAPI.ShowMessage("All tangents in " + node.Name + " set to " + str(newTangent), SCRIPT_TITLE)

## End loader functions
## Start main function

def setTangents(node, newTangent):
	for k in range(node.FrameCount):
	
		# Loop through scale, rotation, translation
		for i in range (0, 9):
			frame = node.GetKeyframe(i, k)
			
			# If keyframe is empty, skip
			if "None" in str(type(frame)):
				continue
			frame._tangent = newTangent
	
	# Mark file as changed
	node.IsDirty = True

## End main function

## Start context menu add

# From CHR0 node
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Set animation tangents to a given value", EnableCheckCHR0, ToolStripMenuItem("Set tangents to...", None, set_tangents_chr0))

# From CHR0Entry node
BrawlAPI.AddContextMenuItem(CHR0EntryWrapper, "", "Set animation tangents to a given value", EnableCheckCHR0Entry, ToolStripMenuItem("Set tangents to...", None, set_tangents_chr0entry))