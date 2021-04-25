__author__ = "mawwwk"
__version__ = "1.4.1"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from BrawlLib.Imaging import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from os import path

BRAWL_STAGE_PACS = ["STGBATTLEFIELD", "STGCHARAROLL", "STGCONFIGTEST", "STGCRAYON", "STGDOLPIC", "STGDONKEY", "STGDXBIGBLUE", "STGDXCORNERIA", "STGDXGARDEN", "STGDXGREENS", "STGDXONETT", "STGDXONETT", "STGDXPSTADIUM", "STGDXRCRUISE", "STGDXSHRINE", "STGDXYORSTER", "STGDXZEBES", "STGEARTH", "STGEDIT_0", "STGEDIT_1", "STGEDIT_2", "STGEMBLEM", "STGEMBLEM_00", "STGEMBLEM_01", "STGEMBLEM_02", "STGFAMICOM", "STGFINAL", "STGFZERO", "STGGREENHILL", "STGGW", "STGGW", "STGHALBERD", "STGHEAL", "STGHOMERUN", "STGHOMERUN", "STGICE", "STGJUNGLE", "STGKART", "STGMADEIN", "STGMANSION", "STGMARIOPAST_00", "STGMARIOPAST_01", "STGMETALGEAR_00", "STGMETALGEAR_01", "STGMETALGEAR_02", "STGNEWPORK", "STGNORFAIR", "STGOLDIN", "STGONLINETRAINING", "STGORPHEON", "STGPALUTENA", "STGPICTCHAT", "STGPIRATES", "STGPLANKTON", "STGRESULT", "STGSTADIUM", "STGSTARFOX_ASTEROID", "STGSTARFOX_BATTLESHIP", "STGSTARFOX_CORNERIA", "STGSTARFOX_GDIFF", "STGSTARFOX_SPACE", "STGTARGETLV1", "STGTARGETLV2", "STGTARGETLV3", "STGTARGETLV4", "STGTARGETLV5", "STGTENGAN_1", "STGTENGAN_2", "STGTENGAN_3", "STGVILLAGE_00", "STGVILLAGE_01", "STGVILLAGE_02", "STGVILLAGE_03", "STGVILLAGE_04"]

BRAWL_MODULES = ["st_battle.rel", "st_battles.rel", "st_config.rel", "st_crayon.rel", "st_croll.rel", "st_dolpic.rel", "st_donkey.rel", "st_dxbigblue.rel", "st_dxcorneria.rel", "st_dxgarden.rel", "st_dxgreens.rel", "st_dxonett.rel", "st_dxpstadium.rel", "st_dxrcruise.rel", "st_dxshrine.rel", "st_dxyorster.rel", "st_dxzebes.rel", "st_earth.rel", "st_emblem.rel", "st_famicom.rel", "st_final.rel", "st_fzero.rel", "st_greenhill.rel", "st_gw.rel", "st_halberd.rel", "st_heal.rel", "st_homerun.rel", "st_ice.rel", "st_jungle.rel", "st_kart.rel", "st_madein.rel", "st_mansion.rel", "st_mariopast.rel", "st_metalgear.rel", "st_newpork.rel", "st_norfair.rel", "st_oldin.rel", "st_orpheon.rel", "st_otrain.rel", "st_palutena.rel", "st_pictchat.rel", "st_pirates.rel", "st_plankton.rel", "st_stadium.rel", "st_stageedit.rel", "st_starfox.rel", "st_tbreak.rel", "st_tengan.rel", "st_village.rel"]

OUTPUT_FILE_NAME = "_Stage Param Data.txt"

paramFilesOpenedCount = 0
missingPacParams = []
missingModuleParams = []
missingTracklistParams = []

# Print a formatted header for each param file
def writeHeader(textfile, parentNode):
	textfile.write("################\n" + \
	str(parentNode.Name) + ".param\n\n")

