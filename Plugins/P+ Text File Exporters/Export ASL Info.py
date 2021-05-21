__author__ = "mawwwk"
__version__ = "1.5.1"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from BrawlLib.Imaging import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from mawwwkLib import *

FLAGS_LIST = [4096, 2048, 1024, 512, 256, 64, 32, 16, 8, 4, 2, 1]
OUTPUT_TEXT_FILENAME = "_ASL Data.txt"

missingASLList = []
missingParamFiles = []

## Begin helper methods

# Print header for each file
def writeHeader(textfile, parentNode):
	childCount = len(parentNode.Children)
	
	writeStr = "################\n" + parentNode.Name + ".asl - "
	
	if childCount == 1:
		writeStr += "1 alt stage\n\n"
	else:
		writeStr += str(childCount) + " alt stages\n\n"
	
	textfile.write(writeStr)

# Return string containing param filename
def checkParam(asl, param):
	paramFilename = str(param) + ".param"
	
	if File.Exists(PARAM_DIR_PATH + "\\" + paramFilename):
		return paramFilename
	else:
		missingASLList.append(asl)
		missingParamFiles.append(param)
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

# Prompt for the tracklist directory
workingDir = BrawlAPI.OpenFolderDialog("Open pf or stageslot folder")

if str(workingDir).endswith("\\pf"):
	workingDir += "\\stage\\stageslot"
elif str(workingDir).endswith("\\pf\\stage"):
	workingDir += "\\stageslot"

if workingDir and "stageslot" not in workingDir:
	BrawlAPI.ShowError("Invalid directory", "Error")

elif workingDir:

	# Confirm dialog box
	message = "Contents of all .asl files in the folder\n\n" + str(workingDir)
	message += "\nwill be exported to " + str(OUTPUT_TEXT_FILENAME) + " in the same folder."
	message += "\n\nPress OK to continue. (The process may take 20 seconds or longer.)"
	
	if BrawlAPI.ShowOKCancelPrompt(message, "Export ASL File Data"):
	
		# Store currently opened file
		CURRENT_OPEN_FILE = getOpenFile()
		
		# Get list of ASL files in tracklist directory
		ASL_FILES = Directory.CreateDirectory(workingDir).GetFiles()
		
		# Open text file and clear it, or create if it doesn't already exist
		fullTextFilePath = str(workingDir) + "\\" + OUTPUT_TEXT_FILENAME
		TEXT_FILE = open(fullTextFilePath,"w+")
		
		# Derive param folder
		PARAM_DIR_PATH = str(workingDir).replace('stageslot','stageinfo')
		
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
				
				# Write header (asl file name, number of entries)
				writeHeader(TEXT_FILE, BrawlAPI.RootNode)
				
				# For each child node, print button combination and assigned param
				for child in parentNode.Children:
					currentAsl += getButtons(child) + ": "
					currentAsl += checkParam(parentNode.Name, child.Name) + "\n"
				
				# Close current ASL file after parsing, and output to text
				TEXT_FILE.write(currentAsl + "\n\n")
				
		# After all ASLs are parsed, close text file
		TEXT_FILE.close()
		progressBar.Finish()
		
		# Reopen previously-opened file
		if CURRENT_OPEN_FILE:
			BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
		
		# RESULTS
		
		# Determine whether any errors were found
		missingParamFound = len(missingParamFiles)

		# Success, no errors
		if aslFilesOpenedCount and not missingParamFound:
			BrawlAPI.ShowMessage("Contents of " + str(aslFilesOpenedCount) + " ASL files exported with no errors to:\n" + str(fullTextFilePath), "Success!")

		# Success, but one or more files missing
		if missingParamFound:
			message = "ASL file contents exported successfully, but errors found.\n\nStage .param file missing:\n"
			
			for i in range(0, len(missingParamFiles),1):
				message += missingASLList[i] + ".asl : " + missingParamFiles[i] + ".param\n"
				
			BrawlAPI.ShowError(message, "Missing files")
		
		# If no ASL files found
		elif aslFilesOpenedCount == 0:
			BrawlAPI.ShowError("No .ASL files found in\n" + str(workingDir), "No ASL files found")