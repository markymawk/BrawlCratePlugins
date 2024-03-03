__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import *
from mawwwkLib import *

SCRIPT_NAME = "Match All StgPosition BRRES"
MODELDATA_BRRES_NAME = "Model Data [100]"
TEMP_BRRES_PATH = AppPath + "\ModelData100.brres"
TEMP_STPM_PATH = AppPath + "\STPM.stpm"

## Start enable check function

# Check to ensure that the BRES is a ModelData 100 within a stage pac
# Wrapper: BRESWrapper
def EnableCheckBRES(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Name == MODELDATA_BRRES_NAME \
	and node.Parent and node.Parent.Name == "2")
	
# Check to ensure that the BRES is a ModelData 100 within a stage pac
# Wrapper: MDL0Wrapper
def EnableCheckMDL0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.IsStagePosition and node.Parent \
	and node.Parent.Parent and node.Parent.Parent.Name == MODELDATA_BRRES_NAME)

# Wrapper: STPMWrapper
def EnableCheckSTPM(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Parent and node.HasChildren)

# Wrapper: GenericWrapper
def EnableCheckSTPMEntry(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Parent and isinstance(node.Parent.NodeType, STPMNode) and node.Parent.Parent)

## End enable check function
## Start helper functions

# Get STPM node by navigating via RootNode
def getSTPMEntryNode():
	mainARC = BrawlAPI.RootNode.FindChild("2")
	STPMParentNode = getChildByName(mainARC, "Stage Parameters")
	if STPMParentNode:
		return STPMParentNode.Children[0]
	# If no STPM, i.e. DualLoad stages
	else:
		return 0

# Generate python list of relevant STPM camera values	
def getSTPMCameraValueList(STPMNode):
	cameraValList = [
		STPMNode.CameraFOV,
		STPMNode.MinimumZ,
		STPMNode.MaximumZ,
		STPMNode.HorizontalRotationFactor,
		STPMNode.VerticalRotationFactor,
		STPMNode.CharacterBubbleBufferMultiplier,
		STPMNode.CameraSpeed,
		STPMNode.StarKOCamTilt,
		STPMNode.FinalSmashCamTilt,
		STPMNode.CameraRight,
		STPMNode.CameraLeft,
		STPMNode.PauseCamX,
		STPMNode.PauseCamY,
		STPMNode.PauseCamZ,
		STPMNode.PauseCamAngle,
		STPMNode.PauseCamZoomIn,
		STPMNode.PauseCamZoomDefault,
		STPMNode.PauseCamZoomOut,
		STPMNode.PauseCamRotYMin,
		STPMNode.PauseCamRotYMax,
		STPMNode.PauseCamRotXMin,
		STPMNode.PauseCamRotXMax,
		STPMNode.FixedCamX,
		STPMNode.FixedCamY,
		STPMNode.FixedCamZ,
		STPMNode.FixedCamFOV,
		STPMNode.OlimarFinalCamAngle,
		STPMNode.IceClimbersFinalPosX,
		STPMNode.IceClimbersFinalPosY,
		STPMNode.IceClimbersFinalPosZ,
		STPMNode.IceClimbersFinalScaleX,
		STPMNode.IceClimbersFinalScaleY,
		STPMNode.PitFinalPalutenaScale
	]
	return cameraValList