# Returns a string containing pac filename.
# If multiple stage pacs are used, format the string in a way that lists the substage format and all stage pacs used by the param
# Currently uses hard-coded cases for Break_The_Targets.param and for Mushroom(y) Kingdom config behavior
def getStagePacName(parentNode):
	parentStage = parentNode.StageName.upper()
	
	if parentStage == "":
		return "[NO STAGE PAC ASSIGNED]"
	
	# If param loads multiple substages
	if parentNode.IsDualLoad or (parentNode.Children and str(parentNode.SubstageVarianceType) != "None"):
		if parentNode.IsDualLoad:
			stageStr = "[Substages / " + "DualLoad" + "]\n"
		else:
			stageStr = "[Substages / " + str(parentNode.SubstageVarianceType) + "]\n"
		
		# Loop through child substages
		# Dual-load stages should read substages differently than non-dual-loaders
		# Check for missing stage .pacs
		if parentNode.IsDualLoad:
			fullStagePacName = "STG" + parentStage + ".pac"
			if fullStagePacName[:-4] not in BRAWL_STAGE_PACS and not checkStagePacFilepath(parentStage, fullStagePacName):
				fullStagePacName += " [PAC FILE MISSING]"
			
			stageStr += "\t- " + fullStagePacName.upper() + "\n"
			
			# Loop through DualLoad child nodes
			for substage in parentNode.Children:
				fullStagePacName = "STG" + substage.Name + ".pac"
				
				# If stage is not in vBrawl, and not found in the pf/stage/melee folder, mark as missing
				if fullStagePacName[:-4].upper() not in BRAWL_STAGE_PACS and not checkStagePacFilepath(parentStage,fullStagePacName):
					fullStagePacName += " [PAC FILE MISSING]"
					
				stageStr += "\t- " + fullStagePacName.upper() + "\n"
		
		# Param uses substages, but not DualLoad
		else:	
			for substage in parentNode.Children:
			
				# Remove underscore in certain params/slots, such as Smashville and Edit_Stage
				if str(substage.Name[0]) == "_":
					substageSuffix = substage.Name[1:].upper()
				else:
					substageSuffix = substage.Name.upper()
				
				# Add a necessary underscore for Targets substages
				if parentNode.Name == "Break_The_Targets":
					fullStagePacName = "STG" + parentStage + substageSuffix + ".pac"
				else:
					fullStagePacName = "STG" + parentStage + "_" + substageSuffix + ".pac"
				
				# If stage is not in vBrawl, not a default P+ Mushroom Kingdom LR stage, and not found in the pf/stage/melee folder, mark as missing
				if fullStagePacName[:-4].upper() not in BRAWL_STAGE_PACS \
				and "MUSHROOMKINGDOM_LR_1-1" not in fullStagePacName \
				and not checkStagePacFilepath(parentStage, fullStagePacName):
					fullStagePacName += " [PAC FILE MISSING]"
				stageStr += "\t- " + fullStagePacName.upper() + "\n"
		
		return stageStr
	
	# If param has no substages
	else:
		fullStagePacName = "STG" + parentStage.upper() + ".pac"
		
		# If pac file is missing, append error string to pac filename
		if fullStagePacName[:-4] not in BRAWL_STAGE_PACS and not checkStagePacFilepath(parentNode.Name, fullStagePacName):
			fullStagePacName += " [PAC FILE MISSING]"
		
		# If pac file is present, return pac filename
		return fullStagePacName

# Helper method to check if stage pac filepath exists
# Returns true if exists, else returns false and adds .param filename to missingPacParams[]
def checkStagePacFilepath(paramName, pacFilename):
	if pacFilename in BRAWL_STAGE_PACS or path.exists(STAGE_MELEE_DIR_PATH + "\\" + pacFilename):
		return True
	else:
		missingPacParams.append(paramName)
		return False

# Derives module filename given a param node
# Also checks for existence of the given .rel file, and returns an error string if the file is missing or empty
def getModuleName(parentNode):
	module = str(parentNode.Module)
	
	# STGRESULT uses no .rel file
	if parentNode.Name == "Results":
		return ""
	elif module == "":
		return "[NO MODULE ASSIGNED]"
	# If module file is missing, append error string to module filename
	elif not checkModuleFilepath(parentNode.Name, module):
		return module + " [MODULE FILE MISSING]"
	else:
		return module

