__author__ = "mawwwk"
__version__ = "3.2"

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

# Returns a string containing pac filename and other info.
# If multiple stage pacs are used, format the string in a way that lists the substage format and all stage pacs used by the param
# Currently uses hard-coded cases for Break_The_Targets.param and for Mushroom(y) Kingdom config behavior
def getStagePacName(paramNode, filePath_meleeDir):
	parentStage = paramNode.StageName.upper()
	stageStr = ""
	
	if parentStage == "":
		return "[NO STAGE PAC ASSIGNED]"
	
	fullStagePacName = "STG" + parentStage.upper() + ".PAC"
	
	# If param loads multiple substages in DualLoad format
	if paramNode.IsDualLoad:
		
		# Check parent stage
		stageStr += "[Substages / DualLoad]\n"
		stageStr += "\t- " + fullStagePacName
		parentPacExists = fullStagePacName[:-4] in BRAWL_STAGE_PACS or checkStagePacFilePath(filePath_meleeDir, parentStage, fullStagePacName)
		
		# If DualLoad parent stage is not in vBrawl, and not found in the pf/stage/melee folder, mark as missing
		if not parentPacExists:
			stageStr += " [PAC FILE MISSING]"
		
		stageStr += "\n"
		
		# Loop through DualLoad child nodes, check & list the substage names
		for substage in paramNode.Children:
			substagePacName = "STG" + substage.Name.upper() + ".PAC"
			stageStr += "\t- " + substagePacName
			
			substagePacExists = substagePacName[:-4] in BRAWL_STAGE_PACS or checkStagePacFilePath(filePath_meleeDir, paramNode.Name, substagePacName)
			
			# If DualLoad substage is not in vBrawl, and not found in the pf/stage/melee folder, mark as missing
			if not substagePacExists:
				stageStr += " [PAC FILE MISSING]"
				
			stageStr += "\n"
		
	# If param uses substages in non-DualLoad format
	elif paramNode.HasChildren and str(paramNode.SubstageVarianceType) != "None":
		stageStr += "[Substages / " + str(paramNode.SubstageVarianceType) + "]\n"
		
		# Combine parent + substage text to form full stage .pac file name
		for substage in paramNode.Children:
			
			# Remove underscore in certain params/slots, such as Smashville and Edit_Stage
			if substage.Name.startswith("_"):
				substageSuffix = substage.Name[1:]
			else:
				substageSuffix = substage.Name
			
			stagePacNameStart = "STG" + parentStage
			
			# Skip adding underscore for Targets substages
			if paramNode.Name != "Break_The_Targets":
				stagePacNameStart += "_"
			
			fullStagePacName = stagePacNameStart + substageSuffix.upper() + ".PAC"
			fullStagePacName = fullStagePacName.upper()
			stageStr += "\t- " + fullStagePacName
			
			# Special check for Mushroomy Kingdom stage loads
			skipMushroomyKingdomCheck = "MUSHROOMKINGDOM_LR_1-1" in fullStagePacName or "MARIOPAST_01" in fullStagePacName
			
			# Check if pac exists
			stagePacExists = checkStagePacFilePath(filePath_meleeDir, paramNode.Name, fullStagePacName)
			
			if not skipMushroomyKingdomCheck and not stagePacExists:
				stageStr += " [PAC FILE MISSING]"
			stageStr += "\n"
	
	# If param has no substages, return the pac file name
	else:
		stageStr += fullStagePacName
		
		# If pac file is missing, append error string
		if fullStagePacName[:-4] not in BRAWL_STAGE_PACS and not checkStagePacFilePath(filePath_meleeDir, paramNode.Name, fullStagePacName):
			stageStr += " [PAC FILE MISSING]"
	
	return stageStr.replace(".PAC", ".pac")

# Returns true if pac filepath exists, else returns false and adds param file name to missingPacParams[]
def checkStagePacFilePath(filePath_meleeDir, paramName, pacFilename):
	pacFileExists = pacFilename[:-4].upper() in BRAWL_STAGE_PACS or File.Exists(filePath_meleeDir + pacFilename)
	
	if not pacFileExists:
		missingPacParams.append(paramName)
	
	return pacFileExists

# Derives module filename given a param node
# Also checks for existence of the given .rel file.
# If rel file is missing, returns an error string and appends param file name to missingModuleParams[]
def getModuleName(parentNode, filePath_moduleDir):
	module = str(parentNode.Module)
	moduleFilePath = filePath_moduleDir + module
	# Results.param uses no .rel file
	if "Results" in parentNode.Name:
		return ""
	
	# If module field is empty, treat as missing
	elif module == "":
		missingModuleParams.append(parentNode.Name)
		return "[NO MODULE ASSIGNED]"
	
	# If module exists, return the module name
	elif module in BRAWL_MODULES or File.Exists(moduleFilePath):
		return module
	
	# If module file is missing, append error string
	else:
		missingModuleParams.append(parentNode.Name)
		return module + " [MODULE FILE MISSING]"

# Derives tracklist name given a param node
# Also checks for the existence of the .tlst file, and returns an error string if the file is missing
def getTracklistName(parentNode, filePath_tracklistDir):
	tracklist = str(parentNode.TrackList) + ".tlst"
	tracklistFilePath = filePath_tracklistDir + tracklist
	
	# Edit_Stage.param uses no tracklist at time of writing
	if parentNode.Name == "Edit_Stage":
		return ""
	
	# If tracklist field is empty, treat as missing
	elif tracklist == ".tlst":
		missingTracklistParams.append(parentNode.Name)
		return "[NO TRACKLIST ASSIGNED]"
	
	# If tracklist file is missing, append error string to tracklist filename, and append error string
	elif not File.Exists(tracklistFilePath):
		missingTracklistParams.append(parentNode.Name)
		return tracklist + " [TRACKLIST FILE MISSING]"
	
	# If tracklist file exists
	else:
		return tracklist

