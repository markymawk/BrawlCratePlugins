__author__ = "mawwwk"
__version__ = "1.1.2"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import *
from mawwwkLib import *

SCRIPT_NAME = "Copy StgPosition and STPM Camera"
MODELDATA_BRRES_NAME = "Model Data [100]"
TEMP_BRRES_PATH = AppPath + "\ModelData100.brres"
TEMP_STPM_PATH = AppPath + "\STPM.stpm"

## Start enable check function

# Check to ensure that the BRES is a ModelData 100 within a stage pac
# Wrapper: BRESWrapper
def EnableCheckBRES(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.Name == MODELDATA_BRRES_NAME \
	and node.Parent and node.Parent.Name == "2")

# Check to ensure that the BRES is a ModelData 100 within a stage pac
# Wrapper: MDL0Wrapper
def EnableCheckMDL0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.IsStagePosition and node.Parent \
	and node.Parent.Parent and node.Parent.Parent.Name == MODELDATA_BRRES_NAME)

# Wrapper: STPMWrapper
def EnableCheckSTPM(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.Parent and node.HasChildren)

# Wrapper: GenericWrapper
def EnableCheckSTPMEntry(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.Parent and isinstance(node.Parent, STPMNode) and node.Parent.Parent)

## End enable check function
## Start helper functions

# Get STPM node by navigating via RootNode
def getSTPMEntryNode():
	mainARC = BrawlAPI.RootNode.FindChild("2")
	stpmParentNode = findChildByName(mainARC, "Stage Parameters")
	if stpmParentNode:
		return stpmParentNode.Children[0]
	else:
		return 0

