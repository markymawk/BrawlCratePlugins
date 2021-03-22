__author__ = "mawwwk"
__version__ = "1.4"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from BrawlLib.Imaging import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from os import path

outputFileName = "_ASL Data.txt"
aslFilesOpenedCount = 0
aslMissing = []
missingParamFiles = []

flagsToButtons = {
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

flagsList = [4096, 2048, 1024, 512, 256, 64, 32, 16, 8, 4, 2, 1]

# Print header for each file
def writeHeader(textfile, aslFilename):
	childCount = len(parentNode.Children)
	
	writeStr = "################\n" + aslFilename + " - "
	
	if childCount == 1:
		writeStr += "1 alt stage\n\n"
	else:
		writeStr += str(childCount) + " alt stages\n\n"
	
	textfile.write(writeStr)

# Return string containing param filename
def checkParam(asl, param):
	paramFilename = str(param) + ".param"
	
	if path.exists (paramFolder + "\\" + paramFilename):
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
	
	for flag in flagsList:
		if thisFlags >= flag:
			thisButtons.append(flagsToButtons[flag])
			thisFlags -= flag
	
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

if workingDir:
	
	# Derive param folder and stage pac folder
	paramFolder = str(workingDir).replace('stageslot','stageinfo')

	# Get list of ASL files in tracklist directory
	ASL_FILES = Directory.CreateDirectory(workingDir).GetFiles()
	ASL_FILE_COUNT = len(ASL_FILES)

	# Open text file and clear it, or create if it doesn't already exist
	fullTextFilePath = str(workingDir) + "\\" + outputFileName
	textfile = open(fullTextFilePath,"w+")

	# Confirm dialog box
	message = "Contents of all .asl files in the folder\n\n" + str(workingDir)
	message += "\nwill be exported to " + str(outputFileName) + " in the same folder."
	message += "\n\nPress OK to continue. (The process may take 20 seconds or longer.)"

	if BrawlAPI.ShowOKCancelPrompt(message, "Export ASL Data"):
	
		progressBar = ProgressWindow()
		progressBar.Begin(0,ASL_FILE_COUNT,0)
		
		# Iterate through all asl files in folder
		for file in ASL_FILES:

			if file.Name.lower().EndsWith(".asl"):
				aslFilesOpenedCount += 1
				currentAsl = ""
				
				progressBar.Update(aslFilesOpenedCount)
				
				# Open asl file
				BrawlAPI.OpenFile(file.FullName)
				parentNode = BrawlAPI.NodeList[0]
				
				# Write header (asl file name, number of entries)
				writeHeader(textfile, file.Name)
				
				for node in parentNode.Children:
					currentAsl += getButtons(node) + ": " + \
					checkParam(parentNode.Name, node.Name) + "\n"
					
				BrawlAPI.ForceCloseFile()
				
				currentAsl += "\n\n"
				textfile.write(currentAsl)
				
		# Close text file after all files are parsed
		textfile.close()
		progressBar.Finish()
		
		#
		# RESULTS
		#
		
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