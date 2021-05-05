__author__ = "mawwwk"
__version__ = "1.5"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from BrawlLib.Imaging import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow

FLAGS_TO_BUTTONS = {
	1 : "Left",
	2 : "Right",
	4 : "Down",
	8: "Up",
	16 : "Z", 		# 0x10
	32 : "R",		# 0x20
	64 : "L",       # 0x40
	256 : "A",      # 0x100
	512 : "B",      # 0x200
	1024 : "X",     # 0x400
	2048 : "Y",     # 0x800
	4096 : "Start"  # 0x1000
}

FLAGS_LIST = [4096, 2048, 1024, 512, 256, 64, 32, 16, 8, 4, 2, 1]

outputFileName = "_ASL Data.txt"

aslMissing = []
missingParamFiles = []

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
		aslMissing.append(asl)
		missingParamFiles.append(param)
		return paramFilename + " [PARAM FILE NOT FOUND]"

# Convert flags hex to list of GCC buttons, then return a formatted string
def getButtons(node):
	thisFlags = node.ButtonFlags
	if thisFlags == 0:
		return "Base"
	
	thisButtons = []
	returnStr = ""
	
	for flag in FLAGS_LIST:
		if thisFlags >= flag:
			thisButtons.append(FLAGS_TO_BUTTONS[flag])
			thisFlags -= flag
		# Quit out after getting to 0
		if thisFlags == 0:
			break
	
	for button in thisButtons:
		returnStr += button + "+"
	
	# Truncate final plus sign
	return returnStr[:-1]

############################################
########### Start of main script ###########
############################################

# Prompt for the tracklist directory
workingDir = BrawlAPI.OpenFolderDialog("Open pf or stageslot folder")

if str(workingDir)[-3:] == "\\pf":
	workingDir += "\\stage\\stageslot"
elif str(workingDir)[-9:] == "\\pf\\stage":
	workingDir += "\\stageslot"

if workingDir and "stageslot" not in workingDir:
	BrawlAPI.ShowError("Invalid directory", "Error")
elif workingDir:
	if BrawlAPI.RootNode:
		CURRENT_OPEN_FILE = str(BrawlAPI.RootNode.FilePath)
	else:
		CURRENT_OPEN_FILE = 0
	
	# Derive param folder
	PARAM_DIR_PATH = str(workingDir).replace('stageslot','stageinfo')

	# Get list of ASL files in tracklist directory
	ASL_FILES = Directory.CreateDirectory(workingDir).GetFiles()
	ASL_FILE_COUNT = len(ASL_FILES)

	# Confirm dialog box
	message = "Contents of all .asl files in the folder\n\n" + str(workingDir)
	message += "\nwill be exported to " + str(outputFileName) + " in the same folder."
	message += "\n\nPress OK to continue. (The process may take 20 seconds or longer.)"

	if BrawlAPI.ShowOKCancelPrompt(message, "Export ASL File Data"):
		# Open text file and clear it, or create if it doesn't already exist
		fullTextFilePath = str(workingDir) + "\\" + outputFileName
		textfile = open(fullTextFilePath,"w+")
		
		aslFilesOpenedCount = 0	# Number of opened files
		
		# Progress bar start
		progressBar = ProgressWindow()
		progressBar.Begin(0,ASL_FILE_COUNT,0)
		
		# Iterate through all ASL files in folder
		for file in ASL_FILES:
			if file.Name.lower().EndsWith(".asl"):
				currentAsl = ""		# Clear current asl output string
				
				# Update progress bar
				aslFilesOpenedCount += 1
				progressBar.Update(aslFilesOpenedCount)
				
				# Open asl file
				BrawlAPI.OpenFile(file.FullName)
				parentNode = BrawlAPI.RootNode
				
				# Write header (asl file name, number of entries)
				writeHeader(textfile, BrawlAPI.RootNode)
				
				# For each child node, print button combination and assigned param
				for child in parentNode.Children:
					currentAsl += getButtons(child) + ": "
					currentAsl += checkParam(parentNode.Name, child.Name) + "\n"
				
				# Close current ASL file after parsing, and output to text
				BrawlAPI.ForceCloseFile()
				textfile.write(currentAsl + "\n\n")
				
		# After all ASLs are parsed, close text file
		textfile.close()
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
				message += aslMissing[i] + ".asl : " + missingParamFiles[i] + ".param\n"
				
			BrawlAPI.ShowError(message, "Missing files")
		
		# No ASL files found
		elif aslFilesOpenedCount == 0:
			BrawlAPI.ShowError("No .ASL files found in\n" + str(workingDir), "No ASL files found")