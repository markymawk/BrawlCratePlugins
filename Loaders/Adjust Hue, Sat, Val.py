__author__ = "mawwwk"
__version__ = "2.0"

from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from BrawlLib import * # Imaging
from BrawlLib.Imaging import * # Imaging
from System.IO import *
from mawwwkLib import *

SET_HUE_VALUE_PROMPT = "Enter hue value to set (0 to 359)"
ROTATE_HUE_VALUE_PROMPT = "Enter hue value to adjust by (-360 to 360)"
SET_VAL_PROMPT = "Enter brightness value to adjust by (-100 to 100)"
SET_SAT_PROMPT = "Enter saturation value to adjust by (-100 to 100)"
TEMP_MDL0_FILE_PATH = AppPath + "\\TEMP.mdl0"

## Start enable check functions
# Wrapper: CLR0MaterialEntryWrapper
def EnableCheckCLR0MatEntry(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None

# Wrapper: CLR0MaterialWrapper	
def EnableCheckCLR0Mat(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and node.HasChildren
	
# Wrapper: CLR0Wrapper
def EnableCheckCLR0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and node.HasChildren

# Wrapper: MDL0ColorWrapper
def EnableCheckMDL0Color(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None

## End enable check functions
## Start helper functions

# getUserValue()
# Prompt user for value at the start of script. Use a string input to allow for 0
def getUserValue(promptText, minValue, maxValue):
	userInput = BrawlAPI.UserStringInput(promptText)
	
	# If user closes prompt or gives bad input, return exitValue
	if not userInput:
		return None
	elif int(userInput) < minValue or int(userInput) > maxValue:
		BrawlAPI.ShowError("Invalid input", "Error")
		return None
	
	# Otherwise, return input as an int
	else:
		return int(userInput)

# From vertex color node, update the parent model using a temp file
def updateParentMDL0(selNode):
	if not (selNode.Parent or selNode.Parent.Parent):
		return
	parentMDL0 = selNode.Parent.Parent
	parentMDL0.Export(TEMP_MDL0_FILE_PATH)
	parentMDL0.Replace(TEMP_MDL0_FILE_PATH)
	File.Delete(TEMP_MDL0_FILE_PATH)

def setFrameColor(node, index, hsvList, alpha):
	# Convert HSV list to RGB
	newRGB = HSV2RGB(hsvList)
	newColor = ARGBPixel(alpha, newRGB[0], newRGB[1], newRGB[2])
	node.SetColor(index, index, newColor)

## End helper functions
## Start loader functions

# Loader function to run rotateHueForAllFrames()
def rotate_hue(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	hueRotate = getUserValue(ROTATE_HUE_VALUE_PROMPT, -360, 360)
	if hueRotate is None:
		return
	
	# CLR0 node
	if isinstance(selNode, CLR0Node):
		for material in BrawlAPI.SelectedNode.Children:
			for entry in material.Children:
				rotateHueForAllFrames(entry, hueRotate)
		
		resultsMsg = str(len(selNode.Children)) + " animations' hues rotated by hue '" + str(hueRotate) + "'"
	
	# CLR0MaterialNode
	elif isinstance(selNode, CLR0MaterialNode):
		for entry in selNode.Children:
			rotateHueForAllFrames(entry, hueRotate)
		
		resultsMsg = "All color frames rotated by hue '" + str(hueRotate) + "' inside\n" + selNode.Name
	
	# CLR0MaterialEntry
	elif isinstance(selNode, CLR0MaterialEntryNode):
		rotateHueForAllFrames(selNode, hueRotate)
		
		resultsMsg = "All color frames rotated by hue '" + str(hueRotate) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name
	
	# MDL0 Color (vertex colors)
	elif isinstance(selNode, MDL0ColorNode):
		rotateHueForAllFrames(selNode, hueRotate)
		
		if selNode.Parent and selNode.Parent.Parent: 
			parentMDL0 = selNode.Parent.Parent
			updateParentMDL0(selNode)
		
		resultsMsg = "All color frames rotated by hue '" + str(hueRotate) + "' inside\n" + selNode.Name
	# Unknown format (shouldn't happen)
	else:
		BrawlAPI.ShowError("Error - unknown format", "Error")
		return
	
	BrawlAPI.ShowMessage(resultsMsg, "Success")

# Loader function to run setHueForAllFrames()
def set_hue(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	hueSet = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	if hueSet is None:
		return
	
	# CLR0 node
	if isinstance(selNode, CLR0Node):
		for material in BrawlAPI.SelectedNode.Children:
			for entry in material.Children:
				setHueForAllFrames(entry, hueSet)
		
		resultsMsg = str(len(selNode.Children)) + " animations' hues set to hue '" + str(hueSet) + "'"
	
	# CLR0MaterialNode
	elif isinstance(selNode, CLR0MaterialNode):
		for entry in selNode.Children:
			setHueForAllFrames(entry, hueSet)
		
		resultsMsg = "All color frames set to hue '" + str(hueSet) + "' inside\n" + selNode.Name
	
	# CLR0MaterialEntry
	elif isinstance(selNode, CLR0MaterialEntryNode):
		setHueForAllFrames(selNode, hueSet)
		
		resultsMsg = "All color frames set to hue '" + str(hueSet) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name
	
	# MDL0 Color (vertex colors)
	elif isinstance(selNode, MDL0ColorNode):
		setHueForAllFrames(selNode, hueSet)
		
		if selNode.Parent and selNode.Parent.Parent: 
			parentMDL0 = selNode.Parent.Parent
			updateParentMDL0(selNode)
		
		resultsMsg = "All color frames set to hue '" + str(hueSet) + "' inside\n" + selNode.Name
	# Unknown format (shouldn't happen)
	else:
		BrawlAPI.ShowError("Error - unknown format", "Error")
		return
	
	BrawlAPI.ShowMessage(resultsMsg, "Success")

# Loader function to run adjustValForAllFrames()
def adjust_val(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	valAdjust = getUserValue(SET_VAL_PROMPT, -100, 100)
	if valAdjust is None:
		return
	
	# CLR0 node
	if isinstance(selNode, CLR0Node):
		for material in BrawlAPI.SelectedNode.Children:
			for entry in material.Children:
				adjustValForAllFrames(entry, valAdjust)
		
		resultsMsg = str(len(selNode.Children)) + " animations' brightness adjusted by value '" + str(valAdjust) + "'"
	
	# CLR0MaterialNode
	elif isinstance(selNode, CLR0MaterialNode):
		for entry in selNode.Children:
			adjustValForAllFrames(entry, valAdjust)
		
		resultsMsg = str(len(selNode.Children)) + " animations' brightness adjusted by value '" + str(valAdjust) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name
	
	# CLR0MaterialEntry
	elif isinstance(selNode, CLR0MaterialEntryNode):
		adjustValForAllFrames(selNode, valAdjust)
		
		resultsMsg = "All color frames' brightness adjusted by value '" + str(valAdjust) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name
	
	# MDL0 Color (vertex colors)
	elif isinstance(selNode, MDL0ColorNode):
		adjustValForAllFrames(selNode, valAdjust)
		
		if selNode.Parent and selNode.Parent.Parent: 
			parentMDL0 = selNode.Parent.Parent
			updateParentMDL0(selNode)
		
		resultsMsg = "All color frames' brightness adjusted by value '" + str(valAdjust) + "' inside\n" + selNode.Name
	# Unknown format (shouldn't happen)
	else:
		BrawlAPI.ShowError("Error - unknown format", "Error")
		return
	
	BrawlAPI.ShowMessage(resultsMsg, "Success")

# Loader function to run adjustSatForAllFrames()
def adjust_sat(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	satAdjust = getUserValue(SET_SAT_PROMPT, -100, 100)
	if satAdjust is None:
		return
	
	# CLR0 node
	if isinstance(selNode, CLR0Node):
		for material in BrawlAPI.SelectedNode.Children:
			for entry in material.Children:
				adjustSatForAllFrames(entry, satAdjust)
		resultsMsg = str(len(selNode.Children)) + " animations' saturation adjusted by value '" + str(satAdjust) + "'"
	
	# CLR0MaterialNode
	elif isinstance(selNode, CLR0MaterialNode):
		for entry in selNode.Children:
			adjustSatForAllFrames(entry, satAdjust)
		
		resultsMsg = str(len(selNode.Children)) + " animations' saturation adjusted by value '" + str(satAdjust) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name
	
	# CLR0MaterialEntry
	elif isinstance(selNode, CLR0MaterialEntryNode):
		adjustSatForAllFrames(selNode, satAdjust)
		
		resultsMsg = "All color frames' saturation adjusted by value '" + str(satAdjust) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name
	
	# MDL0 Color (vertex colors)
	elif isinstance(selNode, MDL0ColorNode):
		adjustSatForAllFrames(selNode, satAdjust)
		
		if selNode.Parent and selNode.Parent.Parent: 
			parentMDL0 = selNode.Parent.Parent
			updateParentMDL0(selNode)
		
		resultsMsg = "All color frames' saturation adjusted by value '" + str(satAdjust) + "' inside\n" + selNode.Name
	# Unknown format (shouldn't happen)
	else:
		BrawlAPI.ShowError("Error - unknown format", "Error")
		return
	
	BrawlAPI.ShowMessage(resultsMsg, "Success")
	
## End loader functions
## Start main functions

# Main function to loop through frames and add (rotate) hue values
def rotateHueForAllFrames(node, hueToAdd):
	for i in range(node.ColorCount(1)):
			
		# If in a vertex color node or non-Constant CLR0 node, use frame color
		if "MDL0ColorNode" in node.NodeType or not node.Constant:
			frame = node.Colors[i]
		# If in a Constant color node
		else:
			frame = node.SolidColor
		
		hsvList = RGB2HSV(frame)	# Get color as HSV value
		hsvList[0] += hueToAdd		# Set hue to new
		setFrameColor(node, i, hsvList, frame.A)

# Main function to loop through frames and set hue values
def setHueForAllFrames(node, newHue):
	for i in range(node.ColorCount(1)):
	
		# If in a vertex color node or non-Constant CLR0 node, use frame color
		if "MDL0ColorNode" in node.NodeType or not node.Constant:
			frame = node.Colors[i]
		# If in a Constant color node
		else:
			frame = node.SolidColor
		
		hsvList = RGB2HSV(frame)	# Get color as HSV value
		hsvList[0] = newHue			# Set hue to new
		setFrameColor(node, i, hsvList, frame.A)

# Main function to loop through frames and set saturation values
def adjustSatForAllFrames(node, valToAdd):
	for i in range(node.ColorCount(1)):
			
		if "MDL0ColorNode" in node.NodeType or not node.Constant:
			frame = node.Colors[i]
		else:
			frame = node.SolidColor
		
		hsvList = RGB2HSV(frame)	# Get color as HSV value
		hsvList[1] += valToAdd		# Set value to new
		setFrameColor(node, i, hsvList, frame.A)

# Main function to loop through frames and set brightness (val) values
def adjustValForAllFrames(node, valToAdd):
	for i in range(node.ColorCount(1)):
		
		if "MDL0ColorNode" in node.NodeType or not node.Constant:
			frame = node.Colors[i]
		else:
			frame = node.SolidColor
		
		hsvList = RGB2HSV(frame)	# Get color as HSV value
		hsvList[2] += valToAdd		# Set value to new
		setFrameColor(node, i, hsvList, frame.A)

## End main functions
## Start context menu add

# "Rotate hue" context options
# Set from CLR0
shortText = "Rotate hue"
longText = "Rotate the hue of all frames by a set value"
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", longText, EnableCheckCLR0, ToolStripMenuItem(shortText, None, rotate_hue))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", longText, EnableCheckCLR0Mat, ToolStripMenuItem(shortText, None, rotate_hue))
# Set from CLR0 Material Entry (LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", longText, EnableCheckCLR0MatEntry, ToolStripMenuItem(shortText, None, rotate_hue))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, rotate_hue))

# "Set hue" context options
# Set from CLR0
shortText = "Set hue"
longText = "Set the hue of all frames to a set value"
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", longText, EnableCheckCLR0, ToolStripMenuItem(shortText, None, set_hue))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", longText, EnableCheckCLR0Mat, ToolStripMenuItem(shortText, None, set_hue))
# Set from Material Entry (LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", longText, EnableCheckCLR0MatEntry, ToolStripMenuItem(shortText, None, set_hue))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, set_hue))

# "Adjust brightness" context options
# Set from CLR0
shortText = "Adjust brightness"
longText = "Adjust brightness value of all frames by a set value"
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", longText, EnableCheckCLR0, ToolStripMenuItem(shortText, None, adjust_val))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", longText, EnableCheckCLR0Mat, ToolStripMenuItem(shortText, None, adjust_val))
# Set from CLR0 Material Entry LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", longText, EnableCheckCLR0MatEntry, ToolStripMenuItem(shortText, None, adjust_val))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, adjust_val))

# "Adjust saturation" context options
# Set from CLR0
shortText = "Adjust saturation"
longText = "Adjust saturation of all frames by a set value"
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", longText, EnableCheckCLR0, ToolStripMenuItem(shortText, None, adjust_sat))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", longText, EnableCheckCLR0Mat, ToolStripMenuItem(shortText, None, adjust_sat))
# Set from CLR0 Material Entry LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", longText, EnableCheckCLR0MatEntry, ToolStripMenuItem(shortText, None, adjust_sat))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, adjust_sat))
