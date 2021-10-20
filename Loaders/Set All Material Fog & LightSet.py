__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *
MINIMUM_INDEX_VALUE = -1
MAXIMUM_INDEX_VALUE = 20

## Start enable check function

# Check that model has Materials group
# Wrapper: MDL0Wrapper
def EnableCheckMDL0(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None \
	and getChildFromName(BrawlAPI.SelectedNode, "Materials"))

## End enable check function
## Begin helper methods

def getMatValues(isLightSet=0):
	if isLightSet:
		indexName = "LightSetIndex"
	else:
		indexName = "FogIndex"
	
	newValue = BrawlAPI.UserStringInput("Enter " + indexName + " value (-1 to 20)")
	
	if str(newValue) == "" or str(newValue) == "None":
		return -99
	
	newValue = int(newValue)
	
	if newValue < MINIMUM_INDEX_VALUE or newValue > MAXIMUM_INDEX_VALUE:
		BrawlAPI.ShowError("Value out of range (" + str(MINIMUM_INDEX_VALUE) + " to " + str(MAXIMUM_INDEX_VALUE) + ")", "Error")
		
	return newValue

## End helper methods
## Start of loader functions

def set_all_mats_fog(sender, event_args):
	matsGroup = getChildFromName(BrawlAPI.SelectedNode, "Materials")
	
	if not matsGroup:
		return
	
	fogValue = getMatValues(0)
	
	if fogValue >= MINIMUM_INDEX_VALUE:
		for mat in matsGroup.Children:
			mat.FogIndex = fogValue

def set_all_mats_lightset(sender, event_args):
	matsGroup = getChildFromName(BrawlAPI.SelectedNode, "Materials")
	
	if not matsGroup:
		return
	
	lightSetValue = getMatValues(1)
	
	if lightSetValue >= MINIMUM_INDEX_VALUE:
		for mat in matsGroup.Children:
			mat.LightSetIndex = lightSetValue

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Set all material LightSet values to the same index", EnableCheckMDL0, ToolStripMenuItem("Set all materials' LightSet index", None, set_all_mats_lightset))

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Set all material FodIndex values to the same fog", EnableCheckMDL0, ToolStripMenuItem("Set all materials' Fog index", None, set_all_mats_fog))