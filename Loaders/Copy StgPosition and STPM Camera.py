__author__ = "mawwwk"
__version__ = "2.0"

from BrawlCrate.UI import * # MainForm CompabibilityMode
from BrawlCrate.NodeWrappers import *
from BrawlCrate.API.BrawlAPI import AppPath
from System.Windows.Forms import ToolStripMenuItem
from System.IO import *
from mawwwkLib import *

SCRIPT_NAME = "Copy StgPosition and STPM Camera"
TEMP_BRRES_PATH = AppPath + "\ModelDataStgPosition.brres"
TEMP_STPM_PATH = AppPath + "\STPM.stpm"
# MODELDATA_BRRES_NAME used only when run via STPM; runs on selected BRRES otherwise
MODELDATA_BRRES_NAME = "Model Data [100]" 

STPM_PROP_NAME_LIST = [
	"CameraFOV",
	"MinimumZ",
	"MaximumZ",
	"HorizontalRotationFactor",
	"VerticalRotationFactor",
	"CharacterBubbleBufferMultiplier",
	"CameraSpeed",
	"StarKOCamTilt",
	"FinalSmashCamTilt",
	"CameraRight",
	"CameraLeft",
	"PauseCamX",
	"PauseCamY",
	"PauseCamZ",
	"PauseCamAngle",
	"PauseCamZoomIn",
	"PauseCamZoomDefault",
	"PauseCamZoomOut",
	"PauseCamRotYMin",
	"PauseCamRotYMax",
	"PauseCamRotXMin",
	"PauseCamRotXMax",
	"FixedCamX",
	"FixedCamY",
	"FixedCamZ",
	"FixedCamFOV",
	"OlimarFinalCamAngle",
	"IceClimbersFinalPosX",
	"IceClimbersFinalPosY",
	"IceClimbersFinalPosZ",
	"IceClimbersFinalScaleX",
	"IceClimbersFinalScaleY",
	"PitFinalPalutenaScale"
	]

STAGE_NAME_SHORTCUTS = {
	"battlefield" : "BF",
	"bowsercastle" : "BC",
	"ceresspacecolony" : "CSC",
	"delfinosecret" : "DS",
	"distantplanet" : "DP",
	"dreamland" : "DL",
	"finaldestination" : "FD",
	"fountainofdreams" : "FOD",
	"frigatehusk" : "FH",
	"greenhillzone" : "GHZ",
	"luigismansion" : "LM",
	"metalcavern" : "MC",
	"pokemonstadium" : "PS2",
	"goldentemple" : "GT",
	"skysanctuary" : "SSZ",
	"smashville" : "SV",
	"templeoftime" : "TOT",
	"warioland" : "WL",
	"yoshisisland" : "YI"
}
## Start enable check function

# Check to ensure that the BRES is a ModelData that contains a StagePosition mdl0
# Wrapper: BRESWrapper
def EnableCheckBRES(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and node.HasChildren and node.FindChild(MDL_GROUP) and node.FindChild(MDL_GROUP).HasChildren and node.FindChild(MDL_GROUP).Children[0].IsStagePosition

# Check to ensure that the MDL0 is a stagePosition
# Wrapper: MDL0Wrapper
def EnableCheckMDL0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.IsStagePosition)

# Wrapper: STPMWrapper
def EnableCheckSTPM(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.Parent and node.HasChildren)

# Wrapper: GenericWrapper (from STPMEntryNode)
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

def setSTPMCameraValues(stpm_node, sourceSTPMValues):
	isSTPMChanged = False
	
	# Loop through property names
	for i in range(len(STPM_PROP_NAME_LIST)):
		# Get property of destination file (file being changed)
		destProperty = eval("stpm_node." + STPM_PROP_NAME_LIST[i])
		# Compare to property of source file (original file being copied from)
		sourceVal = sourceSTPMValues[i]
		
		# If different, update the destination value
		if destProperty != sourceVal:
			exec("stpm_node." + STPM_PROP_NAME_LIST[i] + " = " + str(sourceVal))
			isSTPMChanged = True
	
	return isSTPMChanged

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

