__author__ = "mawwwk"
__version__ = "3.2"

from BrawlCrate.API import *
from BrawlCrate.UI import MainForm
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlLib.Internal import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from System.IO import *
from mawwwkLib import *

## Begin global variables

SCRIPT_NAME = "Verify ASL File Data"
OUTPUT_TEXT_FILENAME = "_ASL Data.txt"
FLAGS_LIST = [0x1000, 0x800, 0x400, 0x200, 0x100, 0x80, 0x40, 0x20, 0x10, 8, 4, 2, 1]
missingParamFiles = []		# List of [asl name, param name] combinations where the param file isn't found

ASL_FLAGS_TO_BUTTONS = {
	0x1000: "Start",
	0x800 : "Y",
	0x400 : "X",
	0x200 : "B",
	0x100 : "A",
	0x80 : "??",
	0x40 : "L",
	0x20 : "R",
	0x10 : "Z",
	8: "Up",
	4: "Down",
	2: "Right",
	1: "Left"
}

## End global variables
## Begin helper methods

# Print header for each file
def writeHeader(textFile, parentNode):
	childCount = len(parentNode.Children)
	
	writeStr = "################\n" + parentNode.Name + ".asl - "
	
	if childCount == 1:
		writeStr += "1 alt stage\n\n"
	else:
		writeStr += str(childCount) + " entries\n\n"
	
	textFile.write(writeStr)

# Return string containing param filename
def checkParam(paramDirPath, aslName, paramName):
	paramFileName = str(paramName) + ".param"
	
	if File.Exists(paramDirPath + "\\" + paramFileName):
		return paramFileName
	else:
		missingParamFiles.append([aslName, paramName])
		return paramFileName + " [PARAM FILE NOT FOUND]"

# Convert flags hex to list of buttons, then return a formatted string (i.e. "L+X")
def getButtons(aslEntryNode):
	entryFlags = aslEntryNode.ButtonFlags
	if entryFlags == 0:
		return "Base"
	
	# If out of button range, return value of ButtonFlags in hex
	if entryFlags >= 0x2000:
		return formatHex(entryFlags, 4)
	
	entryButtons = []
	returnStr = ""
	
	# Generate list of buttons
	for flag in FLAGS_LIST:
		if entryFlags >= flag:
			entryButtons.append(ASL_FLAGS_TO_BUTTONS[flag])
			entryFlags -= flag
		# Exit loop after getting to 0
		if entryFlags == 0:
			break
	
	# Convert list to formatted string
	for button in entryButtons:
		returnStr += button + "+"
	
	# Truncate final plus sign
	return returnStr[:-1]

## End helper methods
## Start of main script

def main():
	
	# Prompt for the stageslot directory
	workingDir = BrawlAPI.OpenFolderDialog("Open pf or stageslot folder")
	if not workingDir:
		return
	
	if str(workingDir).endswith("\\pf"):
		workingDir += "\\stage\\stageslot\\"
	elif str(workingDir).endswith("\\pf\\stage"):
		workingDir += "\\stageslot\\"
	else:
		workingDir += "\\"
	
	# Confirm dialog box
	message = "Contents of all .asl files in the folder:\n" + str(workingDir)
	message += "\nwill be checked for valid stage param file locations."
	message += "\n\nPress OK to continue."
	
	if not BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
		return
			
	# File output prompt
	SHORT_PATH = workingDir.rsplit("\\",2)[1] + "/" + OUTPUT_TEXT_FILENAME
	DO_FILE_WRITE = BrawlAPI.ShowYesNoPrompt("Output results to /" + SHORT_PATH + "?", SCRIPT_NAME)
	
	# If file writing is enabled, open AppPath temp text file
	if DO_FILE_WRITE:
		TEMP_TEXT_FILE_PATH = AppPath + OUTPUT_TEXT_FILENAME
		FULL_TEXT_FILE_PATH = str(workingDir) + OUTPUT_TEXT_FILENAME
		TEXT_FILE = open(TEMP_TEXT_FILE_PATH,"w+", encoding="utf-8")
	
	# Derive param folder
	paramDirPath = str(workingDir).rsplit("\\",2)[0] + "\\stageinfo"
	
	# Open whole stageslot folder in BrawlCrate
	if BrawlAPI.RootNode == None or BrawlAPI.RootNode.FilePath != workingDir:
		BrawlAPI.OpenFile(workingDir)
		
	# Progress bar start
	progressBar = ProgressWindow()
	progressBar.Begin(0, len(BrawlAPI.RootNode.Children), 0)
	
	aslFilesOpenedCount = 0	# Number of opened files
	
	# Loop through all ASL files in folder
	for aslNode in BrawlAPI.RootNode.Children:
		if isinstance(aslNode, ASLSNode):
			aslFilesOpenedCount += 1
			currentAsl = ""
			
			# Progress bar
			progressBar.Update(aslFilesOpenedCount)
			
			# If file writing enabled, write header (asl file name, number of entries)
			if DO_FILE_WRITE:
				writeHeader(TEXT_FILE, aslNode)
			
			# For each child node, check button combination and assigned param
			for child in aslNode.Children:
				currentAsl += getButtons(child) + ": "
				currentAsl += checkParam(paramDirPath, aslNode.Name, child.Name) + "\n"
			
			# If file writing enabled, output ASL info to text
			if DO_FILE_WRITE:
				TEXT_FILE.write((currentAsl + "\n\n"))
			
	# After all ASLs are parsed, close text file, and copy from temp folder to tracklist folder
	if DO_FILE_WRITE:
		TEXT_FILE.close()
		File.Copy(TEMP_TEXT_FILE_PATH, FULL_TEXT_FILE_PATH, True)
		File.Delete(TEMP_TEXT_FILE_PATH) # File.Move() doesn't work?
	
	progressBar.Finish()
	
	# RESULTS
	
	# If no ASL files found
	if aslFilesOpenedCount == 0:
		BrawlAPI.ShowError("No .ASL files found in\n" + str(workingDir), "No ASL files found")
		
	# Success, but one or more files missing (don't show file write info)
	elif len(missingParamFiles):
		message = "ASL file errors found.\n\nStage .param file missing:\n"
		
		for i in range(0, len(missingParamFiles),1):
			message += missingParamFiles[i][0] + ".asl: " + missingParamFiles[i][1] + ".param\n"
			
		BrawlAPI.ShowError(message, "Missing files")
	
	# Success, no errors, file write enabled
	elif DO_FILE_WRITE:
		BrawlAPI.ShowMessage("Contents of " + str(aslFilesOpenedCount) + " ASL files exported with no errors to:\n" + str(FULL_TEXT_FILE_PATH), "Success!")
	
	# Success, no errors, no file write
	else:
		BrawlAPI.ShowMessage("Contents of " + str(aslFilesOpenedCount) + " ASL files verified with no errors.", "Success!")

main()