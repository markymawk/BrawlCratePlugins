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

SCRIPT_NAME = "Verify Tracklist File Data"
OUTPUT_TEXT_FILENAME = "_Tracklist Data.txt"
missingTracks = []				# List of [tracklists, tracks with missing file paths]
existingFilePaths = []			# Saves any found file paths, for fewer hard drive checks

## End global variables
## Begin helper methods

# Print header for each tracklist containing filename and number of tracks
def getHeader(parentNode):
	trackCount = len(parentNode.Children)
	
	headerStr = "################\n" + str(parentNode.Name) + ".tlst - "
	
	if trackCount == 1:
		headerStr += "1 track\n\n"
	else:
		headerStr += str(trackCount) + " tracks\n\n"

	return headerStr

# Get file path of a brstm given a track node
def checkBRSTMFilePath(trackNode):
	brstmString = ""
	
	# If file path is empty (track is from ISO)
	if str(trackNode.SongFileName) == "None":
	
		# Append Brawl track to tracklist string using static BrawlCrate dict
		brawlBrstmFilePath = trackNode.BrawlBRSTMs[trackNode.SongID] + ".brstm"
		brawlSongHex = formatHex(trackNode.SongID)
		
		# Return formatted string containing filepath and Brawl hex ID
		brstmString = brawlBrstmFilePath + " (" + brawlSongHex + ")"
	
	# If track is a custom BRSTM
	else:
		
		# Derive filepath string
		brstmString = str(trackNode.SongFileName) + ".brstm"
		
		# If track filepath has already been found in this script run, return it without extra checks
		if trackNode.rstmPath in existingFilePaths:
			return brstmString
		
		trackExists = trackNode.SongFileName in BRAWL_SONG_ID_LIST or File.Exists(trackNode.rstmPath)
		
		# If brstm file exists, add it to existingFilePaths[] for easier checks
		if trackExists:
			existingFilePaths.append(trackNode.rstmPath)
		
		# If brstm file is missing, add it to the "missing" list and mark it accordingly in output
		else:
			tlstName = str(trackNode.Parent.Name) + ".tlst"
			trackName = str(trackNode.SongFileName) + ".brstm"
			missingTracks.append([tlstName, trackName])
			
			brstmString += " [BRSTM FILE MISSING]"
		
	return brstmString

# Get pinch mode info
def getPinchModeStr(trackNode):
	trackStr = "[PINCH MODE TRACK: " + str(trackNode.SongSwitch) + " frames]\n"
	trackStr += "\t" + str(trackNode.SongFileName) + "_b.brstm"
	
	# If pinch brstm file doesn't exist, append to missingTracks[] and indicate such in the string
	if not File.Exists(str(trackNode.rstmPath)[0:-6] + "_b.brstm"):
		tracklistName = str(trackNode.Parent.Name) + ".tlst"
		missingTrackName = str(trackNode.SongFileName) + "_b.brstm"
		missingTracks.append([tracklistName, missingTrackName])

		trackStr += " [BRSTM FILE MISSING]"
		
	return trackStr

## End helper methods
## Start of main script

