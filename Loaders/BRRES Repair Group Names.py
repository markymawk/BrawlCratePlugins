__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.Internal import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Repair BRRES group names"
VALID_GROUP_NAMES = ["3DModels(NW4R)", "AnmChr(NW4R)", "AnmVis(NW4R)", "AnmClr(NW4R)", "AnmTexPat(NW4R)", "AnmTexSrt(NW4R)", "Textures(NW4R)", "Palettes(NW4R)"]

## Start enable check functions

# Wrapper: BRESWrapper
# Set to true if node has any group names not in VALID_GROUP_NAMES
def enableCheckBRES(sender, event_args):
	node = BrawlAPI.SelectedNode
	
	# If node is not empty, check for children
	if node:
		if node.HasChildren:
			isCorrupt = False
			for group in node.Children:
				if group.Name not in VALID_GROUP_NAMES:
					isCorrupt = True
			
			sender.Enabled = isCorrupt
		# If node has no children, set false
		else:
			sender.Enabled = False
	
	# If node is empty, set false
	else:
		sender.Enabled = False

## End enable check functions
## Start main functions

def repair_brres_groups(sender, event_args):
	brres = BrawlAPI.SelectedNode
	
	for group in brres.Children:
		if not group.HasChildren:
			continue
		
		# Check group type
		groupType = group.Children[0].NodeType
		if "CHR0" in groupType:
			name = CHR_GROUP
		elif "MDL0" in groupType:
			name = MDL_GROUP
		elif "VIS0" in groupType:
			name = VIS_GROUP
		elif "CLR0" in groupType:
			name = CLR_GROUP
		elif "PAT0" in groupType:
			name = PAT_GROUP
		elif "SRT0" in groupType:
			name = SRT_GROUP
		elif "TEX0" in groupType:
			name = TEX_GROUP
		elif "PLT0" in groupType:
			name = PLT_GROUP
		else:
			name = group.Name
		
		# Set name
		group.Name = name
	
## End main functions
## Start context menu add

BrawlAPI.AddContextMenuItem(BRESWrapper, "", "Repair corrupted group names", enableCheckBRES, ToolStripMenuItem("Repair group names", None, repair_brres_groups))