# Helper method to check if module filepath exists
# Returns true if exists, else returns false and adds .param filename to missingModuleParams[]
def checkModuleFilepath (paramName, moduleFilename):
	if moduleFilename in BRAWL_MODULES or path.exists(MODULE_DIR_PATH + "\\" + moduleFilename):
		return True
	else:
		missingModuleParams.append(paramName)
		return False

# Derives tracklist name given a param node
# Hard-coded edge case for Edit_Stage.param (uses no tracklist as of time of writing)
# Also checks for the existence of the .tlst file, and returns an error string if the file is missing
def getTracklistName(parentNode):
	tracklist = str(parentNode.TrackList)
	
	if parentNode.Name == "Edit_Stage":
		return ""
	elif tracklist == "":
		return "[NO TRACKLIST ASSIGNED]"
		missingTracklistParams.append(parentNode.Name)
	# If tracklist file is missing, append error string to tracklist filename
	elif not checkTracklistFilepath(parentNode.Name, tracklist + ".tlst"):
		return tracklist + ".tlst [TRACKLIST FILE MISSING]"
	else:
		return tracklist + ".tlst"

# Helper method to check if tlst filepath exists
# Returns true if filepath exists, else false
# If false, also adds param filename to missingTracklistParams[]
def checkTracklistFilepath (paramName, tracklistFilename):
	if path.exists(TRACKLIST_DIR_PATH + "\\" + tracklistFilename) :
		return True
	else:
		missingTracklistParams.append(paramName)
		return False

# Return character color overlay value, or return 0 if overlay string corresponds to #00000000
def getColorOverlay (parentNode):
	overlay = parentNode.CharacterOverlay.ToString()
	
	if overlay == "R:0 G:0 B:0 A:0":
		return 0
	else:
		return overlay
	
# Returns string containing all flags set in param file
def getStageFlags(parentNode):
	thisStageFlags = []
	strFlags = ""
	
	if parentNode.IsFlat:
		thisStageFlags.append("Flat")
	if parentNode.IsFixedCamera:
		thisStageFlags.append("FixedCamera")
	if parentNode.IsSlowStart:
		thisStageFlags.append("SlowStart")
	if parentNode.IsDualLoad:
		thisStageFlags.append("DualLoad")
	if parentNode.IsDualShuffle:
		thisStageFlags.append("DualShuffle")
	if parentNode.IsOldSubstage:
		thisStageFlags.append("OldSubstage")
	
	for flag in thisStageFlags:
		strFlags += flag + ", "
	
	# Truncate final comma
	return strFlags[:-2]

# Given dec value, returns hex value
# Formatted with lowercase 0x prefix, four uppercase hex digits, and trailing L removed
def formatHex(value):
	string = "0x" + str(hex(value)).upper()[2:-1]
	while len(string) < 6:
		string = string[:2] + '0' + string[2:]
	return string

############################################
########### Start of main script ###########
############################################

# Prompt for the stageinfo directory
workingDir = BrawlAPI.OpenFolderDialog("Open pf or stageinfo folder")

if str(workingDir)[-3:] == "\\pf":
	workingDir += "\\stage\\stageinfo"
elif str(workingDir)[-9:] == "\\pf\\stage":
	workingDir += "\\stageinfo"

