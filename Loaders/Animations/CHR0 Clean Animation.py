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

def clean_chr0_animation(sender, event_args):
	# Show start prompt
	START_MSG = "Remove redundant keyframes within an interval of " + str(ACCEPTED_INTERVAL) + "\n\nTHIS PLUG-IN IS EXPERIMENTAL! Save back-ups of any affected files.\n\nPress OK to continue."
	
	if not BrawlAPI.ShowOKCancelWarning(START_MSG, SCRIPT_TITLE):
		return
	
	cleanCHR(BrawlAPI.SelectedNode, ACCEPTED_INTERVAL) # Lib function

# From CHR0 node
BrawlAPI.AddContextMenuItem(CHR0Wrapper, "", "Remove redundant keyframes from CHR0", EnableCheckCHR0, ToolStripMenuItem("Clean animation", None, clean_chr0_animation))

# From CHR0Entry node
BrawlAPI.AddContextMenuItem(CHR0EntryWrapper, "", "Remove redundant keyframes from CHR0", EnableCheckCHR0Entry, ToolStripMenuItem("Clean animation", None, clean_chr0_animation))
