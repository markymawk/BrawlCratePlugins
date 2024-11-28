__author__ = "mawwwk"
__version__ = "1.0"

from System.Windows.Forms import ToolStripMenuItem # Needed for all loaders
from BrawlCrate.NodeWrappers import *
from mawwwkLib import *

SCRIPT_TITLE = "Clean CHR0 Animation"

# Maximum value that a keyframe can differ by to be cleared
ACCEPTED_INTERVAL = 0.001

## Start enable check functions
# Wrapper: CHR0Wrapper
def EnableCheckCHR0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.HasChildren)

# Wrapper: CHR0EntryWrapper
def EnableCheckCHR0Entry(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None

## End enable check functions
## Start helper functions

def main(entry):
	frameCount = entry.Parent.FrameCount
	entry._generateTangents = False
	
	# Loop through CHR array indices (scale, rot, trans)
	for i in range(9):
		
		# Loop through frames
		for frameIndex in range(1, frameCount+1):
			keyframe = entry.GetKeyframe(i, frameIndex)
			
			# Ignore blank keyframes
			if keyframe == None:
				continue
			
			# Save value then remove it
			tangent = keyframe._tangent
			value = keyframe._value
			entry.RemoveKeyframe(i, frameIndex)
			
			blankValue = entry.GetFrameValue(i, frameIndex)
			minVal = blankValue - ACCEPTED_INTERVAL
			maxVal = blankValue + ACCEPTED_INTERVAL
			
			inRemovableRange = value >= minVal and value <= maxVal
			
			# If value differs too greatly, restore the keyframe value
			if not inRemovableRange:
				# Last true = don't regenerate tangents
				restoredKeyframe = entry.SetKeyframe(i, frameIndex, value, True)
				restoredKeyframe._tangent = tangent

def clean_chr0_animation(sender, event_args):
	# Show start prompt
	START_MSG = "Remove redundant keyframes within an interval of " + str(ACCEPTED_INTERVAL) + "\n\nTHIS PLUG-IN IS EXPERIMENTAL! Save back-ups of any affected files.\n\nPress OK to continue."
	
	if not BrawlAPI.ShowOKCancelWarning(START_MSG, SCRIPT_TITLE):
		return
	
	selNode = BrawlAPI.SelectedNode
	
	# If CHR0 node, run on each entry
	if isinstance(selNode, CHR0Node):
		for entry in selNode.Children:
			main(entry)
	else:
		main(selNode)

# From CHR0 node
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Remove redundant keyframes from CHR0", EnableCheckCHR0, ToolStripMenuItem("Clean animation", None, clean_chr0_animation))

# From CHR0Entry node
BrawlAPI.AddContextMenuItem(CHR0EntryWrapper, "", "Remove redundant keyframes from CHR0", EnableCheckCHR0Entry, ToolStripMenuItem("Clean animation", None, clean_chr0_animation))
