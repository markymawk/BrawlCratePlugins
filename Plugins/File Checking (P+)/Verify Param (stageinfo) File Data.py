__author__ = "mawwwk"
__version__ = "3.0.1"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from mawwwkLib import *

## Begin global variables

SCRIPT_NAME = "Verify Param File Data"
OUTPUT_TEXT_FILENAME = "_Stage Param Data.txt"
missingPacParams = []
missingModuleParams = []
missingTracklistParams = []

## End global variables
## Start helper methods

# Returns a string containing pac filename.
# If multiple stage pacs are used, format the string in a way that lists the substage format and all stage pacs used by the param
# Currently uses hard-coded cases for Break_The_Targets.param and for Mushroom(y) Kingdom config behavior
def getStagePacName(paramNode):
	parentStage = paramNode.StageName.upper()
	stageStr = ""
	
	if parentStage == "":
		return "[NO STAGE PAC ASSIGNED]"
	
	fullStagePacName = "STG" + parentStage.upper() + ".pac"
	
	# If param loads multiple substages in DualLoad format
	if paramNode.IsDualLoad:
		stageStr += "[Substages / DualLoad]\n"
		
		# Check for DualLoad parent stage pac
		if fullStagePacName[:-4] not in BRAWL_STAGE_PACS and not checkStagePacFilepath(parentStage, fullStagePacName):
			fullStagePacName += " [PAC FILE MISSING]"
		
		stageStr += "\t- " + fullStagePacName.upper() + "\n"
		
		# Loop through DualLoad child nodes and check/list the substage names
		for substage in paramNode.Children:
			fullSubstagePacName = "STG" + substage.Name + ".pac"
			
			# If DualLoad substage is not in vBrawl, and not found in the pf/stage/melee folder, mark as missing
			if not fullSubstagePacName[:-4].upper() in BRAWL_STAGE_PACS and not checkStagePacFilepath(paramNode.Name,fullSubstagePacName):
				fullSubstagePacName += " [PAC FILE MISSING]"
				
			stageStr += "\t- " + fullSubstagePacName.upper() + "\n"
		
	# If param uses substages in non-DualLoad format
	elif paramNode.HasChildren and str(paramNode.SubstageVarianceType) != "None":
		stageStr += "[Substages / " + str(paramNode.SubstageVarianceType) + "]\n"
		
		# Combine parent+substage text to form full stage .pac file name
		for substage in paramNode.Children:
			
			# Remove underscore in certain params/slots, such as Smashville and Edit_Stage
			if substage.Name.startswith("_"):
				substageSuffix = substage.Name[1:]
			else:
				substageSuffix = substage.Name
			
			# Add a necessary underscore for Targets substages
			if paramNode.Name == "Break_The_Targets":
				fullStagePacName = "STG" + parentStage + substageSuffix.upper() + ".pac"
			else:
				fullStagePacName = "STG" + parentStage + "_" + substageSuffix.upper() + ".pac"
			
			# Special check for Mushroomy Kingdom stage loads (assume pac exists)
			if "MUSHROOMKINGDOM_LR_1-1" in fullStagePacName.upper() or "MARIOPAST_01" in fullStagePacName.upper():
				stageStr += "\t- " + fullStagePacName.upper() + "\n"
			else:
				if not checkStagePacFilepath(paramNode.Name, fullStagePacName):
					fullStagePacName += " [PAC FILE MISSING]"
				stageStr += "\t- " + fullStagePacName.upper() + "\n"

	# If param has no substages, return the pac file name
	else:
		
		# If pac file is missing, append error string before returning
		if fullStagePacName[:-4] not in BRAWL_STAGE_PACS and not checkStagePacFilepath(paramNode.Name, fullStagePacName):
			fullStagePacName += " [PAC FILE MISSING]"
		
		return fullStagePacName
	
	return stageStr

# Returns true if pac filepath exists, else returns false and adds .param filename to missingPacParams[]
def checkStagePacFilepath(paramName, pacFilename):
	if pacFilename[:-4].upper() in BRAWL_STAGE_PACS or File.Exists(STAGE_MELEE_DIR_PATH + "\\" + pacFilename):
		return True
	else:
		missingPacParams.append(paramName)
		return False

