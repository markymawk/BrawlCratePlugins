__author__ = "mawwwk"
__version__ = "1.2"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from BrawlLib import * # Imaging
from BrawlLib.Imaging import * # Imaging
from mawwwkLib import *

successCheck = False	# Global check to determine whether success prompt should be shown

SET_HUE_VALUE_PROMPT = "Enter hue value to set (0 to 359)"
ROTATE_HUE_VALUE_PROMPT = "Enter hue value to adjust by (-180 to 180)"
SET_VAL_PROMPT = "Enter brightness value to adjust by (-100 to 100)"

## Start enable check functions
# Wrapper: CLR0MaterialEntryWrapper
def EnableCheckCLR0MatEntry(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None)

# Wrapper: CLR0MaterialWrapper	
def EnableCheckCLR0Mat(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and BrawlAPI.SelectedNode.HasChildren)
	
# Wrapper: CLR0Wrapper
def EnableCheckCLR0(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and BrawlAPI.SelectedNode.HasChildren)

# Wrapper: MDL0ColorWrapper
def EnableCheckMDL0Color(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None)

## End enable check functions
## Start helper functions

# Prompt user for hue value at the start of script. Use a string input to allow for 0
def getUserValue(promptText, minValue, maxValue, exitValue=-1):
	userInput = BrawlAPI.UserStringInput(promptText)
	
	# If user closes prompt or gives bad input, return exitValue
	if not userInput:
		return exitValue
	elif userInput == "0" or userInput == "360":
		return 0
	elif int(userInput) < minValue or int(userInput) > maxValue:
		BrawlAPI.ShowError("Invalid input", "Error")
		return exitValue
	
	# Otherwise, return input as an int
	else:
		return int(userInput)

## End helper functions
## Start loader functions

