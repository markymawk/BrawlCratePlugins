__author__ = "mawwwk"
__version__ = "1.1"

from BrawlCrate.NodeWrappers import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Increment Texture Name"

NAMES_TO_IGNORE = [
	"TShadow1"
]

## Start enable check function
# Check that tex0 name ends in a digit, with a prevSibling that also ends in a digit
# Wrapper: TEX0Wrapper
def EnableCheckTEX0Number(sender, event_args):
	node = BrawlAPI.SelectedNode
	prevSibling = node.PrevSibling()
	
	sender.Enabled = (node and prevSibling and node.Parent \
	and node.Name not in NAMES_TO_IGNORE \
	and node.Name[-1].isdigit() \
	and prevSibling.Name[-1].isdigit())

## End enable check function
## Start loader function

def increment_tex0_name(sender, event_args):
	
	# Confirmation prompt
	if not BrawlAPI.ShowOKCancelPrompt("Including the selected texture, enter the amount of textures above (behind) the selected one to increment.", SCRIPT_NAME):
		return
	
	# Get amount of textures to rename
	textureCount = BrawlAPI.UserStringInput("Texture count (Enter -1 for all)")
	if textureCount == "None":
		return
	textureCount = int(textureCount)
	
	# If input is -1, do all textures (set count to a big number)
	if textureCount == -1:
		textureCount = 9999
	
	tex0 = BrawlAPI.SelectedNode
	
	for i in range(textureCount):
		
		# If texture name doesn't end in a number, quit
		if not tex0.Name[-1].isdigit():
			return
		
		# Store the ending digits of the texture name, and remove them from the name
		digitsOld = ""
		while tex0.Name[-1].isdigit():
			digitsOld = str(tex0.Name[-1]) + "" + str(digitsOld)
			tex0.Name = tex0.Name[:-1]
		
		# Calculate new ending digit
		digitsNew = str(int(digitsOld) + 1)
		
		# Add leading zeroes
		while len(digitsNew) < len(digitsOld):
			digitsNew = '0' + digitsNew
		
		tex0.Name = tex0.Name + "" + digitsNew
		
		# If above node exists, use it in the next loop run
		tex0 = tex0.PrevSibling()
		
		# If at the final node, quit
		if tex0 is None:
			return

## End loader function
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Rename multiple TEX0s by incrementing 1", EnableCheckTEX0Number, ToolStripMenuItem("Increment texture names...", None, increment_tex0_name))