def setSTPMCameraValues(stpm_node, cameraValList):
	stpmChanged = []
	
	listIndex = 0
	# Set FOV
	if (stpm_node.CameraFOV != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.CameraFOV = cameraValList[listIndex]
	
	listIndex += 1
	# Set MinimumZ
	if (stpm_node.MinimumZ != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.MinimumZ = cameraValList[listIndex]
	
	listIndex += 1
	# Set MaximumZ
	if (stpm_node.MaximumZ != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.MaximumZ = cameraValList[listIndex]
	
	listIndex += 1
	# Set HorizontalRotationFactor
	if (stpm_node.HorizontalRotationFactor != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.HorizontalRotationFactor = cameraValList[listIndex]
		
	listIndex += 1
	# Set VerticalRotationFactor
	if (stpm_node.VerticalRotationFactor != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.VerticalRotationFactor = cameraValList[listIndex]
	
	listIndex += 1
	# Set CharacterBubbleBufferMultiplier
	if (stpm_node.CharacterBubbleBufferMultiplier != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.CharacterBubbleBufferMultiplier = cameraValList[listIndex]
	
	listIndex += 1
	# Set CameraSpeed
	if (stpm_node.CameraSpeed != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.CameraSpeed = cameraValList[listIndex]
	
	listIndex += 1
	# Set StarKOCamTilt
	if (stpm_node.StarKOCamTilt != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.StarKOCamTilt = cameraValList[listIndex]
	
	listIndex += 1
	# Set FinalSmashCamTilt
	if (stpm_node.FinalSmashCamTilt != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.FinalSmashCamTilt = cameraValList[listIndex]
	
	listIndex += 1
	# Set CameraRight
	if (stpm_node.CameraRight != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.CameraRight = cameraValList[listIndex]
	
	listIndex += 1
	# Set CameraLeft
	if (stpm_node.CameraLeft != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.CameraLeft = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamX
	if (stpm_node.PauseCamX != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamX = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamY
	if (stpm_node.PauseCamY != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamY = cameraValList[listIndex]
		
	listIndex += 1
	# Set PauseCamZ
	if (stpm_node.PauseCamZ != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamZ = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamAngle
	if (stpm_node.PauseCamAngle != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamAngle = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamZoomIn
	if (stpm_node.PauseCamZoomIn != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamZoomIn = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamZoomDefault
	if (stpm_node.PauseCamZoomDefault != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamZoomDefault = cameraValList[listIndex]
		
	listIndex += 1
	# Set PauseCamZoomOut
	if (stpm_node.PauseCamZoomOut != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamZoomOut = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamRotYMin
	if (stpm_node.PauseCamRotYMin != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamRotYMin = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamRotYMax
	if (stpm_node.PauseCamRotYMax != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamRotYMax = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamRotXMin
	if (stpm_node.PauseCamRotXMin != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamRotXMin = cameraValList[listIndex]
	
	listIndex += 1
	# Set PauseCamRotXMax
	if (stpm_node.PauseCamRotXMax != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PauseCamRotXMax = cameraValList[listIndex]
	
	listIndex += 1
	# Set FixedCamX
	if (stpm_node.FixedCamX != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.FixedCamX = cameraValList[listIndex]
	
	listIndex += 1
	# Set FixedCamY
	if (stpm_node.FixedCamY != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.FixedCamY = cameraValList[listIndex]
	
	listIndex += 1
	# Set FixedCamZ
	if (stpm_node.FixedCamZ != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.FixedCamZ = cameraValList[listIndex]
	
	listIndex += 1
	# Set FixedCamFOV
	if (stpm_node.FixedCamFOV != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.FixedCamFOV = cameraValList[listIndex]
	
	listIndex += 1
	# Set OlimarFinalCamAngle
	if (stpm_node.OlimarFinalCamAngle != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.OlimarFinalCamAngle = cameraValList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalPosX
	if (stpm_node.IceClimbersFinalPosX != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.IceClimbersFinalPosX = cameraValList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalPosY
	if (stpm_node.IceClimbersFinalPosY != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.IceClimbersFinalPosY = cameraValList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalPosZ
	if (stpm_node.IceClimbersFinalPosZ != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.IceClimbersFinalPosZ = cameraValList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalScaleX
	if (stpm_node.IceClimbersFinalScaleX != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.IceClimbersFinalScaleX = cameraValList[listIndex]
	
	listIndex += 1
	# Set IceClimbersFinalScaleY
	if (stpm_node.IceClimbersFinalScaleY != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.IceClimbersFinalScaleY = cameraValList[listIndex]
	
	listIndex += 1
	# Set PitFinalPalutenaScale
	if (stpm_node.PitFinalPalutenaScale != cameraValList[listIndex]):
		stpmChanged.append(listIndex)
		stpm_node.PitFinalPalutenaScale = cameraValList[listIndex]
	
	return stpmChanged

def getSTPMCameraValueList(stpm_node):
	cameraValList = [
		stpm_node.CameraFOV,
		stpm_node.MinimumZ,
		stpm_node.MaximumZ,
		stpm_node.HorizontalRotationFactor,
		stpm_node.VerticalRotationFactor,
		stpm_node.CharacterBubbleBufferMultiplier,
		stpm_node.CameraSpeed,
		stpm_node.StarKOCamTilt,
		stpm_node.FinalSmashCamTilt,
		stpm_node.CameraRight,
		stpm_node.CameraLeft,
		stpm_node.PauseCamX,
		stpm_node.PauseCamY,
		stpm_node.PauseCamZ,
		stpm_node.PauseCamAngle,
		stpm_node.PauseCamZoomIn,
		stpm_node.PauseCamZoomDefault,
		stpm_node.PauseCamZoomOut,
		stpm_node.PauseCamRotYMin,
		stpm_node.PauseCamRotYMax,
		stpm_node.PauseCamRotXMin,
		stpm_node.PauseCamRotXMax,
		stpm_node.FixedCamX,
		stpm_node.FixedCamY,
		stpm_node.FixedCamZ,
		stpm_node.FixedCamFOV,
		stpm_node.OlimarFinalCamAngle,
		stpm_node.IceClimbersFinalPosX,
		stpm_node.IceClimbersFinalPosY,
		stpm_node.IceClimbersFinalPosZ,
		stpm_node.IceClimbersFinalScaleX,
		stpm_node.IceClimbersFinalScaleY,
		stpm_node.PitFinalPalutenaScale
	]
	return cameraValList

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
	
	if brresNode:
		main(brresNode, selNode.Children[0])
	else:
		BrawlAPI.ShowError("Error finding StgPosition brres", "Error")
		

# Loader function from STPMEntryNode
def export_data_stpmEntryNode(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	brresNode = selNode.Parent.Parent.FindChild(MODELDATA_BRRES_NAME)
	
	if brresNode:
		main(brresNode, selNode)
	else:
		BrawlAPI.ShowError("Error finding StgPosition brres", "Error")

## End loader function
## Start main function

def main(brresNode, stpm_node):
	
	# Prompt for filename substring to check for
	stageString = BrawlAPI.UserStringInput("Enter stage substring (e.g. \"_BF_\")")
	if stageString == "" or stageString == None:
		return
	
	# Export stgPosition brres to temp brres file
	brresNode.ExportUncompressed(TEMP_BRRES_PATH)
	
	# Store source STPM camera values in originalSTPMCameraProperties[]
	originalSTPMCameraProperties = getSTPMCameraValueList(stpm_node)
	
	# Get list of stage pacs in the same folder as the opened file
	sourceFilePath = str(BrawlAPI.RootNode.FilePath)
	stageMeleeDirPath = getParentFolderPath(sourceFilePath)
	stageFilePathList = Directory.CreateDirectory(stageMeleeDirPath).GetFiles()
	
	# Get hash of selected node, to compare with new nodes
	originalHash = brresNode.MD5Str()
	
	# List of files found with the given substring
	matchingFilesCount = 0
	filesModified = []
	
	# Check each pac file in stage/melee for the given substring
	for file in stageFilePathList:
		if stageString in file.Name and file.FullName != sourceFilePath:
			matchingFilesCount += 1
			BrawlAPI.OpenFile(file.FullName)
			
			# Find Model Data 100 node
			parentARC = getParentArc()
			if not parentARC:
				continue
			newBRRES = parentARC.FindChild(MODELDATA_BRRES_NAME)
			
			# If hashes aren't identical, replace the brres and save
			if newBRRES and not originalHash == newBRRES.MD5Str():
				newBRRES.Replace(TEMP_BRRES_PATH)
				filesModified.append(file.Name)
				BrawlAPI.SaveFile()
			
			# Compare STPM and update. If no node found, move to next file
			newSTPMEntryNode = getSTPMEntryNode()
			if not newSTPMEntryNode:
				continue
			
			entriesChanged = setSTPMCameraValues(newSTPMEntryNode, originalSTPMCameraProperties)
			
			if len(entriesChanged):
				if file.Name not in filesModified:
					filesModified.append(file.Name)
				BrawlAPI.SaveFile()
	
	# After checking all files, open the original stage pac again
	BrawlAPI.OpenFile(sourceFilePath)
	
	# Delete temp brres file
	File.Delete(TEMP_BRRES_PATH)
	
	msg = str(matchingFilesCount) + " stage .pac file(s) found with substring \"" + stageString + "\"\n"
	
	# If any files modified, list them
	if len(filesModified):
		msg += str(len(filesModified)) + " file(s) edited:\n\n"
		msg += listToString(filesModified)
	
	# Otherwise, no mismatches found
	elif len(filesFound):
		msg += "\nNo mismatching " + MODELDATA_BRRES_NAME + " or STPM data found"
	
	BrawlAPI.ShowMessage(msg, SCRIPT_NAME)

## End main function
## Start context menu add

LONG_TEXT = "Export StgPosition and STPM Camera data to other stage .pac files"
SHORT_TEXT = "Copy StgPosition, STPM Camera to 1:1s"

# From parent BRRES
BrawlAPI.AddContextMenuItem(BRESWrapper, "", LONG_TEXT, EnableCheckBRES, ToolStripMenuItem(SHORT_TEXT, None, export_data_stgPosBRRES))

# From stgPosition MDL0 (export BRRES)
BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", LONG_TEXT, EnableCheckMDL0, ToolStripMenuItem(SHORT_TEXT, None, export_data_stgPosMDL0))

# From STPMNode
BrawlAPI.AddContextMenuItem(STPMWrapper, "", LONG_TEXT, EnableCheckSTPM, ToolStripMenuItem(SHORT_TEXT, None, export_data_stpmnode))

# From STPMEntryNode (GenericWrapper)
BrawlAPI.AddContextMenuItem(GenericWrapper, "", LONG_TEXT, EnableCheckSTPMEntry, ToolStripMenuItem(SHORT_TEXT, None, export_data_stpmEntryNode))