# Derives module filename given a param node
# Also checks for existence of the given .rel file, and returns an error string if the file is missing or empty
def getModuleName(parentNode):
	module = str(parentNode.Module)
	
	# Results.param uses no .rel file
	if parentNode.Name == "Results":
		return ""
	
	# If module field is empty, treat as missing
	elif module == "":
		missingModuleParams.append(parentNode.Name + ".param")
		return "[NO MODULE ASSIGNED]"
	
	# If module exists, return the module name
	elif module in BRAWL_MODULES or File.Exists(MODULE_DIR_PATH + "\\" + module):
		return module
	
	# If module file is missing, append error string
	else:
		missingModuleParams.append(parentNode.Name + ".param")
		return module + " [MODULE FILE MISSING]"

# Derives tracklist name given a param node
# Also checks for the existence of the .tlst file, and returns an error string if the file is missing
def getTracklistName(parentNode):
	tracklist = str(parentNode.TrackList) + ".tlst"
	
	# Edit_Stage.param uses no tracklist at time of writing
	if parentNode.Name == "Edit_Stage":
		return ""
	
	# If tracklist field is empty, treat as missing
	elif tracklist == ".tlst":
		missingTracklistParams.append(parentNode.Name)
		return "[NO TRACKLIST ASSIGNED]"
	
	# If tracklist file is missing, append error string to tracklist filename, and append error string
	elif not File.Exists(TRACKLIST_DIR_PATH + "\\" + tracklist):
		missingTracklistParams.append(parentNode.Name)
		return tracklist + " [TRACKLIST FILE MISSING]"
	
	# If tracklist file exists
	else:
		return tracklist

# Return character color overlay value, or return 0 if overlay string corresponds to #00000000
def getColorOverlay (parentNode):
	overlay = parentNode.CharacterOverlay.ToString()
	
	if overlay == "R:0 G:0 B:0 A:0":
		return 0
	else:
		return overlay
	
# Returns string containing all flags set in param file (assuming 1 or more flags set)
def getStageFlags(parentNode):
	thisStageFlags = []
	strFlags = ""
	
	if parentNode.IsFlat:
		strFlags += "Flat, "
	if parentNode.IsFixedCamera:
		strFlags += "FixedCamera, "
	if parentNode.IsSlowStart:
		strFlags += "SlowStart, "
	if parentNode.IsDualLoad:
		strFlags += "DualLoad, "
	if parentNode.IsDualShuffle:
		strFlags += "DualShuffle, "
	if parentNode.IsOldSubstage:
		strFlags += "OldSubstage, "
	
	# Truncate final comma
	return strFlags[:-2]

# Returns string containing SFX and GFX bank IDs, if they exist. Otherwise returns 0
def getSfxGfxString(parentNode):
	sfxID = parentNode.SoundBank
	gfxID = parentNode.EffectBank
	
	if [sfxID, gfxID] == [65535, 50]: # 0xFFFF and 0x32
		return 0
	else:
		return "SFX / GFX: " + str(formatHex(sfxID)) + " / " + str(formatHex(gfxID))

## End helper methods
## Start of main script

