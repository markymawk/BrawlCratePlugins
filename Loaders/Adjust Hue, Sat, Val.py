__author__ = "mawwwk"
__version__ = "1.2.4"

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

## End helper functions
## Start loader functions

# 1. START ROTATE HUE
# CLR0 loader function to run rotateHueForAllFrames()
def rotate_hue_from_clr0(sender,event_args):
	hue = getUserValue(ROTATE_HUE_VALUE_PROMPT, -360, 360)
	if hue is None:
		return
	
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			rotateHueForAllFrames(entry, hue)
	
	BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' hues rotated by hue '" + str(hue) + "'", "Success")

# CLR0Material loader function to run rotateHueForAllFrames()
def rotate_hue_from_material(sender, event_args):
	hue = getUserValue(ROTATE_HUE_VALUE_PROMPT, -360, 360)
	if hue is None:
		return
	
	for entry in BrawlAPI.SelectedNode.Children:
		rotateHueForAllFrames(entry, hue)
	
	BrawlAPI.ShowMessage("All color frames rotated by hue '" + str(hue) + "' inside\n" + BrawlAPI.SelectedNode.Name, "Success")

# CLR0MaterialEntry loader function to run rotateHueForAllFrames()
def rotate_hue_from_mat_entry(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	hue = getUserValue(ROTATE_HUE_VALUE_PROMPT, -360, 360)
	if hue is None:
		return
	
	rotateHueForAllFrames(selNode, hue)
	
	entryName = selNode.Name
	materialName = selNode.Parent.Name
	BrawlAPI.ShowMessage("All color frames rotated by hue '" + str(hue) + "' inside\n" + materialName + " > " + entryName, "Success")

# MDL0Color loader function to run rotateHueForAllFrames()	
def rotate_hue_from_mdl0_vertex_color(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	hue = getUserValue(ROTATE_HUE_VALUE_PROMPT, -360, 360)
	if hue is None:
		return
	
	if selNode.Parent and selNode.Parent.Parent: 
		parentMDL0 = BrawlAPI.SelectedNode.Parent.Parent
	
	rotateHueForAllFrames(selNode, hue)
	updateParentMDL0(selNode)
	
	entryName = selNode.Name
	BrawlAPI.ShowMessage("All color frames rotated by hue '" + str(hue) + "' inside\n" + entryName, "Success")

# 1. END ROTATE HUE
# 2. START SET HUE
# CLR0 loader function to run setHueForAllFrames()
def set_hue_from_clr0(sender, event_args):
	hue = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	if hue is None:
		return
		
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			setHueForAllFrames(entry, hue)
	
	BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' hues set to hue '" + str(hue) + "'", "Success")

# CLR0Material loader function to run setHueForAllFrames()
def set_hue_from_material(sender, event_args):
	hue = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	if hue is None:
		return
	
	for entry in BrawlAPI.SelectedNode.Children:
		setHueForAllFrames(entry, hue)
	
	BrawlAPI.ShowMessage("All color frames set to hue '" + str(hue) + "' inside\n" + BrawlAPI.SelectedNode.Name, "Success")

# CLR0MaterialEntry loader function to run setHueForAllFrames()
def set_hue_from_mat_entry(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	hue = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	if hue is None:
		return
	setHueForAllFrames(selNode, hue)
	
	BrawlAPI.ShowMessage("All color frames set to hue '" + str(hue) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name, "Success")

# MDL0Color loader function to run setHueForAllFrames()
def set_hue_from_mdl0_vertex_color(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	hue = getUserValue(SET_HUE_VALUE_PROMPT, 0, 359)
	if hue is None:
		return
	
	if selNode.Parent and selNode.Parent.Parent: 
		parentMDL0 = BrawlAPI.SelectedNode.Parent.Parent
	
	setHueForAllFrames(selNode, hue)
	# Update parent MDL0 by exporting and re-importing
	updateParentMDL0(selNode)

	entryName = selNode.Name
	BrawlAPI.ShowMessage("All color frames set to hue '" + str(hue) + "' inside\n" + entryName, "Success")

# 2. END SET HUE
# 3. START SET VALUE
# CLR0 loader function to run adjustValForAllFrames()
def adjust_val_from_clr0(sender, event_args):
	val = getUserValue(SET_VAL_PROMPT, -100, 100)
	if val is None:
		return
	
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			adjustValForAllFrames(entry, val)
	
	BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' brightness adjusted by value '" + str(val) + "'", "Success")

# CLR0Material loader function to run adjustValForAllFrames()
def adjust_val_from_material(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	val = getUserValue(SET_VAL_PROMPT, -100, 100)
	if val is None:
		return
	
	for entry in selNode.Children:
		adjustValForAllFrames(entry, val)
	
	BrawlAPI.ShowMessage(str(len(selNode.Children)) + " animations' brightness adjusted by value '" + str(val) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name, "Success")

# CLR0MaterialEntry loader function to run adjustValForAllFrames()
def adjust_val_from_mat_entry(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	val = getUserValue(SET_VAL_PROMPT, -100, 100)
	if val is None:
		return
	adjustValForAllFrames(selNode, val)
	
	BrawlAPI.ShowMessage("All color frames' brightness adjusted by value '" + str(val) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name, "Success")

# MDL0Color loader function to run adjustValForAllFrames()
def adjust_val_mdl0_vertex_color(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	val = getUserValue(SET_VAL_PROMPT, -100, 100)
	if val is None:
		return
	
	if selNode.Parent and selNode.Parent.Parent: 
		parentMDL0 = BrawlAPI.SelectedNode.Parent.Parent
	
	adjustValForAllFrames(selNode, val)
	updateParentMDL0(selNode)
	
	entryName = selNode.Name
	BrawlAPI.ShowMessage("All color frames' brightness adjusted by value '" + str(val) + "' inside\n" + entryName, "Success")

# 3. END ADJUST VALUE
# 4. START ADJUST SATURATION
# CLR0 loader function to run adjustSatForAllFrames()
def adjust_sat_from_clr0(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	sat = getUserValue(SET_SAT_PROMPT, -100, 100)
	if sat is None:
		return
	
	for material in selNode.Children:
		for entry in material.Children:
			adjustSatForAllFrames(entry, sat)
	
	BrawlAPI.ShowMessage(str(len(selNode.Children)) + " animations' saturation adjusted by value '" + str(sat) + "'", "Success")

# CLR0Material loader function to run adjustSatForAllFrames()
def adjust_sat_from_material(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	sat = getUserValue(SET_SAT_PROMPT, -100, 100)
	if sat is None:
		return
	
	for node in selNode.Children:
		adjustSatForAllFrames(node, sat)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(selNode.Children)) + " animations' saturation adjusted by value '" + str(sat) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name, "Success")

# CLR0MaterialEntry loader function to run adjustSatForAllFrames()
def adjust_sat_from_mat_entry(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	sat = getUserValue(SET_SAT_PROMPT, -100, 100)
	if sat is None:
		return
	
	adjustSatForAllFrames(selNode, sat)
	
	BrawlAPI.ShowMessage("All color frames' saturation adjusted by value '" + str(sat) + "' inside\n" + selNode.Parent.Name + " > " + selNode.Name, "Success")

# MDL0Color loader function to run adjustSatForAllFrames()
def adjust_sat_mdl0_vertex_color(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	sat = getUserValue(SET_SAT_PROMPT, -100, 100)
	if sat is None:
		return
	
	if selNode.Parent and selNode.Parent.Parent: 
		parentMDL0 = BrawlAPI.SelectedNode.Parent.Parent
	
	adjustSatForAllFrames(selNode, sat)
	updateParentMDL0(selNode)
	
	entryName = selNode.Name
	BrawlAPI.ShowMessage("All color frames' saturation adjusted by value '" + str(sat) + "' inside\n" + entryName, "Success")
	
## End loader functions
## Start main functions

# Main function to iterate through frames and add (rotate) hue values
def rotateHueForAllFrames(node, hueToAdd):
	for i in range(node.ColorCount(1)):
			
		# If in a vertex color node or non-Constant CLR0 node, use frame color
		if "MDL0ColorNode" in node.NodeType or not node.Constant:
			frame = node.Colors[i]
		# If in a Constant color node
		else:
			frame = node.SolidColor
		
		HSV_as_List = RGB2HSV(frame)	# Get color as HSV value
		HSV_as_List[0] += hueToAdd		# Set hue to new
		new_RGB = HSV2RGB(HSV_as_List)	# Convert back to RGB
	
		# Set frame color to new RGB
		newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
		node.SetColor(i, i, newColor)	# i: index

# Main function to iterate through frames and set hue values
def setHueForAllFrames(node, newHue):
	for i in range(node.ColorCount(1)):
	
		# If in a vertex color node or non-Constant CLR0 node, use frame color
		if "MDL0ColorNode" in node.NodeType or not node.Constant:
			frame = node.Colors[i]
		# If in a Constant color node
		else:
			frame = node.SolidColor
		
		HSV_as_List = RGB2HSV(frame)	# Get color as HSV value
		HSV_as_List[0] = newHue			# Set hue to new
		new_RGB = HSV2RGB(HSV_as_List)	# Convert back to RGB
		
		# Set frame color to new RGB
		newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
		node.SetColor(i, i, newColor)

# Main function to iterate through frames and set brightness (val) values
# Exactly the same as rotateHueForAllFrames() except for the HSV list index. Don't feel like consolidating into one but could be simplified
def adjustValForAllFrames(node, valToAdd):
	for i in range(node.ColorCount(1)):
		
		if "MDL0ColorNode" in node.NodeType or not node.Constant:
			frame = node.Colors[i]
		else:
			frame = node.SolidColor
		
		HSV_as_List = RGB2HSV(frame)	# Get color as HSV value
		HSV_as_List[2] += valToAdd		# Set value to new
		new_RGB = HSV2RGB(HSV_as_List)	# Convert back to RGB
		
		# Set frame color to new RGB
		newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
		node.SetColor(i, i, newColor)

# Main function to iterate through frames and set saturation values
# Exactly the same as rotateHueForAllFrames() except for the HSV list index. Don't feel like consolidating into one but could be simplified
def adjustSatForAllFrames(node, valToAdd):
	for i in range(node.ColorCount(1)):
			
		if "MDL0ColorNode" in node.NodeType or not node.Constant:
			frame = node.Colors[i]
		else:
			frame = node.SolidColor
		
		HSV_as_List = RGB2HSV(frame)	# Get color as HSV value
		HSV_as_List[1] += valToAdd		# Set value to new
		new_RGB = HSV2RGB(HSV_as_List)	# Convert back to RGB
		
		# Set frame color to new RGB
		newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
		node.SetColor(i, i, newColor)	# i: index

## End main functions
## Start context menu add

# "Set hue" context options
# Set from CLR0
shortText = "Set hue"
longText = "Set the hue of all frames to a set value"
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", longText, EnableCheckCLR0, ToolStripMenuItem(shortText, None, set_hue_from_clr0))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", longText, EnableCheckCLR0Mat, ToolStripMenuItem(shortText, None, set_hue_from_material))
# Set from Material Entry (LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", longText, EnableCheckCLR0MatEntry, ToolStripMenuItem(shortText, None, set_hue_from_mat_entry))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, set_hue_from_mdl0_vertex_color))

# "Rotate hue" context options
# Set from CLR0
shortText = "Rotate hue"
longText = "Rotate the hue of all frames by a set value"
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", longText, EnableCheckCLR0, ToolStripMenuItem(shortText, None, rotate_hue_from_clr0))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", longText, EnableCheckCLR0Mat, ToolStripMenuItem(shortText, None, rotate_hue_from_material))
# Set from CLR0 Material Entry (LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", longText, EnableCheckCLR0MatEntry, ToolStripMenuItem(shortText, None, rotate_hue_from_mat_entry))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, rotate_hue_from_mdl0_vertex_color))

# "Adjust brightness" context options
# Set from CLR0
shortText = "Adjust brightness"
longText = "Adjust brightness value of all frames by a set value"
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", longText, EnableCheckCLR0, ToolStripMenuItem(shortText, None, adjust_val_from_clr0))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", longText, EnableCheckCLR0Mat, ToolStripMenuItem(shortText, None, adjust_val_from_material))
# Set from CLR0 Material Entry LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", longText, EnableCheckCLR0MatEntry, ToolStripMenuItem(shortText, None, adjust_val_from_mat_entry))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, adjust_val_mdl0_vertex_color))

# "Adjust saturation" context options
# Set from CLR0
shortText = "Adjust saturation"
longText = "Adjust saturation of all frames by a set value"
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", longText, EnableCheckCLR0, ToolStripMenuItem(shortText, None, adjust_sat_from_clr0))
# Set from CLR0 Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", longText, EnableCheckCLR0Mat, ToolStripMenuItem(shortText, None, adjust_sat_from_material))
# Set from CLR0 Material Entry LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", longText, EnableCheckCLR0MatEntry, ToolStripMenuItem(shortText, None, adjust_sat_from_mat_entry))
# Set from MDL0 Vertex color
BrawlAPI.AddContextMenuItem(MDL0ColorWrapper, "", longText, EnableCheckMDL0Color, ToolStripMenuItem(shortText, None, adjust_sat_mdl0_vertex_color))
