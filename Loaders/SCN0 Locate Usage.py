__author__ = "mawwwk"
__version__ = "1.0"

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
	sender.Enabled = (BrawlAPI.SelectedNode is not None \
	and isinstance(BrawlAPI.SelectedNode, SCN0LightSetNode) \
	and BrawlAPI.SelectedNode.Parent is not None \
	and BrawlAPI.SelectedNode.Parent.Parent is not None \
	and isinstance(BrawlAPI.SelectedNode.Parent.Parent, SCN0Node) \
	and "LightSet" in BrawlAPI.SelectedNode.Parent.Name)

# Fog check: nothing specific
# Wrapper: SCN0FogWrapper
def enableCheckFog(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None)

## End enable check functions
## Start helper functions

# Given the SCN0 realIndex value, parse all MDL0s for the materials inside.
# If the material uses the given SCN0 data, add it to a list, then return that list
def buildUsedMaterialsList(SCN0Index, isLightSet):
	usedMaterialsList = []
	MDL0List = BrawlAPI.NodeListOfType[MDL0Node]()
	
	for mdl0 in BrawlAPI.NodeListOfType[MDL0Node]():
		matsGroup = getChildFromName(mdl0,"Material")
		if matsGroup:
			for material in matsGroup.Children:
				if isLightSet and material.LightSetIndex == SCN0Index:
					usedMaterialsList.append(material)
				elif not isLightSet and material.FogIndex == SCN0Index:
					usedMaterialsList.append(material)
	
	return usedMaterialsList
	
## End helper functions
## Start main functions

def checkLightSetUse(sender, event_args):
	lightSetIndex = BrawlAPI.SelectedNode.RealIndex
	lightSetName = BrawlAPI.SelectedNode.Name
	
	# Build list of materials that use the matching index
	usedMaterialsList = buildUsedMaterialsList(lightSetIndex, True)
	
	# Results
	# If unused, show unused message and end script
	if len(usedMaterialsList) == 0:
		BrawlAPI.ShowMessage("LightSet " + lightSetName + " not used by any materials.", "SCN0 LightSet Unused")
	# If used, list all materials used, formatted as ModelData/MDL0Name/MaterialName
	else:
		msg = "LightSet " + lightSetName + " used by " + str(len(usedMaterialsList)) + " material(s):\n"
		
		for mat in usedMaterialsList:
			msg += mat.Parent.Parent.Parent.Parent.Name + "/" + mat.Parent.Parent.Name + "/" + mat.Name + "\n"
		
		BrawlAPI.ShowMessage(msg, "SCN0 LightSet Usage")

def checkFogUse(sender, event_args):
	fogIndex = BrawlAPI.SelectedNode.RealIndex
	fogName = BrawlAPI.SelectedNode.Name
	
	# Build list of materials that use the matching index
	usedMaterialsList = buildUsedMaterialsList(fogIndex, False)
	
	# Results
	# If unused, show unused message and end script
	if len(usedMaterialsList) == 0:
		BrawlAPI.ShowMessage("Fog " + fogName + " not used by any materials.", "SCN0 Fog Unused")
	# If used, list all materials used, formatted as ModelData/MDL0Name/MaterialName
	else:
		msg = "Fog " + fogName + " used by " + str(len(usedMaterialsList)) + " material(s):\n"
		
		for mat in usedMaterialsList:
			msg += mat.Parent.Parent.Parent.Parent.Name + "/" + mat.Parent.Parent.Name + "/" + mat.Name + "\n"
		
		BrawlAPI.ShowMessage(msg, "SCN0 Fog Usage")

## End main functions
## Start context menu add

# LightSet uses GenericWrapper
BrawlAPI.AddContextMenuItem(GenericWrapper, "", "Detect SCN0 LightSet usage in materials", enableCheckLightSet, ToolStripMenuItem("Locate SCN0 LightSet usage", None, checkLightSetUse))

# Fog check
BrawlAPI.AddContextMenuItem(SCN0FogWrapper, "", "Detect SCN0 fog usage in materials", enableCheckFog, ToolStripMenuItem("Locate SCN0 fog usage", None, checkFogUse))
