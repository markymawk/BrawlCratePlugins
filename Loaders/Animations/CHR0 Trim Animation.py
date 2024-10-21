__author__ = "mawwwk"
__version__ = "1.0.1"

from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_TITLE = "Trim CHR0 Animation"

## Start enable check functions
# Wrapper: CHR0Wrapper
def EnableCheckCHR0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.HasChildren and node.FrameCount > 1)

# Wrapper: CHR0EntryWrapper
def EnableCheckCHR0Entry(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.Parent and node.Parent.FrameCount > 1)

## End enable check functions
## Start helper functions

# Move keyframe and force-include empty non-set values
def forceMoveKeyframe(chr0Entry, newIndex, originalIndex):
	# Loop through scale, rot, trans
	for i in range(9):
		value = chr0Entry.GetFrameValue(i, originalIndex)
		chr0Entry.SetKeyframe(i, newIndex, value)

# Move keyframe while ignoring empty values
def moveKeyframe(chr0Entry, newIndex, originalIndex):
	# Loop through scale, rot, trans
	for i in range(9):
		value = chr0Entry.GetKeyframe(i, originalIndex)
		if value is None:
			continue
		# If set, then assign at new frame index
		chr0Entry.SetKeyframe(i, newIndex, value._value)
		
		# Update tangent
		tangent = value._tangent
		newFrame = chr0Entry.GetKeyframe(i, newIndex)
		newFrame._tangent = tangent	

## End helper functions
## Start loader functions

# Base loader function (parent chr0 node)
def trim_chr(sender, event_args):
	main(BrawlAPI.SelectedNode)

# Base loader function (child chr0 entry node)
def trim_chr_entry(sender, event_args):
	main(BrawlAPI.SelectedNode.Parent)

# Main function
def main(chr0Node):
	selNodeFrameCount = chr0Node.FrameCount
	
	# Prompt for starting frame index
	startFrame = BrawlAPI.UserStringInput("Enter starting frame")
	if not startFrame:
		return
	
	startFrame = int(startFrame)
	if startFrame not in range (1, selNodeFrameCount):
		BrawlAPI.ShowMessage("Input out of range or invalid", SCRIPT_TITLE)
		return
	
	# Prompt for ending frame index
	endFrame = BrawlAPI.UserStringInput("Enter ending frame")
	if not endFrame:
		return
	
	endFrame = int(endFrame)
	if endFrame not in range (1, selNodeFrameCount) or endFrame < startFrame:
		BrawlAPI.ShowMessage("Input out of range or invalid", SCRIPT_TITLE)
		return
	
	# Subtract 1 to match zero-indexed syntax
	startFrame = startFrame - 1
	endFrame = endFrame - 1
	newFrameCount = endFrame - startFrame
	
	# Loop through chr0 entries
	for chr0Entry in chr0Node.Children:
		# Assume animation is static until multiple frames are set
		
		isStaticAnimation = True
		# Set first frame manually
		forceMoveKeyframe(chr0Entry, 0, startFrame)
		
		# Start animation trim
		for i in range(1, newFrameCount):
			newFrame = chr0Entry.GetAnimFrame(startFrame+i, True)
			
			# If source keyframe is empty, set empty keyframe in new spot
			if not newFrame.HasKeys:
				chr0Entry.RemoveKeyframe(i)
			
			# If not empty, copy values
			else:
				isStaticAnimation = False
				moveKeyframe(chr0Entry, i, startFrame+i)
		
		# Set final frame manually
		if not isStaticAnimation:
			forceMoveKeyframe(chr0Entry, newFrameCount-1, endFrame)
	
	# Update CHR0 FrameCount value
	chr0Node.FrameCount = newFrameCount
	
	# Results
	msg = "CHR " + chr0Node.Name + " trimmed from frames " + str(startFrame+1) + "-" + str(endFrame+1) + "."
	BrawlAPI.ShowMessage(msg, "")

## End loader functions
## Start context menu add

LONG_TEXT = "Trim CHR animation to given start and end frame"
SHORT_TEXT = "Trim to..."

BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", LONG_TEXT, EnableCheckCHR0, ToolStripMenuItem(SHORT_TEXT, None, trim_chr))
BrawlAPI.AddContextMenuItem(CHR0EntryWrapper, "", LONG_TEXT, EnableCheckCHR0Entry, ToolStripMenuItem(SHORT_TEXT, None, trim_chr_entry))