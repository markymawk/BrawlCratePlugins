__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Update Shared-Name Material Colors"

## Start enable check functions
# Wrapper: MDL0MaterialWrapper
def EnableCheckMDL0Material(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Parent)

## End enable check functions
## Start loader functions

def update_mats_with_same_name(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	matsToUpdate = []
	for mat in BrawlAPI.NodeListOfType[MDL0MaterialNode]():
		if mat.Name == selNode.Name:
			matsToUpdate.append(mat)
	
	# If material doesn't share a name with any others, quit script
	if len(matsToUpdate) == 1:
		BrawlAPI.ShowMessage("No other materials named \'" + selNode.Name + "\' found in file.", SCRIPT_NAME)
		return
	
	msg = str(len(matsToUpdate)) + " materials found named \'" + selNode.Name + "\'.\n\n"
	msg += "Update color values in LightChannel0, Shader Colors, and Shader Constant Colors of these materials?"
	if not BrawlAPI.ShowYesNoPrompt(msg, SCRIPT_NAME):
		return
	
	# Update mats
	for mat in matsToUpdate:
		mat.LightChannel0.MaterialColor = selNode.LightChannel0.MaterialColor
		mat.LightChannel0.AmbientColor = selNode.LightChannel0.AmbientColor
		mat.Color0 = selNode.Color0
		mat.Color1 = selNode.Color1
		mat.Color2 = selNode.Color2
		mat.ConstantColor0 = selNode.ConstantColor0
		mat.ConstantColor1 = selNode.ConstantColor1
		mat.ConstantColor2 = selNode.ConstantColor2

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(MDL0MaterialWrapper, "", "Copy color values from this material to those with the same name", EnableCheckMDL0Material, ToolStripMenuItem("Update shared-name materials", None, update_mats_with_same_name))
