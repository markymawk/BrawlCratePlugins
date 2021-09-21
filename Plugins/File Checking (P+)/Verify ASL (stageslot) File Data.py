__author__ = "mawwwk"
__version__ = "2.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from mawwwkLib import *

## Begin global variables

SCRIPT_NAME = "Verify ASL File Data"
OUTPUT_TEXT_FILENAME = "_ASL Data.txt"
FLAGS_LIST = [4096, 2048, 1024, 512, 256, 64, 32, 16, 8, 4, 2, 1]
missingParamFiles = []		# List of [asl, param] combinations where the param file isn't found

## End global variables
## Begin helper methods

# Print header for each file
def writeHeader(textfile, parentNode):
	childCount = len(parentNode.Children)
	
	writeStr = "################\n" + parentNode.Name + ".asl - "
	
	if childCount == 1:
		writeStr += "1 alt stage\n\n"
	else:
		writeStr += str(childCount) + " entries\n\n"
	
	textfile.write(writeStr)

# Return string containing param filename
def checkParam(asl, param):
	paramFilename = str(param) + ".param"
	
	if File.Exists(PARAM_DIR_PATH + "\\" + paramFilename):
		return paramFilename
	else:
		missingParamFiles.append([asl, param])
		return paramFilename + " [PARAM FILE NOT FOUND]"

# Convert flags hex to list of GCC buttons, then return a formatted string
def getButtons(node):
	thisFileFlags = node.ButtonFlags
	if thisFileFlags == 0:
		return "Base"
	
	thisFileButtons = []
	returnStr = ""
	
	for flag in FLAGS_LIST:
		if thisFileFlags >= flag:
			thisFileButtons.append(ASL_FLAGS_TO_BUTTONS[flag])
			thisFileFlags -= flag
		# Exit loop after getting to 0
		if thisFileFlags == 0:
			break
	
	for button in thisFileButtons:
		returnStr += button + "+"
	
	# Truncate final plus sign
	return returnStr[:-1]

## End helper methods
## Start of main script

def main():
	global PARAM_DIR_PATH
	
	# Prompt for the tracklist directory
	workingDir = BrawlAPI.OpenFolderDialog("Open pf or stageslot folder")
	if not workingDir:
		return
	
	if str(workingDir).endswith("\\pf"):
		workingDir += "\\stage\\stageslot"
	elif str(workingDir).endswith("\\pf\\stage"):
		workingDir += "\\stageslot"
	
	# Confirm dialog box
	message = "Contents of all .asl files in the folder:\n" + str(workingDir) + "\\"
	message += "\nwill be checked for valid stage param file locations."
	message += "\n\nPress OK to continue. (The process may take 20 seconds or longer.)"
	
	if BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
		
		# File output prompt
		SHORT_PATH = workingDir.rsplit("\\",1)[1] + "/" + OUTPUT_TEXT_FILENAME
		DO_FILE_WRITE = BrawlAPI.ShowYesNoPrompt("Output results to /" + SHORT_PATH + "?", SCRIPT_NAME)
		
		# Store currently opened file
		CURRENT_OPEN_FILE = getOpenFile()
		
		# Get list of ASL files in tracklist directory
		ASL_FILES = Directory.CreateDirectory(workingDir).GetFiles()
		
		# If file writing is enabled, open text file and clear it, or create if it doesn't already exist
		if DO_FILE_WRITE:
			FULL_TEXT_FILE_PATH = str(workingDir) + "\\" + OUTPUT_TEXT_FILENAME
			TEXT_FILE = open(FULL_TEXT_FILE_PATH,"w+")
		
		# Derive param folder
		PARAM_DIR_PATH = str(workingDir).rsplit("\\",1)[0] + "\\stageinfo"
		
		aslFilesOpenedCount = 0	# Number of opened files
		
		# Progress bar start
		progressBar = ProgressWindow()
		progressBar.Begin(0,len(ASL_FILES),0)
		
		# Iterate through all ASL files in folder
		for file in ASL_FILES:
		
			if file.Name.lower().EndsWith(".asl"):
				aslFilesOpenedCount += 1
				currentAsl = ""
				
				# Progress bar
				progressBar.Update(aslFilesOpenedCount)
				
				# Open asl file
				BrawlAPI.OpenFile(file.FullName)
				parentNode = BrawlAPI.RootNode
				
				# If file writing enabled, write header (asl file name, number of entries)
				if DO_FILE_WRITE:
					writeHeader(TEXT_FILE, BrawlAPI.RootNode)
				
				# For each child node, check button combination and assigned param
				for child in parentNode.Children:
					currentAsl += getButtons(child) + ": "
					currentAsl += checkParam(parentNode.Name, child.Name) + "\n"
				
				# If file writing enabled, output ASL info to text
				if DO_FILE_WRITE:
					TEXT_FILE.write(currentAsl + "\n\n")
				
		# After all ASLs are parsed, close text file
		if DO_FILE_WRITE:
			TEXT_FILE.close()
		
		progressBar.Finish()
		
		# Reopen previously-opened file
		if CURRENT_OPEN_FILE:
			BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
		
		# RESULTS
		
		# If no ASL files found
		if aslFilesOpenedCount == 0:
			BrawlAPI.ShowError("No .ASL files found in\n" + str(workingDir), "No ASL files found")
			
		# Success, but one or more files missing
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