__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Increment Texture Name"

## Start enable check function
# Check that tex0 name ends in a digit
# Wrapper: TEX0Wrapper
def EnableCheckTEX0Number(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None \
	and node.Name[-1].isdigit() and node.Parent)

## End enable check function
## Start loader function

def increment_tex0_name(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	
	# Find last node to rename
	if not BrawlAPI.ShowOKCancelPrompt("Including the selected texture, enter the amount of textures above (behind) the selected one to increment.", SCRIPT_NAME):
		return
	
	# Get amount of textures to rename
	texturesToRenameCount = BrawlAPI.UserStringInput("Texture count (Enter -1 for all)")
	if texturesToRenameCount == "None":
		return
	texturesToRenameCount = int(texturesToRenameCount)
	
	# If input is -1, do all textures (set count to a big number)
	if texturesToRenameCount == -1:
		texturesToRenameCount = 9999
	
	nodeToRename = selNode
	
	for i in range (0, texturesToRenameCount, 1):
		oldDigitSuffix = ""
		
		# If texture name doesn't end in a number, exit the loop
		if not nodeToRename.Name[-1].isdigit():
			break
		
		# Otherwise, store the ending digits of the texture name and remove them from the name
		while nodeToRename.Name[-1].isdigit():
			oldDigitSuffix = str(nodeToRename.Name[-1]) + "" + str(oldDigitSuffix) 
			nodeToRename.Name = nodeToRename.Name[:-1]
		
		# Calculate new ending digit
		newDigitSuffix = str(int(oldDigitSuffix) + 1)
		
		# Add leading zeroes
		while len(newDigitSuffix) < len(oldDigitSuffix):
			newDigitSuffix = '0' + newDigitSuffix
		
		nodeToRename.Name = nodeToRename.Name + "" + newDigitSuffix
		
		# If above node exists, use it in the next loop run
		nodeToRename = nodeToRename.PrevSibling()
		if nodeToRename is None:
			break

## End loader function
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Rename TEX0 and multiple other textures by incrementing 1", EnableCheckTEX0Number, ToolStripMenuItem("Increment texture names...", None, increment_tex0_name))