# Return character color overlay value, or return 0 if overlay string corresponds to #00000000
def getColorOverlay(paramNode):
	overlay = paramNode.CharacterOverlay.ToString()
	
	if overlay == "R:0 G:0 B:0 A:0":
		return 0
	else:
		return overlay
	
# Returns string containing all flags set in param file (assuming 1 or more flags set)
def getStageFlags(paramNode):
	thisStageFlags = []
	strFlags = ""
	
	if paramNode.IsFlat:
		strFlags += "Flat, "
	if paramNode.IsFixedCamera:
		strFlags += "FixedCamera, "
	if paramNode.IsSlowStart:
		strFlags += "SlowStart, "
	if paramNode.IsDualLoad:
		strFlags += "DualLoad, "
	if paramNode.IsDualShuffle:
		strFlags += "DualShuffle, "
	if paramNode.IsOldSubstage:
		strFlags += "OldSubstage, "
	
	# Truncate final comma
	return strFlags[:-2]

# Returns string containing SFX and GFX bank IDs, if they exist. Otherwise returns 0
def getSfxGfxString(paramNode):
	sfxID = paramNode.SoundBank
	gfxID = paramNode.EffectBank
	
	if [sfxID, gfxID] == [0xFFFF, 0x32]:
		return 0
	else:
		return "SFX / GFX: " + str(formatHex(sfxID)) + " / " + str(formatHex(gfxID))

## End helper methods
## Start of main script

def main():
	
	# Prompt for stageinfo directory
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
	START_MSG = "Contents of all .param files in the folder:\n" + str(workingDir) + \
	 "\nwill be checked for valid stage, module, and tracklist files." + \
	 "\n\nPress OK to continue."

	if not BrawlAPI.ShowOKCancelPrompt(START_MSG, SCRIPT_NAME):
		return
	
	# Text file output prompt
	SHORT_PATH = workingDir.rsplit("\\",2)[1] + "/" + OUTPUT_TEXT_FILENAME
	DO_FILE_WRITE = BrawlAPI.ShowYesNoPrompt("Output results to /" + SHORT_PATH + "?", SCRIPT_NAME)
	
	# If file writing is enabled, open AppPath temp text file
	if DO_FILE_WRITE:
		TEMP_TEXT_FILE_PATH = AppPath + OUTPUT_TEXT_FILENAME
		FULL_TEXT_FILE_PATH = str(workingDir) + OUTPUT_TEXT_FILENAME
		TEXT_FILE = open(TEMP_TEXT_FILE_PATH,"w+", encoding="utf-8")
	
	# Derive module, tracklist, and stage/melee folders
	filePath_pf = str(workingDir).rsplit("\\",3)[0] + "\\"
	filePath_meleeDir = filePath_pf + "stage\\melee\\"
	filePath_moduleDir = filePath_pf + "module\\"
	filePath_tracklistDir = filePath_pf + "sound\\tracklist\\"
	
	# Open stageinfo folder in BrawlCrate
	if BrawlAPI.RootNode == None or BrawlAPI.RootNode.FilePath != workingDir:
		BrawlAPI.OpenFile(workingDir)
	
	# Progress bar start
	progressBar = ProgressWindow()
	progressBar.Begin(0, len(BrawlAPI.RootNode.Children), 0)
	paramFilesOpenedCount = 0	# Number of opened files
	
	# Iterate through all param files in folder
	for paramNode in BrawlAPI.NodeListOfType[STEXNode]():
		
		# Progress bar
		paramFilesOpenedCount += 1
		progressBar.Update(paramFilesOpenedCount)
		
		# Param output header
		currentParam = "################\n" + paramNode.Name + ".param\n\n" 
		
		# Check stage pac, module, & tracklist, and store in a string (regardless of file write)
		currentParam += "\t" + getStagePacName(paramNode, filePath_meleeDir) + "\n"
		currentParam += "\t" + getModuleName(paramNode, filePath_moduleDir) + "\n"
		currentParam += "\t" + getTracklistName(paramNode, filePath_tracklistDir) + "\n"
		
		# If file writing is enabled, output above info, sfx, gfx, overlay, and flags to text
		if DO_FILE_WRITE:
			
			# If [SFX, GFX] is not empty banks, get SFX/GFX
			sfxGfxString = getSfxGfxString(paramNode)
			if sfxGfxString:
				currentParam += "\t" + sfxGfxString + "\n"
			
			# Get overlay if not #00000000
			overlay = getColorOverlay(paramNode)
			if overlay:
				currentParam += "\tCharacter overlay enabled: " + overlay + "\n"
			
			# Get memory allocation if not 0
			memoryAllocation = paramNode.MemoryAllocation
			if memoryAllocation:
				currentParam += "\tMemoryAllocation: " + formatHex(memoryAllocation) \
				+ " (" + str(memoryAllocation) + " bytes)\n"
				
			# Get stage flags if they exist
			if paramNode.Flags:
				currentParam += "\tFlags: " + getStageFlags(paramNode) + "\n"
			
			# Write to text file
			TEXT_FILE.write(currentParam + "\n")
	
	progressBar.Finish()
	
	# After all params are checked, close text file and copy from temp folder to tracklist folder
	if DO_FILE_WRITE:
		TEXT_FILE.close()
		File.Copy(TEMP_TEXT_FILE_PATH, FULL_TEXT_FILE_PATH, True)
		File.Delete(TEMP_TEXT_FILE_PATH) # File.Move() doesn't work?
	
	# Results
	
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