def main():
	duplicateIDsTracklists = []		# Names of tlst nodes with duplicate song IDs
	
	# Prompt for the pf or tracklist directory
	workingDir = BrawlAPI.OpenFolderDialog("Open pf or tracklist folder")
	if not workingDir:
		return
	
	if str(workingDir).endswith("\\pf"):
		workingDir += "\\sound\\tracklist\\"
	elif str(workingDir).endswith("\\pf\\sound"):
		workingDir += "\\tracklist\\"
	else:
		workingDir += "\\"
	
	# Confirm dialog box
	START_MSG = "Contents of all tracklists in the folder:\n" + str(workingDir)
	START_MSG += "\nwill be checked for valid track filepaths and properties."
	START_MSG += "\n\nPress OK to continue."
	
	if not BrawlAPI.ShowOKCancelPrompt(START_MSG, SCRIPT_NAME):
		return
	
	# File output prompt
	SHORT_PATH = workingDir.rsplit("\\",2)[1] + "/" + OUTPUT_TEXT_FILENAME
	DO_FILE_WRITE = BrawlAPI.ShowYesNoPrompt("Output results to /" + SHORT_PATH + "?", SCRIPT_NAME)
	
	# If file writing is enabled, open AppPath temp text file
	if DO_FILE_WRITE:
		TEMP_TEXT_FILE_PATH = AppPath + OUTPUT_TEXT_FILENAME
		FULL_TEXT_FILE_PATH = str(workingDir) + OUTPUT_TEXT_FILENAME
		TEXT_FILE = open(TEMP_TEXT_FILE_PATH,"w+", encoding="utf-8")
	
	# Open whole tracklist folder in BrawlCrate
	if BrawlAPI.RootNode == None or BrawlAPI.RootNode.FilePath != workingDir:
		BrawlAPI.OpenFile(workingDir)
	
	# Progress bar start
	progressBar = ProgressWindow()
	progressBar.Begin(0,len(BrawlAPI.RootNode.Children),0)
	
	tracklistOpenedCount = 0	# Number of opened files
	
	# Check all TLST files in folder
	for tlstNode in BrawlAPI.NodeListofType[TLSTNode]():
		tracklistOpenedCount += 1
		currentTracklist = ""	# Current tracklist output string
		tracklistSongIDs = []	# Current tracklist song IDs
		
		# Progress bar
		progressBar.Update(tracklistOpenedCount)
		
		# Loop through tracklist entries
		for trackNode in tlstNode.Children:
		
			# Check for any duplicate song IDs
			if trackNode.SongID in tracklistSongIDs and tlstNode.Name not in duplicateIDsTracklists:
				duplicateIDsTracklists.append(tlstNode.Name)
				
			# If not a duplicate, add to songIDs list
			else:
				tracklistSongIDs.append(trackNode.SongID)
				
			# Check track name and filepath, and store in a string (regardless of file write)
			currentTracklist += "\t" + str(trackNode.Name) + "\n"
			currentTracklist += "\t" + checkBRSTMFilePath(trackNode) + "\n"
			
			# If track is from SD card, get volume
			if str(trackNode.SongFileName) != "None":
				currentTracklist += "\tVolume: " + str(trackNode.Volume) + "\n"
				
			# If songSwitch is enabled, check for pinch mode brstm and print info
			if trackNode.SongSwitch:
				currentTracklist += "\t" + getPinchModeStr(trackNode) + "\n"
		
			# If file writing is enabled, check frequency and songDelay
			if DO_FILE_WRITE:
				currentTracklist += "\tFrequency: " + str(trackNode.Frequency) + "\n"
				if trackNode.SongDelay != 0:
					currentTracklist += "\tSong delay: " + str(trackNode.SongDelay) + "\n"
				currentTracklist += "\n"
		
		if DO_FILE_WRITE:
			TEXT_FILE.write(getHeader(tlstNode))
			TEXT_FILE.write(currentTracklist)
	
	# After all TLSTs are parsed, close text file, and copy from temp folder to tracklist folder
	if DO_FILE_WRITE:
		TEXT_FILE.close()
		File.Copy(TEMP_TEXT_FILE_PATH, FULL_TEXT_FILE_PATH, True)
		File.Delete(TEMP_TEXT_FILE_PATH) # File.Move() doesn't work?
		
	progressBar.Finish()
	
	# RESULTS
	
	# Results: If no tracklists found
	if tracklistOpenedCount == 0:
		BrawlAPI.ShowError("No tlst files found in\n" + str(workingDir), "No tracklists found")
		return
	
	# Determine whether any errors were found
	isMissingTracks = len(missingTracks)
	isDuplicateIDs = len(duplicateIDsTracklists)
	
	# Results

	# If errors found
	if isMissingTracks or isDuplicateIDs:
		ERROR_LIST_MAX = 10
		missingTracklistMessage = ""
		duplicateIDMessage = ""
		
		# If one or more brstm files missing in sound/strm folder, list them in an error message
		if isMissingTracks:
			missingTracklistMessage = str(isMissingTracks) + " brstm file(s) missing:\n"
			
			# Fill message with missing track names, up to ERROR_LIST_MAX
			for i in range(0, min(isMissingTracks, ERROR_LIST_MAX), 1):
				missingTracklistMessage += "\n" + str(missingTracks[i][0]) + ":\n"
				missingTracklistMessage += str(missingTracks[i][1]) + "\n"
				
			if isMissingTracks > ERROR_LIST_MAX:
				missingTracklistMessage += "...and " + str(isMissingTracks - ERROR_LIST_MAX) + " more."
		
		# If one or more tracklists have duplicate Song ID values, list them in error message
		if isDuplicateIDs:
			duplicateIDMessage = str(isDuplicateIDs) + " tracklist(s) use duplicate song IDs:\n"
			
			# Fill message with duplicate song ID tracklists, up to ERROR_LIST_MAX
			
			for i in range(0, min(isDuplicateIDs, ERROR_LIST_MAX), 1):
				duplicateIDMessage += "\n" + str(duplicateIDsTracklists[i]) + ".tlst\n"
			
			if isDuplicateIDs > ERROR_LIST_MAX:
				duplicateIDMessage += "...and " + str(isDuplicateIDs - ERROR_LIST_MAX) + " more."
				
		# Show error message
		BrawlAPI.ShowError(missingTracklistMessage + "\n" + duplicateIDMessage, "Error")
	
	# Success, no errors, file write enabled
	elif DO_FILE_WRITE:
		BrawlAPI.ShowMessage("Contents of " + str(tracklistOpenedCount) + " tracklist files exported with no errors to:\n" + str(FULL_TEXT_FILE_PATH), "Success!")
	
	# Success, no errors, no file write
	else:
		BrawlAPI.ShowMessage("Contents of " + str(tracklistOpenedCount) + " tracklist files verified with no errors.", "Success!")

main()
