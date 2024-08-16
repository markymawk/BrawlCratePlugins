__author__ = "mawwwk"
__version__ = "1.1"

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
	# Loop through scale, rotation, translation
	for i in range (9):
		for k in range(node.FrameCount):
			
			# Don't change tangents for 1-frame animations
			isMultipleFrames = False
			
			frame = node.GetKeyframe(i, k)
			
			# If keyframe is empty, skip
			if "None" in str(type(frame)):
				continue
			
			# Store tangent of first frame
			if k == 0:
				frame0Tangent = frame._tangent
			
			isMultipleFrames = (k > 0)
			frame._tangent = newTangent
		
		# If only 1 frame in the animation, restore its original tangent
		firstFrame = node.GetKeyframe(i, 0)
		if not isMultipleFrames and firstFrame:
			firstFrame._tangent = frame0Tangent
	
	node.IsDirty = True

## End main function
## Start context menu add

# From CHR0 node
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Set animation tangents to a given value", EnableCheckCHR0, ToolStripMenuItem("Set tangents to...", None, set_tangents_chr0))

# From CHR0Entry node
BrawlAPI.AddContextMenuItem(CHR0EntryWrapper, "", "Set animation tangents to a given value", EnableCheckCHR0Entry, ToolStripMenuItem("Set tangents to...", None, set_tangents_chr0entry))