# 1. START ROTATE HUE
# CLR0 loader function to run rotateHueForAllFrames()
def rotate_hue_from_clr0(sender,event_args):
	hue = getUserValue(ROTATE_HUE_VALUE_PROMPT, -180, 180, -999)
	
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			rotateHueForAllFrames(entry, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' hues rotated by hue '" + str(hue) + "'", "Success")

# CLR0Material loader function to run rotateHueForAllFrames()
def rotate_hue_from_material(sender, event_args):
	hue = getUserValue(ROTATE_HUE_VALUE_PROMPT, -180, 180, -999)
	
	for entry in BrawlAPI.SelectedNode.Children:
		rotateHueForAllFrames(entry, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames rotated by hue '" + str(hue) + "' inside\n" + BrawlAPI.SelectedNode.Name, "Success")

# CLR0MaterialEntry loader function to run rotateHueForAllFrames()
def rotate_hue_from_mat_entry(sender, event_args):
	hue = getUserValue(ROTATE_HUE_VALUE_PROMPT, -180, 180, -999)
	rotateHueForAllFrames(BrawlAPI.SelectedNode, hue)
	
	if successCheck:
		entryName = BrawlAPI.SelectedNode.Name
		materialName = BrawlAPI.SelectedNode.Parent.Name
		BrawlAPI.ShowMessage("All color frames rotated by hue '" + str(hue) + "' inside\n" + materialName + " > " + entryName, "Success")

# MDL0Color loader function to run rotateHueForAllFrames()	
def rotate_hue_from_mdl0_vertex_color(sender, event_args):
	hue = getUserValue(ROTATE_HUE_VALUE_PROMPT, -180, 180, -999)
	rotateHueForAllFrames(BrawlAPI.SelectedNode, hue)
	
	if successCheck:
		entryName = BrawlAPI.SelectedNode.Name
		materialName = BrawlAPI.SelectedNode.Parent.Name
		BrawlAPI.ShowMessage("All color frames rotated by hue '" + str(hue) + "' inside\n" + materialName + " > " + entryName, "Success")

# 1. END ROTATE HUE
# 2. START SET HUE
# CLR0 loader function to run setHueForAllFrames()
def set_hue_from_clr0(sender, event_args):
	hue = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			setHueForAllFrames(entry, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' hues set to hue '" + str(hue) + "'", "Success")

# CLR0Material loader function to run setHueForAllFrames()
def set_hue_from_material(sender, event_args):
	hue = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	
	for entry in BrawlAPI.SelectedNode.Children:
		setHueForAllFrames(entry, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames set to hue '" + str(hue) + "' inside\n" + BrawlAPI.SelectedNode.Name, "Success")

# CLR0MaterialEntry loader function to run setHueForAllFrames()
def set_hue_from_mat_entry(sender, event_args):
	hue = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	node = BrawlAPI.SelectedNode
	setHueForAllFrames(node, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames set to hue '" + str(hue) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")

# MDL0Color loader function to run setHueForAllFrames()
def set_hue_from_mdl0_vertex_color(sender, event_args):
	hue = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	node = BrawlAPI.SelectedNode
	setHueForAllFrames(node, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames set to hue '" + str(hue) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")

# 2. END SET HUE
# 3. START SET VALUE
# CLR0 loader function to run adjustValForAllFrames()
def adjust_val_from_clr0(sender, event_args):
	val = getUserValue(SET_VAL_PROMPT, -100, 100, -999)
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			adjustValForAllFrames(entry, val)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' brightness adjusted by value '" + str(val) + "'", "Success")

# CLR0Material loader function to run adjustValForAllFrames()
def adjust_val_from_material(sender, event_args):
	val = getUserValue(SET_VAL_PROMPT, -100, 100, -999)
	node = BrawlAPI.SelectedNode
	for entry in BrawlAPI.SelectedNode.Children:
		adjustValForAllFrames(entry, val)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(node.Children)) + " animations' brightness adjusted by value '" + str(val) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")

# CLR0MaterialEntry loader function to run adjustValForAllFrames()
def adjust_val_from_mat_entry(sender, event_args):
	val = getUserValue(SET_VAL_PROMPT, -100, 100, -999)
	node = BrawlAPI.SelectedNode
	adjustValForAllFrames(node, val)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames' brightness adjusted by value '" + str(val) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")

# MDL0Color loader function to run adjustValForAllFrames()
def adjust_val_mdl0_vertex_color(sender, event_args):
	val = getUserValue(SET_VAL_PROMPT, -100, 100, -999)
	node = BrawlAPI.SelectedNode
	adjustValForAllFrames(node, val)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames' brightness adjusted by value '" + str(val) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")

# 3. END ADJUST VALUE
# 4. START ADJUST SATURATION
# CLR0 loader function to run adjustSatForAllFrames()
def adjust_sat_from_clr0(sender, event_args):
	sat = getUserValue(SET_VAL_PROMPT, -100, 100, -999)
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			adjustSatForAllFrames(entry, sat)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' saturation adjusted by value '" + str(sat) + "'", "Success")

# CLR0Material loader function to run adjustSatForAllFrames()
def adjust_sat_from_material(sender, event_args):
	sat = getUserValue(SET_VAL_PROMPT, -100, 100, -999)
	for entry in BrawlAPI.SelectedNode.Children:
		adjustSatForAllFrames(entry, sat)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' saturation adjusted by value '" + str(sat) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")

# CLR0MaterialEntry loader function to run adjustSatForAllFrames()
def adjust_sat_from_mat_entry(sender, event_args):
	sat = getUserValue(SET_VAL_PROMPT, -100, 100, -999)
	node = BrawlAPI.SelectedNode
	adjustSatForAllFrames(node, sat)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames' saturation adjusted by value '" + str(sat) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")

# MDL0Color loader function to run adjustSatForAllFrames()
def adjust_sat_mdl0_vertex_color(sender, event_args):
	sat = getUserValue(SET_VAL_PROMPT, -100, 100, -999)
	node = BrawlAPI.SelectedNode
	adjustSatForAllFrames(node, sat)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames' saturation adjusted by value '" + str(sat) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")
	
## End loader functions
## Start main functions

# Main function to iterate through frames and add (rotate) hue values
def rotateHueForAllFrames(node, hueToAdd):
	global successCheck
	successCheck = False
	
	if hueToAdd >= -180:
		for i in range(0, node.ColorCount(1),1): #was ColorCount(1)
			
			# If in a vertex color node or non-Constant CLR0 node, use frame color
			if "MDL0ColorNode" in node.NodeType or not node.Constant:
				frame = node.Colors[i]
			# If in a Constant color node
			else:
				frame = node.SolidColor
			
			# Get color as HSV value
			HSV_as_List = RGB2HSV(frame)
			
			# Set hue to new
			HSV_as_List[0] += hueToAdd

			# Convert back to RGB
			new_RGB = HSV2RGB(HSV_as_List)

			# Set frame color to new RGB
			newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
			node.SetColor(i, i, newColor)	# i: index
		
		successCheck = True

# Main function to iterate through frames and set hue values
def setHueForAllFrames(node, newHue):
	global successCheck
	successCheck = False
	if newHue > -1:
		for i in range(0,node.ColorCount(1),1):
		
			# If in a vertex color node or non-Constant CLR0 node, use frame color
			if "MDL0ColorNode" in node.NodeType or not node.Constant:
				frame = node.Colors[i]
			# If in a Constant color node
			else:
				frame = node.SolidColor
			
			# Get color as HSV value
			HSV_as_List = RGB2HSV(frame)
			
			# Set hue to new
			HSV_as_List[0] = newHue
			
			# Convert back to RGB
			new_RGB = HSV2RGB(HSV_as_List)
			
			# Set frame color to new RGB
			newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
			node.SetColor(i, i, newColor)
		
		successCheck = True