def setSTPMCameraValues(STPMNode, cameraPropList):
	stpmChanged = []
	listIndex = 0
	# Set FOV
	if (STPMNode.CameraFOV != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.CameraFOV = cameraPropList[listIndex]
	
	listIndex += 1
	# Set MinimumZ
	if (STPMNode.MinimumZ != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.MinimumZ = cameraPropList[listIndex]
	
	listIndex += 1
	# Set MaximumZ
	if (STPMNode.MaximumZ != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.MaximumZ = cameraPropList[listIndex]
	
	listIndex += 1
	# Set HorizontalRotationFactor
	if (STPMNode.HorizontalRotationFactor != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.HorizontalRotationFactor = cameraPropList[listIndex]
		
	listIndex += 1
	# Set VerticalRotationFactor
	if (STPMNode.VerticalRotationFactor != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.VerticalRotationFactor = cameraPropList[listIndex]
	
	listIndex += 1
	# Set CharacterBubbleBufferMultiplier
	if (STPMNode.CharacterBubbleBufferMultiplier != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.CharacterBubbleBufferMultiplier = cameraPropList[listIndex]
	
	listIndex += 1
	# Set CameraSpeed
	if (STPMNode.CameraSpeed != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.CameraSpeed = cameraPropList[listIndex]
	
	listIndex += 1
	# Set StarKOCamTilt
	if (STPMNode.StarKOCamTilt != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.StarKOCamTilt = cameraPropList[listIndex]
	
	listIndex += 1
	# Set FinalSmashCamTilt
	if (STPMNode.FinalSmashCamTilt != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.FinalSmashCamTilt = cameraPropList[listIndex]
	
	listIndex += 1
	# Set CameraRight
	if (STPMNode.CameraRight != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.CameraRight = cameraPropList[listIndex]
	
	listIndex += 1
	# Set CameraLeft
	if (STPMNode.CameraLeft != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.CameraLeft = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamX
	if (STPMNode.PauseCamX != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamX = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamY
	if (STPMNode.PauseCamY != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamY = cameraPropList[listIndex]
		
	listIndex += 1
	# Set PauseCamZ
	if (STPMNode.PauseCamZ != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamZ = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamAngle
	if (STPMNode.PauseCamAngle != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamAngle = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamZoomIn
	if (STPMNode.PauseCamZoomIn != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamZoomIn = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamZoomDefault
	if (STPMNode.PauseCamZoomDefault != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamZoomDefault = cameraPropList[listIndex]
		
	listIndex += 1
	# Set PauseCamZoomOut
	if (STPMNode.PauseCamZoomOut != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamZoomOut = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamRotYMin
	if (STPMNode.PauseCamRotYMin != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamRotYMin = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamRotYMax
	if (STPMNode.PauseCamRotYMax != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamRotYMax = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamRotXMin
	if (STPMNode.PauseCamRotXMin != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamRotXMin = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PauseCamRotXMax
	if (STPMNode.PauseCamRotXMax != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PauseCamRotXMax = cameraPropList[listIndex]
	
	listIndex += 1
	# Set FixedCamX
	if (STPMNode.FixedCamX != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.FixedCamX = cameraPropList[listIndex]
	
	listIndex += 1
	# Set FixedCamY
	if (STPMNode.FixedCamY != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.FixedCamY = cameraPropList[listIndex]
	
	listIndex += 1
	# Set FixedCamZ
	if (STPMNode.FixedCamZ != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.FixedCamZ = cameraPropList[listIndex]
	
	listIndex += 1
	# Set FixedCamFOV
	if (STPMNode.FixedCamFOV != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.FixedCamFOV = cameraPropList[listIndex]
	
	listIndex += 1
	# Set OlimarFinalCamAngle
	if (STPMNode.OlimarFinalCamAngle != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.OlimarFinalCamAngle = cameraPropList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalPosX
	if (STPMNode.IceClimbersFinalPosX != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.IceClimbersFinalPosX = cameraPropList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalPosY
	if (STPMNode.IceClimbersFinalPosY != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.IceClimbersFinalPosY = cameraPropList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalPosZ
	if (STPMNode.IceClimbersFinalPosZ != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.IceClimbersFinalPosZ = cameraPropList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalScaleX
	if (STPMNode.IceClimbersFinalScaleX != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.IceClimbersFinalScaleX = cameraPropList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalScaleY
	if (STPMNode.IceClimbersFinalScaleY != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.IceClimbersFinalScaleY = cameraPropList[listIndex]
	
	listIndex += 1
	# Set PitFinalPalutenaScale
	if (STPMNode.PitFinalPalutenaScale != cameraPropList[listIndex]):
		stpmChanged.append(listIndex)
		STPMNode.PitFinalPalutenaScale = cameraPropList[listIndex]
	
	return stpmChanged

## End helper functions
## Start loader function

# Loader function from BRRES (Model Data 100)
def export_data_stgPosBRRES(sender, event_args):
	STPMEntryNode = getSTPMEntryNode()
	main(BrawlAPI.SelectedNode, STPMEntryNode)

# Loader function from StgPosition mdl0
def export_data_stgPosMDL0(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	STPMEntryNode = getSTPMEntryNode()
	if selNode.Parent and selNode.Parent.Parent and isinstance(selNode.Parent.Parent,BRRESNode):
		main(selNode.Parent.Parent, STPMEntryNode)
	else:
		BrawlAPI.ShowError("Error exporting parent BRRES", "Error")

# Loader function from STPMNode (parent to STPMEntryNode)
def export_data_stpmnode(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	brresNode = selNode.Parent.FindChild(MODELDATA_BRRES_NAME)
	if not brresNode:	
		BrawlAPI.ShowError("Error finding StgPosition brres", "Error")
		return
		
	main(brresNode, selNode.Children[0])

# Loader function from STPMEntryNode
def export_data_stpmEntryNode(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	brresNode = selNode.Parent.Parent.FindChild(MODELDATA_BRRES_NAME)
	if not brresNode:	
		BrawlAPI.ShowError("Error finding StgPosition brres", "Error")
		return
		
	main(brresNode, selNode)

## End loader function
## Start main function

def main(brresNode, STPMNode):
	# Prompt for filename substring to check for
	stageString = BrawlAPI.UserStringInput("Enter stage substring (e.g. \"_BF\")")
	if stageString == "" or stageString == None:
		return
	
	SOURCE_FILE = str(BrawlAPI.RootNode.FilePath)
	
	# Export stgPosition brres to temp brres file
	brresNode.ExportUncompressed(TEMP_BRRES_PATH)
	
	# Store STPM camera values
	originalSTPMCameraProperties = getSTPMCameraValueList(STPMNode)
	
	# Get list of stage pacs in the same folder as the opened file
	STAGE_MELEE_PATH = str(BrawlAPI.RootNode.FilePath).rsplit("\\", 1)[0]
	STAGE_FILES = Directory.CreateDirectory(STAGE_MELEE_PATH).GetFiles()
	
	# Get hash of selected node, to compare with new nodes
	originalHash = brresNode.MD5Str()
	
	# List of files found with the given substring
	filesFound = []
	# List of modified files
	filesModified = []
	
	# Check each pac file in stage/melee for the given substring
	for file in STAGE_FILES:
		if stageString in file.Name and file.FullName != SOURCE_FILE:
			filesFound.append(file.Name)
			
			# Find Model Data 100 node
			BrawlAPI.OpenFile(file.FullName)
			newBRRES = getChildFromName(getParentArc(), MODELDATA_BRRES_NAME, True)
			
			# If hashes aren't identical, replace the brres and save
			if newBRRES and not originalHash == newBRRES.MD5Str():
				newBRRES.Replace(TEMP_BRRES_PATH)
				filesModified.append(file.Name)
				BrawlAPI.SaveFile()
			
			# Compare STPM and update. If no node found, move to next file
			newSTPMEntryNode = getSTPMEntryNode()
			if not newSTPMEntryNode:
				continue
			
			fileChanged = setSTPMCameraValues(newSTPMEntryNode, originalSTPMCameraProperties)
			
			if len(fileChanged):
				if file.Name not in filesModified:
					filesModified.append(file.Name)
				BrawlAPI.SaveFile()
	
	# After checking all files, open the original stage pac again
	BrawlAPI.OpenFile(SOURCE_FILE)
	
	# Delete temp brres file
	File.Delete(TEMP_BRRES_PATH)
	
	msg = str(len(filesFound)) + " stage file(s) found with substring \"" + stageString + "\"\n"
	
	# If any files modified, list them
	if len(filesModified):
		msg += str(len(filesModified)) + " file(s) edited:\n\n"
		
		for file in filesModified:
			msg += file + "\n"
		BrawlAPI.ShowMessage(msg, "Success!")
	
	# Otherwise, no mismatches found
	elif len(filesFound):
		BrawlAPI.ShowMessage(msg + "\nNo mismatching " + MODELDATA_BRRES_NAME + " or STPM data found", "Complete")

## End main function
## Start context menu add

LONG_TEXT = "Export StgPosition and STPM Camera data to other stages"
SHORT_TEXT = "Copy StgPosition, STPM Camera to 1:1s"

# From parent BRRES
BrawlAPI.AddContextMenuItem(BRESWrapper, "", LONG_TEXT, EnableCheckBRES, ToolStripMenuItem(SHORT_TEXT, None, export_data_stgPosBRRES))

# From stgPosition MDL0 (export BRRES)
BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", LONG_TEXT, EnableCheckMDL0, ToolStripMenuItem(SHORT_TEXT, None, export_data_stgPosMDL0))

# From STPMNode
BrawlAPI.AddContextMenuItem(STPMWrapper, "", LONG_TEXT, EnableCheckSTPM, ToolStripMenuItem(SHORT_TEXT, None, export_data_stpmnode))

# From STPMEntryNode (GenericWrapper)
BrawlAPI.AddContextMenuItem(GenericWrapper, "", LONG_TEXT, EnableCheckSTPMEntry, ToolStripMenuItem(SHORT_TEXT, None, export_data_stpmEntryNode))