def main(brresNode, stpmEntryNode):
	
	# Get default text for prompt based on stage filename (remove STG and .pac)
	stageName = BrawlAPI.RootNode.FileName[3:-4].lower()
	if stageName in STAGE_NAME_SHORTCUTS.keys():
		promptStr = "Enter stage file identifier"
		defaultText = "_" + STAGE_NAME_SHORTCUTS[stageName] + "_"
	else:
		promptStr = "Enter stage file identifier (e.g. \"_BF_\")"
		defaultText = ""
	
	# Prompt for filename substring to check for
	stageString = BrawlAPI.UserStringInput(promptStr, defaultText)
	if stageString == "" or stageString == None:
		return
	
	# Store source STPM camera values
	sourceSTPMValues = []
	for propertyName in STPM_PROP_NAME_LIST:
		value = eval("stpmEntryNode." + propertyName)
		sourceSTPMValues.append(value)
	
	# Get list of stage pacs in the same folder as the opened file
	sourceFilePath = str(BrawlAPI.RootNode.FilePath)
	stageMeleeDirPath = getParentFolderPath(sourceFilePath)
	stagePacs = Directory.CreateDirectory(stageMeleeDirPath).GetFiles()

	# Export stgPosition brres to temp brres file
	brresNode.ExportUncompressed(TEMP_BRRES_PATH)
	brresID = brresNode.FileIndex
	
	# Get hash of selected node, to compare with new nodes
	originalHash = brresNode.MD5Str()
	
	# List of files found with the given substring
	matchingFilesCount = 0
	filesModified = []
	filesBRRESNotFound = []
	
	# Enable compatibility mode to avoid corrupting older imports
	isCompatibility = MainForm.Instance.CompatibilityMode
	MainForm.Instance.CompatibilityMode = True
	
	# Check each pac file in stage/melee for the given substring
	for file in stagePacs:
		if stageString in file.Name and file.FullName != sourceFilePath:
			matchingFilesCount += 1
			BrawlAPI.OpenFile(file.FullName)
			
			# Find Model Data brres
			parentARC = BrawlAPI.RootNode.FindChild("2")
			if not parentARC:
				continue
			newBRRES = getBRRES(parentARC, brresID)
			
			# If brres not found, add to list and continue
			if not newBRRES:
				filesBRRESNotFound.append(file.Name)
				continue
			
			# If brres hashes aren't identical, replace the brres and save
			if originalHash != newBRRES.MD5Str():
				newBRRES.Replace(TEMP_BRRES_PATH)
				filesModified.append(file.Name)
				BrawlAPI.SaveFile()
			
			# Compare STPM and update. If no node found, move to next file
			newSTPMEntryNode = getSTPMEntryNode()
			if not newSTPMEntryNode:
				continue
			
			entriesChanged = False
			
			# Loop through property names
			for i in range(len(STPM_PROP_NAME_LIST)):
				# Get property of destination file (file being changed)
				destProperty = eval("stpmEntryNode." + STPM_PROP_NAME_LIST[i])
				# Compare to property of source file (original file being copied from)
				sourceVal = sourceSTPMValues[i]
				
				# If different, update the destination value
				if destProperty != sourceVal:
					exec("stpmEntryNode." + STPM_PROP_NAME_LIST[i] + " = " + str(sourceVal))
					entriesChanged = True
			
			if entriesChanged:
				if file.Name not in filesModified:
					filesModified.append(file.Name)
				BrawlAPI.SaveFile()
	
	# After checking all files, open the original stage pac again
	BrawlAPI.OpenFile(sourceFilePath)
	
	# Delete temp brres file
	File.Delete(TEMP_BRRES_PATH)
	# Restore compatibility mode setting
	MainForm.Instance.CompatibilityMode = isCompatibility
	
	# If no mismatches found
	if len(filesModified) == 0 and len(filesBRRESNotFound) == 0:
		msg = "\nNo mismatching BRRES " + str(brresID) + " or STPM data found"
		BrawlAPI.ShowMessage(msg, SCRIPT_NAME)
	
	else:
		msg = ""
		# List any files modified
		if len(filesModified):
			msg += str(matchingFilesCount) + " stage .pac file(s) found with substring \"" + stageString + "\"\n"
			msg += str(len(filesModified)) + " file(s) edited:\n\n"
			msg += listToString(filesModified, 20)
			BrawlAPI.ShowMessage(msg, SCRIPT_NAME)
		
		# List any files missing the appropriate BRRES
		if len(filesBRRESNotFound):
			if not len(filesModified):
				msg += str(matchingFilesCount) + " stage .pac file(s) found with substring \"" + stageString + "\"\n"
			msg += "Files missing BRRES " + str(brresID) + ":\n\n"
			msg += listToString(filesBRRESNotFound, 20)
			BrawlAPI.ShowError(msg, SCRIPT_NAME)

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