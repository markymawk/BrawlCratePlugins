__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import File
from mawwwkLib import *

FILL_COLOR_NAMES = [
 "AGameWatch"
]

BORDER_COLOR_NAMES = [
 "BrdDSGameWatch",
 "BrdGameWatch",
 "BrdZOffDSGameWatch",
 "BrdZOffGameWatch"
]

## Start enable check functions
# Wrapper: CLR0MaterialWrapper
def EnableCheckGNWBorder(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Name in BORDER_COLOR_NAMES and node.HasChildren and node.Children[0].Name == "ColorRegister0")

# Wrapper: CLR0MaterialWrapper
def EnableCheckGNWFill(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Name in FILL_COLOR_NAMES and node.HasChildren and node.Children[0].Name == "ColorRegister0")

# Wrapper: CLR0MaterialEntryWrapper
def EnableCheckGNWBorderEntry(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Name == "ColorRegister0" and node.Parent and node.Parent.Name in BORDER_COLOR_NAMES)

# Wrapper: CLR0MaterialEntryWrapper
def EnableCheckGNWFillEntry(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Name == "ColorRegister0" and node.Parent and node.Parent.Name in FILL_COLOR_NAMES)

## End enable check functions
## Start helper functions

# Copy frames from the given baseNode frames list to the output materials
def exportGNWColors (inputFramesList, outputMatsList):
	FRAME_COUNT = len(inputFramesList)
	
	# Material i.e. BrdDSGameWatch
	for mat in outputMatsList:
	
		# MaterialEntry i.e. ColorRegister0
		matEntry = mat.Children[0]
		
		# Set color of frames[i] to input frames[i]
		for i in range(0, FRAME_COUNT, 1):
			matEntry.SetColor(i, i, inputFramesList[i])

## End helper functions
## Start loader functions

# Base loader function (border colors, CLR0Material)
def copy_gnw_colors_border(sender, event_args):
	framesList = BrawlAPI.SelectedNode.Children[0].Colors
	main(BORDER_COLOR_NAMES, framesList)

# Base loader function (fill colors, CLR0Material)
def copy_gnw_colors_fill(sender, event_args):
	framesList = BrawlAPI.SelectedNode.Children[0].Colors
	main(FILL_COLOR_NAMES, framesList)

# Base loder function (border colors, MaterialEntry)
def copy_gnw_colors_border_entry(sender, event_args):
	framesList = BrawlAPI.SelectedNode.Colors
	main(BORDER_COLOR_NAMES, framesList)

# Base loader function (fill colors, MaterialEntry)
def copy_gnw_colors_fill_entry(sender, event_args):
	framesList = BrawlAPI.SelectedNode.Colors
	main(FILL_COLOR_NAMES, framesList)

def main (outputAnimNamesList, baseFramesList):
	CLR_LIST = BrawlAPI.NodeListOfType[CLR0Node]()
	
	# Determine which nodes in the file to modify based on names list
	matsToExportTo = []
	
	for anim in CLR_LIST:
		for mat in anim.Children:
			if mat.Name in outputAnimNamesList:
				matsToExportTo.append(mat)
	
	# Export from selected node to other applicable nodes
	exportGNWColors(baseFramesList, matsToExportTo)
	
	# Success dialog message, if fill colors
	if outputAnimNamesList == FILL_COLOR_NAMES:
		BrawlAPI.ShowMessage("G&W fill colors copied across " + matsToExportTo[0].Name + " entries.", "Success")
	
	# Success dialog message, if border colors
	else:
		BrawlAPI.ShowMessage("G&W border colors copied to " + str(len(matsToExportTo)-1) + " entries.", "Success")

## End loader functions
## Start context menu add

# Menu options from CLR0 material (AGameWatch)
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", "Set all G&W border colors to this entry", EnableCheckGNWBorder, ToolStripMenuItem("Set all GameWatch colors (border)", None, copy_gnw_colors_border))
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", "Set all G&W fill colors to this entry", EnableCheckGNWFill, ToolStripMenuItem("Set all GameWatch colors (fill)", None, copy_gnw_colors_fill))

# Menu options from CLR0 materialEntry (ColorRegister0)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", "Set all G&W border colors to this entry", EnableCheckGNWBorderEntry, ToolStripMenuItem("Set all GameWatch colors (border)", None, copy_gnw_colors_border_entry))

BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", "Set all G&W fill colors to this entry", EnableCheckGNWFillEntry, ToolStripMenuItem("Set all GameWatch colors (fill)", None, copy_gnw_colors_fill_entry))