# Main function to iterate through frames and set brightness (val) values
# Exactly the same as rotateHueForAllFrames() except for the HSV list index. Don't feel like consolidating into one but could be simplified
def adjustValForAllFrames(node, valToAdd):
	global successCheck
	successCheck = False
	
	if valToAdd >= -100:
		for i in range(0, node.ColorCount(1), 1):
			
			if node.Constant:
				frame = node.SolidColor
			else:
				frame = node.Colors[i]
			
			# Get color as HSV value
			HSV_as_List = RGB2HSV(frame)
			
			# Set value to new
			HSV_as_List[2] += valToAdd
			
			# Convert back to RGB
			new_RGB = HSV2RGB(HSV_as_List)
			
			# Set frame color to new RGB
			newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
			node.SetColor(i, i, newColor)	# i: index
		
		successCheck = True

# Main function to iterate through frames and set saturation values
# Exactly the same as rotateHueForAllFrames() except for the HSV list index. Don't feel like consolidating into one but could be simplified
def adjustSatForAllFrames(node, valToAdd):
	global successCheck
	successCheck = False
	
	if valToAdd >= -100:
		for i in range(0, node.ColorCount(1), 1):
			
			if node.Constant:
				frame = node.SolidColor
			else:
				frame = node.Colors[i]
			
			# Get color as HSV value
			HSV_as_List = RGB2HSV(frame)
			
			# Set value to new
			HSV_as_List[1] += valToAdd
			
			# Convert back to RGB
			new_RGB = HSV2RGB(HSV_as_List)
			
			# Set frame color to new RGB
			newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
			node.SetColor(i, i, newColor)	# i: index
		
		successCheck = True

## End main functions
## Start context menu add

# "Set hue" context options
# Set from CLR0
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Set the hue of all frames to a defined integer", EnableCheckCLR0, ToolStripMenuItem("Set hue (all entries)", None, set_hue_from_clr0))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", "Set the hue of all frames to a defined integer", EnableCheckCLR0Mat, ToolStripMenuItem("Set hue (all entries)", None, set_hue_from_material))
# Set from Material Entry (LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", "Set the hue of all frames to a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Set hue (all frames)", None, set_hue_from_mat_entry))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", "Set the hue of all frames to a defined integer", EnableCheckMDL0Color, ToolStripMenuItem("Set hue (all entries)", None, set_hue_from_mdl0_vertex_color))

# "Rotate hue" context options
# Set from CLR0
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Rotate the hue of all frames by a defined integer", EnableCheckCLR0, ToolStripMenuItem("Rotate hue (all entries)", None, rotate_hue_from_clr0))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", "Rotate the hue of all frames by a defined integer", EnableCheckCLR0Mat, ToolStripMenuItem("Rotate hue (all entries)", None, rotate_hue_from_material))
# Set from CLR0 Material Entry (LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", "Rotate the hue of all frames by a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Rotate hue (all frames)", None, rotate_hue_from_mat_entry))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", "Rotate the hue of all frames by a defined integer", EnableCheckMDL0Color, ToolStripMenuItem("Rotate hue (all entries)", None, rotate_hue_from_mdl0_vertex_color))

# "Adjust brightness" context options
# Set from CLR0
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Adjust brightness value of all frames by a defined integer", EnableCheckCLR0, ToolStripMenuItem("Adjust brightness (all entries)", None, adjust_val_from_clr0))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", "Adjust brightness value of all frames by a defined integer", EnableCheckCLR0Mat, ToolStripMenuItem("Adjust brightness (all entries)", None, adjust_val_from_material))
# Set from CLR0 Material Entry LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", "Adjust brightness value of all frames by a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Adjust brightness (all frames)", None, adjust_val_from_mat_entry))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", "Adjust brightness value of all frames by a defined integer", EnableCheckMDL0Color, ToolStripMenuItem("Adjust brightness (all entries)", None, adjust_val_mdl0_vertex_color))

# "Adjust saturation" context options
# Set from CLR0
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Adjust saturation value of all frames by a defined integer", EnableCheckCLR0, ToolStripMenuItem("Adjust saturation (all entries)", None, adjust_sat_from_clr0))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", "Adjust saturation value of all frames by a defined integer", EnableCheckCLR0Mat, ToolStripMenuItem("Adjust saturation (all entries)", None, adjust_sat_from_material))
# Set from CLR0 Material Entry LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", "Adjust saturation value of all frames by a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Adjust saturation (all frames)", None, adjust_sat_from_mat_entry))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", "Adjust saturation value of all frames by a defined integer", EnableCheckMDL0Color, ToolStripMenuItem("Adjust saturation (all entries)", None, adjust_sat_mdl0_vertex_color))
