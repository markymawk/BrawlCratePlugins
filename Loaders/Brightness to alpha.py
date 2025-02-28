__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.NodeWrappers import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Brightness to alpha"
## Start enable check functions
# Wrapper: MDL0ColorWrapper
def EnableCheckMDL0Color(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None

## End enable check functions
## Start loader functions
def brightness_to_alpha(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	
	usedColors = []
	isDuplicate = False
	for i in range(selNode.ColorCount(0)):
		# Get color value (brightness)
		color = selNode.GetColor(i, 0)
		brightness = RGB2HSV(color)[2]
		
		# Convert from [0, 100] to [0, 255]
		alpha = round(brightness * 255 / 100)
		newColor = ARGBPixel(alpha, color.R, color.G, color.B)
		if newColor in usedColors:
			isDuplicate = True
		else:
			usedColors.append(newColor)
		
		selNode.SetColor(i, 0, newColor)
	
	# If duplicate colors found, warn the user
	if isDuplicate:
		msg = "Complete.\n\nDuplicate vertex colors detected. This is known to cause color corruption on saving."
		BrawlAPI.ShowWarning(msg, SCRIPT_NAME)

## End loader functions
## Start context menu add

# Set from CLR0
shortText = "Brightness to alpha"
longText = "Set alpha value of each color entry to match its value (brightness)"
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, brightness_to_alpha))