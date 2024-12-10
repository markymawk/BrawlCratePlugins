__author__ = "mawwwk"
__version__ = "1.2.1"

from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from mawwwkLib import *

SCRIPT_NAME = "Detect Unused BRSTM Files"
 
brstmFiles = []			# List containing file names of all brstm files in pf\sound\strm, except Brawl song IDs
brawlBrstmFiles = []	# List containing brawl song ID names used

## Start helper methods

# Populate brstmFiles[] by adding all brstm file names, then recursively run through each subfolder
def populateBrstmFilesList(dir, parentFolder=""):
	for file in Directory.CreateDirectory(dir).GetFiles():
	
		if ".brstm" in file.Name:
			# Swap backslash (\) with forward slash (/) for consistency
			filePath = (parentFolder + file.Name).replace("\\", "/")
			
			if file.Name[0:3] in BRAWL_SONG_ID_LIST:
				brawlBrstmFiles.append(filePath)
			else:
				brstmFiles.append(filePath)
	
	for subfolder in Directory.GetDirectories(dir):
		subfolderName = subfolder.split("strm\\")[-1]
		populateBrstmFilesList(subfolder, subfolderName + "/")

# Given the track entry node, check if the given track name string exists in brstmFiles[]
# If it exists, return the index
def checkTrackName(track):
	trackName = str(track.SongFileName)
	if trackName != "None":
		
		trackName = trackName.lower() + ".brstm"
		trackName = trackName.replace("\\", "/")
		
		# If track is found, return index of the track
		for i in range(0, len(brstmFiles), 1):
			fileName = brstmFiles[i].lower()
			if trackName == fileName.lower():
				return i
	
	# If not found, return -1
	return -1

# Given a track entry node with a SongSwitch > 1, find and return the index of the track name inside brstmFiles[]
def getPinchTrackIndex(track):
	trackName = str(track.SongFileName).lower() + "_b.brstm"
	trackName = trackName.replace("\\", "/")
	
	# Return index inside brstmFiles
	for i in range(0, len(brstmFiles), 1):
		fileName = brstmFiles[i].lower()
		if trackName == fileName.lower():
			return i
	
	# If not present, return -1
	return -1

## End helper methods
## Start of main script

