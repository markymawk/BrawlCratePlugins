__author__ = "mawwwk"
__version__ = "1.0.2"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.Internal import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Detect SCN0 Usage"

## Start enable check functions

# LightSet check: selected node is a LightSet node with a Parent.Parent of type SCN0Node
# Wrapper: GenericWrapper
def enableCheckLightSet(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node \
	and isinstance(node, SCN0LightSetNode) \
	and node.Parent \
	and node.Parent.Parent \
	and isinstance(node.Parent.Parent, SCN0Node) \
	and "LightSet" in node.Parent.Name)

# Fog check: nothing specific
# Wrapper: SCN0FogWrapper
def enableCheckFog(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None)

## End enable check functions
## Start main functions

def check_LightSet_use(sender, event_args):
	lightSetIndex = BrawlAPI.SelectedNode.RealIndex
	lightSetName = BrawlAPI.SelectedNode.Name
	
	# Build list of materials that use the matching index
	usedMaterialsList = []
	for mat in BrawlAPI.NodeListOfType[MDL0MaterialNode]():
		if mat.LightSetIndex == lightSetIndex:
			usedMaterialsList.append(mat)
	
	# Results
	# If LightSet used, list all materials used, formatted as brres/MDL0Name/MaterialName
	if len(usedMaterialsList):
		msg = "LightSet " + lightSetName + " used by " + str(len(usedMaterialsList)) + " material(s):\n"
		
		# Generate output message
		outputList = []
		for mat in usedMaterialsList:
			mdl0 = mat.Parent.Parent
			brres = mat.Parent.Parent.Parent.Parent
			outputList.append(brres.Name + "/" + mdl0.Name + "/" + mat.Name)
		
		msg += listToString(outputList, 20)
		
		BrawlAPI.ShowMessage(msg, "SCN0 LightSet Usage")
	
	# If LightSet unused, show unused message
	else:
		BrawlAPI.ShowMessage("LightSet " + lightSetName + " not used by any materials.", "SCN0 LightSet Unused")

def check_fog_use(sender, event_args):
	fogIndex = BrawlAPI.SelectedNode.RealIndex
	fogName = BrawlAPI.SelectedNode.Name
	
	# Build list of materials that use the matching index
	usedMaterialsList = []
	for mat in BrawlAPI.NodeListOfType[MDL0MaterialNode]():
		if mat.FogIndex == fogIndex:
			usedMaterialsList.append(mat)
	
	# Results
	# If fog used, list all materials used, formatted as brres/MDL0Name/MaterialName
	if len(usedMaterialsList):
		msg = "Fog " + fogName + " used by " + str(len(usedMaterialsList)) + " material(s):\n"
		
		# Generate output message
		outputList = []
		for mat in usedMaterialsList:
			mdl0 = mat.Parent.Parent
			brres = mat.Parent.Parent.Parent.Parent
			outputList.append(brres.Name + "/" + mdl0.Name + "/" + mat.Name)
		
		msg += listToString(outputList, 20)
		
		BrawlAPI.ShowMessage(msg, "SCN0 Fog Usage")
		
	# If fog unused, show unused message
	else:
		BrawlAPI.ShowMessage("Fog " + fogName + " not used by any materials.", "SCN0 Fog Unused")

## End main functions
## Start context menu add

# LightSet uses GenericWrapper
BrawlAPI.AddContextMenuItem(GenericWrapper, "", "Detect SCN0 LightSet usage in materials", enableCheckLightSet, ToolStripMenuItem("Locate SCN0 LightSet usage", None, check_LightSet_use))

# Fog check
BrawlAPI.AddContextMenuItem(SCN0FogWrapper, "", "Detect SCN0 fog usage in materials", enableCheckFog, ToolStripMenuItem("Locate SCN0 fog usage", None, check_fog_use))