def main():
	global STAGE_MELEE_DIR_PATH
	global MODULE_DIR_PATH
	global TRACKLIST_DIR_PATH
	
	# Prompt for the stageinfo directory
	workingDir = BrawlAPI.OpenFolderDialog("Open pf or stageinfo folder")
	if not workingDir:
		return

	if workingDir.endswith("\\pf"):
		workingDir += "\\stage\\stageinfo\\"
	elif workingDir.endswith("\\pf\\stage"):
		workingDir += "\\stageinfo\\"
	else:
		workingDir += "\\"
	
	# Confirm dialog box
	message = "Contents of all .param files in the folder:\n" + str(workingDir) + \
	 "\nwill be checked for valid stage, module, and tracklist files." + \
	 "\n\nPress OK to continue."

	if not BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
		return
	
	# File output prompt
	SHORT_PATH = workingDir.rsplit("\\",2)[1] + "/" + OUTPUT_TEXT_FILENAME
	DO_FILE_WRITE = BrawlAPI.ShowYesNoPrompt("Output results to /" + SHORT_PATH + "?", SCRIPT_NAME)
	
	# If file writing is enabled, open AppPath temp text file
	if DO_FILE_WRITE:
		TEMP_TEXT_FILE_PATH = AppPath + OUTPUT_TEXT_FILENAME
		FULL_TEXT_FILE_PATH = str(workingDir) + OUTPUT_TEXT_FILENAME
		TEXT_FILE = open(TEMP_TEXT_FILE_PATH, "w+")
	
	# Derive module, tracklist, and stage/melee folders
	PF_PATH = str(workingDir).rsplit("\\",3)[0] + "\\"
	STAGE_MELEE_DIR_PATH = PF_PATH + "stage\\melee"
	MODULE_DIR_PATH = PF_PATH + "module"
	TRACKLIST_DIR_PATH = PF_PATH + "sound\\tracklist"
	
	# Open whole stageinfo folder in BrawlCrate
	if BrawlAPI.RootNode == None or BrawlAPI.RootNode.FilePath != workingDir:
		BrawlAPI.OpenFile(workingDir)
	
	# Progress bar start
	progressBar = ProgressWindow()
	progressBar.Begin(0, len(BrawlAPI.RootNode.Children), 0)
	
	paramFilesOpenedCount = 0	# Number of opened files
	
	# Iterate through all param files in folder
	for node in BrawlAPI.RootNode.Children:
		if isinstance(node, STEXNode):
			paramFilesOpenedCount += 1
			currentParam = "" # Current param output string
			
			# Progress bar
			progressBar.Update(paramFilesOpenedCount)
			
			# Check stage pac, module, & tracklist, and store in a string (regardless of file write)
			currentParam += "################\n" + node.Name + ".param\n\n" + \
			 "\t" + getStagePacName(node) + "\n" + \
			 "\t" + getModuleName(node) + "\n" + \
			 "\t" + getTracklistName(node) + "\n"
			
			# If file writing is enabled, output above info, sfx, gfx, overlay, and flags to text
			if DO_FILE_WRITE:
				sfxGfxString = getSfxGfxString(node)
				overlay = getColorOverlay(node)
				
				# If [SFX, GFX] is not empty banks, get SFX/GFX
				if sfxGfxString:
					currentParam += "\t" + sfxGfxString + "\n"
				
				# If overlay is not #00000000, get overlay
				if overlay:
					currentParam += "\tCharacter overlay enabled: " + overlay + "\n"
					
				# If stage flags exist, get stage flags
				if node.Flags:
					currentParam += "\tFlags: " + getStageFlags(node) + "\n"
			
				TEXT_FILE.write(currentParam + "\n")
		
	# After all params are parsed, close text file, and copy from temp folder to tracklist folder
	if DO_FILE_WRITE:
		TEXT_FILE.close()
		File.Copy(TEMP_TEXT_FILE_PATH, FULL_TEXT_FILE_PATH, True)
		File.Delete(TEMP_TEXT_FILE_PATH) # File.Move() doesn't work?
	
	progressBar.Finish()
	
	# RESULTS
	
	# If no params found
	if paramFilesOpenedCount == 0:
		BrawlAPI.ShowError("No .param files found in\n" + str(workingDir), "No param files found")
		return
	
	# Determine whether any errors were found
	errors = len(missingPacParams) + len(missingModuleParams) + len(missingTracklistParams)
	
	# One or more files missing
	if errors:
		message = "Stage param file errors found.\n\n"
		
		# List missing stage pac files
		if len(missingPacParams):
			message += "Stage .pac file not found:\n"
			for p in missingPacParams:
				message += p + ".param\n"
			message += "\n"
		
		# List missing stage module files
		if len(missingModuleParams):
			message += "Module file not found:\n"
			for p in missingModuleParams:
				message += p + ".param\n"
			message += "\n"
		
		# List missing tracklist files
		if len(missingTracklistParams):
			message += "Tracklist file not found:\n"
			for p in missingTracklistParams:
				message += p + ".param\n"
			message += "\n"
			
		BrawlAPI.ShowError(message, "Missing files")

	# Success, no errors, file write enabled
	elif DO_FILE_WRITE:
		BrawlAPI.ShowMessage("Contents of " + str(paramFilesOpenedCount) + " param files exported with no errors to:\n" + str(FULL_TEXT_FILE_PATH), "Success!")
	
	# Success, no file write
	else:
		BrawlAPI.ShowMessage("Contents of " + str(paramFilesOpenedCount) + " param files verified with no errors.", "Success!")

main()