def main():
	# Prompt for directory
	workingDir = BrawlAPI.OpenFolderDialog("Open pf, sound, or strm folder")
	workingDir = str(workingDir)

	# Derive strm and tracklist folder paths
	[strmFolderPath, tracklistFolderPath] = [0, 0]
	if workingDir[-3:] == "\\pf":
		strmFolderPath = workingDir + "\\sound\\strm\\"
		tracklistFolderPath = workingDir + "\\sound\\tracklist\\"
	elif workingDir[-9:] == "\\pf\\sound":
		strmFolderPath = workingDir + "\\strm\\"
		tracklistFolderPath = workingDir + "\\tracklist\\"
	elif workingDir [-5:] == "\\strm":
		strmFolderPath = workingDir
		tracklistFolderPath = workingDir.replace("\\strm", "\\tracklist")

	if workingDir and not strmFolderPath:
		BrawlAPI.ShowError("Invalid directory", "Error")
		return
	elif not workingDir:
		return
	
	# Save currently opened file, if any
	initialOpenedFile = getOpenFile()
	
	# Get list of brstm file names in sound/strm directory, and store in brstmFiles[]
	populateBrstmFilesList(strmFolderPath)
	BRSTM_FILE_COUNT = len(brstmFiles)
	
	# Open tracklist folder in BrawlCrate
	if BrawlAPI.RootNode == None or BrawlAPI.RootNode.FilePath != tracklistFolderPath:
		BrawlAPI.OpenFile(tracklistFolderPath)
	
	# Progress bar start
	progressBar = ProgressWindow()
	progressBar.Begin(0, len(BrawlAPI.RootNode.Children), 0)
	filesOpenedCount = 0
	
	# Loop through all files in tracklist folder
	for node in BrawlAPI.RootNode.Children:
		if isinstance(node, TLSTNode):
		
			# Update progress bar
			filesOpenedCount += 1
			progressBar.Update(filesOpenedCount)
			
			# Loop through entries in tracklist
			for track in node.Children:
				trackName = str(track.SongFileName)
				
				# If file exists, get its index and delete it from brstmFiles[]
				trackIndex = checkTrackName(track)
				if trackIndex >= 0:
					del brstmFiles[trackIndex]
					
					# Check pinch mode track (trackname_b.brstm)
					if track.SongSwitch:
						pinchIndex = getPinchTrackIndex(track)
						if pinchIndex >= 0:
							del brstmFiles[getPinchTrackIndex(track)]
		
		# If all brstm files are used, stop checking
		if len(brstmFiles) == 0:
			break
			
	# Progress bar close
	progressBar.Finish()
	
	# Reopen previously-opened file
	if initialOpenedFile:
		BrawlAPI.OpenFile(initialOpenedFile)
	
	# RESULTS
	# If no unused files found, show success dialog
	if not len(brstmFiles):
		message = "No unused BRSTM files detected!" + \
		"\n(" + str(BRSTM_FILE_COUNT) + " files)"
		
		# If any Brawl file IDs detected, list them to be safe
		if len(brawlBrstmFiles):
			message += "\n\nBrawl song IDs found (possibly used):\n"
			for i in brawlBrstmFiles:
				message += i + "\n"
		
		BrawlAPI.ShowMessage(message, "Success!")
		return
	
	# If unused files found
	message = "Unused BRSTM files detected:\n\n"
	MAX_BRAWL_LIST = 5
	MAX_CUSTOM_LIST = 25
	brawlListPrintedCount = 0
	customListPrintedCount = 0
	
	# List unused song files with Brawl IDs
	# If greater than max limit, cut off list
	while brawlListPrintedCount < MAX_BRAWL_LIST and brawlListPrintedCount < len(brawlBrstmFiles):
		name = brawlBrstmFiles[brawlListPrintedCount]
		message += name + " (Brawl song ID: possibly used)\n"
		brawlListPrintedCount += 1
	
	# Truncate list at MAX_BRAWL_LIST
	if MAX_BRAWL_LIST < len(brawlBrstmFiles):
		message += "...and " + str((len(brawlBrstmFiles) - MAX_BRAWL_LIST)) + " more\n"
	
	# List unused brstm files with custom names
	while customListPrintedCount < MAX_CUSTOM_LIST and customListPrintedCount < len(brstmFiles):
		name = brstmFiles[customListPrintedCount]
		message += name + "\n"
		customListPrintedCount += 1
	
	# Truncate list at MAX_CUSTOM_LIST
	if MAX_CUSTOM_LIST < len(brstmFiles):
		message += "...and " + str((len(brstmFiles) - MAX_CUSTOM_LIST)) + " more\n"
	
	# Prompt to delete unused files
	message += "\n\nDelete these BRSTM files?"
	if brawlListPrintedCount:
		message += "\n(Files with Brawl song IDs will not be deleted.)"
	if not BrawlAPI.ShowYesNoWarning(message, SCRIPT_NAME):
		return
	
	# Delete files confirmation prompt
	msg = "Deleting these BRSTM files is irreversible. They will be not be moved to the Recycle Bin, but be erased from your hard drive.\nAre you sure you want to continue?"
	if not (BrawlAPI.ShowYesNoWarning(msg, SCRIPT_NAME)):
		return
	
	# Loop through unused files and delete
	for fileName in brstmFiles:
		File.Delete(strmFolderPath + fileName)
	
	BrawlAPI.ShowMessage(str(len(fileNameList)) + " unused BRSTM files deleted.", SCRIPT_NAME)

main()