if workingDir:
	if BrawlAPI.RootNode:
		CURRENT_OPEN_FILE = str(BrawlAPI.RootNode.FilePath)
	else:
		CURRENT_OPEN_FILE = 0
	
	# Derive module folder and stage pac folder
	STAGE_MELEE_DIR_PATH = str(workingDir).replace('stageinfo','melee')
	MODULE_DIR_PATH = str(workingDir).replace('stage\\stageinfo', 'module')
	TRACKLIST_DIR_PATH = str(workingDir).replace('stage\\stageinfo', 'sound\\tracklist')

	# Get list of param files in stageinfo directory
	PARAM_FILES = Directory.CreateDirectory(workingDir).GetFiles()
	PARAM_FILE_COUNT = len(PARAM_FILES)

	# Open text file and clear it, or create if it doesn't already exist
	FULL_TEXT_FILE_PATH = str(workingDir) + "\\" + OUTPUT_FILE_NAME
	TEXT_FILE = open(FULL_TEXT_FILE_PATH,"w+")

	# Confirm dialog box
	message = "Contents of all .param files in the folder\n\n" + str(workingDir)
	message += "\nwill be exported to " + str(OUTPUT_FILE_NAME) + " in the same folder."
	message += "\n\nPress OK to continue. (The process may take 20 seconds or longer.)"

	if BrawlAPI.ShowOKCancelPrompt(message, "Export Param File Data"):
		
		progressBar = ProgressWindow()
		progressBar.Begin(0,PARAM_FILE_COUNT,0)
		
		# Iterate through all param files in folder
		for file in PARAM_FILES:

			if file.Name.lower().EndsWith(".param"):
				paramFilesOpenedCount += 1
				currentParam = ""
				
				progressBar.Update(paramFilesOpenedCount)
			
				# Open param file
				BrawlAPI.OpenFile(file.FullName)
				parentNode = BrawlAPI.NodeList[0]
				
				# Write param header (file name)
				writeHeader(TEXT_FILE, parentNode)
				
				# Write stage pac filename(s)
				currentParam += "\t" + getStagePacName(parentNode) + "\n"
				# Write module
				currentParam += "\t" + getModuleName(parentNode) + "\n"
				# Write tracklist
				currentParam += "\t" + str(getTracklistName(parentNode)) + "\n"
				# Write SFX and GFX
				currentParam += "\t" + "SFX / GFX: " + str(formatHex(parentNode.SoundBank)) + " / " + str(formatHex(parentNode.EffectBank)) + "\n"
				
				# Write overlay, if not #00000000
				overlay = getColorOverlay(parentNode)
				if overlay:
					currentParam += "\tCharacter overlay enabled: " + overlay + "\n"
					
				# Write stage flags, if exist
				if parentNode.Flags:
					currentParam += "\tFlags: " + getStageFlags(parentNode) + "\n"
				
				currentParam += "\n\n"
				
				# Close current param file after parsing, and output to text
				BrawlAPI.ForceCloseFile()
				
				TEXT_FILE.write(currentParam)
				
		# Close output text file after all param files are parsed
		TEXT_FILE.close()
		progressBar.Finish()
		
		# Reopen previously-opened file
		if CURRENT_OPEN_FILE:
			BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
		# RESULTS
		
		# Determine the existence of any errors found while parsing
		isMissingPacFound = len(missingPacParams)
		isMissingModuleFound = len(missingModuleParams)
		isMissingTracklistFound = len(missingTracklistParams)

		# Success, no errors
		if not isMissingPacFound and not isMissingModuleFound and not isMissingTracklistFound and paramFilesOpenedCount > 0:
			BrawlAPI.ShowMessage("Contents of " + str(paramFilesOpenedCount) + " param files exported with no errors to:\n" + str(FULL_TEXT_FILE_PATH), "Success!")

		# Success, but one or more files missing
		if isMissingPacFound or isMissingModuleFound or isMissingTracklistFound:
			message = "Stage param contents exported successfully, but errors found.\n\n"
			if isMissingPacFound:
				message += "Stage .pac file not found:\n"
				for p in missingPacParams:
					message += p + ".param\n"
				message += "\n"
			if isMissingModuleFound:
				message += "Module file not found:\n"
				for p in missingModuleParams:
					message += p + ".param\n"
				message += "\n"
			if isMissingTracklistFound:
				message += "Tracklist file not found:\n"
				for p in missingTracklistParams:
					message += p + ".param\n"
				message += "\n"
				
			BrawlAPI.ShowError(message, "Missing files")
		
		# No params found
		elif paramFilesOpenedCount == 0:
			BrawlAPI.ShowError("No .param files found in\n" + str(workingDir), "No param files found")
