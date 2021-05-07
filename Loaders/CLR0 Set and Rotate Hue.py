__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from BrawlLib import * # Imaging
from BrawlLib.Imaging import * # Imaging

successCheck = False	# Global check to determine whether success prompt should be shown

SET_HUE_VALUE_PROMPT = "Enter hue value to set (0 to 359)"
ROTATE_HUE_VALUE_PROMPT = "Enter hue value to adjust by (-180 to 180)"

## Start enable check functions
# Check to ensure the context menu item can be active
# Wrapper: CLR0MaterialEntryWrapper
def EnableCheckCLR0MatEntry(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None)

# Wrapper: CLR0MaterialWrapper	
def EnableCheckCLR0Mat(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and BrawlAPI.SelectedNode.HasChildren)
	
# Wrapper: CLR0Wrapper
def EnableCheckCLR0(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and BrawlAPI.SelectedNode.HasChildren)

## End enable check functions
## Start helper functions
# Prompt user for hue value at the start of script. Use a string input to allow for 0
def getHueValue(promptText, minValue, maxValue, exitValue=-1):
	userInput = BrawlAPI.UserStringInput(promptText)
	
	# If user closes prompt or gives bad input, return exitValue
	if not userInput:
		return exitValue
	elif userInput == "0" or userInput == "360":
		return 0
	elif int(userInput) < minValue or int(userInput) > maxValue:
		BrawlAPI.ShowError("Invalid input", "Error")
		return exitValue
	else:
		return int(userInput)
	
# Given an array of 3 numbers, return an array of 3 ints corresponding to the RGB values
# Hue in [0, 359], sat in [0,1], val in [0,1]
def HSV2RGB(colorList):
	[HUE, SAT, VAL] = colorList
	
	# Some formula calcs
	cValue = float(VAL * SAT)
	xValue = cValue * (1.0 - abs((HUE / 60.0) % 2 - 1.0))
	mValue = VAL - cValue
	
	# Keep hue value in [0, 359] range
	while HUE < 0:
		HUE = HUE + 360
	while HUE > 360:
		HUE = HUE - 360
	
	if HUE >= 0 and HUE < 60:
		[red, green, blue] = [cValue, xValue, 0]
	elif HUE >= 60 and HUE < 120:
		[red, green, blue] = [xValue, cValue, 0]
	elif HUE >= 120 and HUE < 180:
		[red, green, blue] = [0, cValue, xValue]
	elif HUE >= 180 and HUE < 240:
		[red, green, blue] = [0, xValue, cValue]
	elif HUE >= 240 and HUE < 300:
		[red, green, blue] = [xValue, 0, cValue]
	else:
		[red, green, blue] = [cValue, 0, xValue]
	
	red = int((red + mValue) * 255.0)
	green = int((green + mValue) * 255.0)
	blue = int((blue + mValue) * 255.0)
	
	return [red, green, blue]

# Given a color entry, return an array of 3 floats corresponding to the HSV values
def RGB2HSV(colorNode):
	RED = colorNode.R / 255.0
	BLUE = colorNode.B / 255.0
	GREEN = colorNode.G / 255.0
	colorMax = max(RED, BLUE, GREEN)
	colorMin = min(RED, BLUE, GREEN)
	colorDiff = colorMax - colorMin
	
	# If hue not 0, calculate hue as value 0..359
	if colorDiff == 0:
		hue = 0
	elif colorMax == RED:
		hue = ((GREEN - BLUE) / colorDiff) % 6
	elif colorMax == GREEN:
		hue = ((BLUE - RED) / colorDiff) + 2.0
	else:
		hue = ((RED - GREEN) / colorDiff) + 4.0

	hue = (hue * 60.0) % 360
	
	# Calculate saturation as [0,1]
	if colorMax > 0:
		sat = colorDiff / colorMax
	else:
		sat = 0
		
	# Calculate value (highest color) as [0,1]
	val = colorMax
	
	return [hue, sat, val]

## End helper functions
## Start loader functions

# Initial loader functions to run rotateHueForAllFrames()
def rotate_hue_from_clr0(sender,event_args):
	hue = getHueValue(ROTATE_HUE_VALUE_PROMPT, -180, 180, -999)
	
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			rotateHueForAllFrames(entry, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' hues rotated by hue '" + str(hue) + "'", "Success")

def rotate_hue_from_material(sender, event_args):
	hue = getHueValue(ROTATE_HUE_VALUE_PROMPT, -180, 180, -999)
	
	for entry in BrawlAPI.SelectedNode.Children:
		rotateHueForAllFrames(entry, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames rotated by hue '" + str(hue) + "' inside\n" + BrawlAPI.SelectedNode.Name, "Success")

# Initial loader functions to run setHueForAllFrames()
def set_hue_from_clr0(sender, event_args):
	hue = getHueValue(SET_HUE_VALUE_PROMPT, 0, 359)
	
	for material in BrawlAPI.SelectedNode.Children:
		for entry in material.Children:
			setHueForAllFrames(entry, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage(str(len(BrawlAPI.SelectedNode.Children)) + " animations' hues set to hue '" + str(hue) + "'", "Success")

def set_hue_from_material(sender, event_args):
	hue = getHueValue(SET_HUE_VALUE_PROMPT, 0, 359)
	
	for entry in BrawlAPI.SelectedNode.Children:
		setHueForAllFrames(entry, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames set to hue '" + str(hue) + "' inside\n" + BrawlAPI.SelectedNode.Name, "Success")

def set_hue_from_mat_entry(sender, event_args):
	hue = getHueValue(SET_HUE_VALUE_PROMPT, 0, 359)
	setHueForAllFrames(BrawlAPI.SelectedNode, hue)
	
	if successCheck:
		BrawlAPI.ShowMessage("All color frames set to hue '" + str(hue) + "' inside\n" + node.Parent.Name + " > " + node.Name, "Success")

def rotate_hue_from_mat_entry(sender, event_args):
	hue = getHueValue(ROTATE_HUE_VALUE_PROMPT, -180, 180, -999)
	rotateHueForAllFrames(BrawlAPI.SelectedNode, hue)
	
	if successCheck:
		entryName = BrawlAPI.SelectedNode.Name
		materialName = BrawlAPI.SelectedNode.Parent.Name
		BrawlAPI.ShowMessage("All color frames rotated by hue '" + str(hue) + "' inside\n" + materialName + " > " + entryName, "Success")

## End loader functions
## Start main functions

# Main function to iterate through frames and add (rotate) hue values
def rotateHueForAllFrames(node, hueToAdd):
	global successCheck
	successCheck = False

	if hueToAdd >= -180:
		for i in range (0, node.ColorCount(1),1):
			frame = node.Colors[i]
			# Get color as HSV value
			HSV_as_List = RGB2HSV(frame)
			
			# Set hue to new
			HSV_as_List[0] = HSV_as_List[0] + hueToAdd

			# Convert back to RGB
			new_RGB = HSV2RGB(HSV_as_List)
			
			# Set frame color to new RGB
			newColor = ARGBPixel(frame.A, new_RGB[0], new_RGB[1], new_RGB[2])
			node.SetColor(i, i, newColor)
		
		successCheck = True

# Main function to iterate through frames and set hue values
def setHueForAllFrames(node, newHue):
	global successCheck
	successCheck = False
	if newHue > -1:
		for i in range(0,node.ColorCount(1),1):
			frame = node.Colors[i]
			
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

## End main functions
## Start context menu add

# "Set hue" context options
# Set from Material Entry (LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", "Set the hue of all frames to a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Set hue (all frames)", None, set_hue_from_mat_entry))
# Set from Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", "Set the hue of all frames to a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Set hue (all entries)", None, set_hue_from_material))
# Set from CLR0
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Set the hue of all frames to a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Set hue (all entries)", None, set_hue_from_clr0))

# "Rotate hue" context options
# Set from Material Entry (LightChannel0MaterialColor)
BrawlAPI.AddContextMenuItem(CLR0MaterialEntryWrapper, "", "Rotate the hue of all frames by a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Rotate hue (all frames)", None, rotate_hue_from_mat_entry))
# Set from Material
BrawlAPI.AddContextMenuItem(CLR0MaterialWrapper, "", "Rotate the hue of all frames by a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Rotate hue (all entries)", None, rotate_hue_from_material))
# Set from CLR0
BrawlAPI.AddContextMenuItem(CLR0Wrapper, "", "Rotate the hue of all frames by a defined integer", EnableCheckCLR0MatEntry, ToolStripMenuItem("Rotate hue (all entries)", None, rotate_hue_from_clr0))