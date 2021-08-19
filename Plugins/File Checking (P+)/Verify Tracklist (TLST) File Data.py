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

SCRIPT_NAME = "Verify Tracklist File Data"
OUTPUT_TEXT_FILENAME = "_Tracklist Data.txt"
missingTracks = []				# List of [tracklists, tracks with missing file paths]
existingFilePaths = []			# Saves any found file paths, for faster checks

## End global variables
## Begin helper methods

# Print header for each tracklist containing filename and number of tracks
def writeHeader(textfile, parentNode):
	trackCount = len(parentNode.Children)
	
	writeStr = "################\n" + str(parentNode.Name) + ".tlst - "
	
	if trackCount == 1:
		writeStr += "1 track\n\n"
	else:
		writeStr += str(trackCount) + " tracks\n\n"

	textfile.write(writeStr)

# Get file path of a brstm given a track node
def getBrstmFilePath(track):

	# If file path is empty, track should be from ISO
	if str(track.SongFileName) == "None":
	
		# Append Brawl track to tracklist string using static BrawlCrate dict
		brawlBrstmFilePath = track.BrawlBRSTMs[track.SongID] + ".brstm"
		brawlSongHex = formatHex(track.SongID)
		
		# Return formatted string containing filepath and Brawl hex ID
		return brawlBrstmFilePath + " (" + brawlSongHex + ")"
	
	# If file path isn't empty, the track is a custom .brstm
	else:
		
		# Derive filepath string
		trackStr = str(track.SongFileName) + ".brstm"
		
		# If track filepath has already been found, return it without extra checks
		if track.rstmPath in existingFilePaths:
			return trackStr
			
		# If brstm file is missing, add it to the "missing" list and mark it accordingly in output
		elif track.SongFileName not in BRAWL_SONG_ID_LIST and not File.Exists(track.rstmPath):
			tracklistName = str(track.Parent.Name) + ".tlst"
			missingTrackName = str(track.SongFileName) + ".brstm"
			missingTracks.append([tracklistName, missingTrackName])
			
			return trackStr + " [BRSTM FILE MISSING]"
		
		# If brstm file exists, save it in existingFilePaths[] for easier future checking, and return filepath
		else:
			existingFilePaths.append(track.rstmPath)
			return trackStr

# Get pinch mode info
def getPinchModeStr(track):
	trackStr = "[PINCH MODE TRACK: " + str(track.SongSwitch) + " frames]\n"
	trackStr += "\t" + str(track.SongFileName) + "_b.brstm"
	
	# Check if pinch brstm file exists
	if not File.Exists(str(track.rstmPath)[0:-6] + "_b.brstm"):
		tracklistName = str(track.Parent.Name) + ".tlst"
		missingTrackName = str(track.SongFileName) + "_b.brstm"
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
		workingDir += "\\sound\\tracklist"
	elif str(workingDir).endswith("\\pf\\sound"):
		workingDir += "\\tracklist"
	
	# Confirm dialog box
	message = "Contents of all tracklists in the folder:\n" + str(workingDir) + "\\"
	message += "\nwill be checked for valid track filepaths and properties."
	message += "\n\nPress OK to continue. (The process may take 20 seconds or longer.)"
	
	if BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
		
		SHORT_PATH = workingDir.rsplit("\\",1)[1] + "/" + OUTPUT_TEXT_FILENAME
		DO_FILE_WRITE = BrawlAPI.ShowYesNoPrompt("Output results to /" + SHORT_PATH + "?", SCRIPT_NAME)
		
		# Store currently opened file
		CURRENT_OPEN_FILE = getOpenFile()
		
		# Get list of TLST files in tracklist directory
		TRACKLIST_FILES = Directory.CreateDirectory(workingDir).GetFiles()
		TLST_FILE_COUNT = len(TRACKLIST_FILES)
		
		# If file writing is enabled, open text file and clear it, or create if it doesn't already exist
		if DO_FILE_WRITE:
			FULL_TEXT_FILE_PATH = str(workingDir) + "\\" + OUTPUT_TEXT_FILENAME
			TEXT_FILE = open(FULL_TEXT_FILE_PATH,"w+")
		
		tracklistOpenedCount = 0	# Number of opened files
		
		# Progress bar start
		progressBar = ProgressWindow()
		progressBar.Begin(0,TLST_FILE_COUNT,0)
		
		# Iterate through all TLST files in folder
		for file in TRACKLIST_FILES:
		
			if file.Name.lower().EndsWith(".tlst"):
				tracklistOpenedCount += 1
				currentTracklist = ""	# Clear current tracklist output string
				tracklistSongIDs = []	# Clear current tracklist song IDs
				
				# Update progress bar
				progressBar.Update(tracklistOpenedCount)
				
				# Open TLST file
				BrawlAPI.OpenFile(file.FullName)
				parentNode = BrawlAPI.RootNode
				
				# If file writing enabled, write header (filename and track count)
				if DO_FILE_WRITE:
					writeHeader(TEXT_FILE, parentNode)

				# Iterate through entry nodes
				for track in parentNode.Children:
					
					# Check for any duplicate song IDs
					if track.SongID in tracklistSongIDs and parentNode.Name not in duplicateIDsTracklists:
						duplicateIDsTracklists.append(str(parentNode.Name) + ".tlst")
						
					# If not a duplicate, add to songIDs list
					else:
						tracklistSongIDs.append(track.SongID)
						
					# Add track name and filepath to output string
					currentTracklist += "\t" + str(track.Name) + "\n"
					currentTracklist += "\t" + getBrstmFilePath(track) + "\n"
					
					# If track is from SD card, get volume
					if str(track.SongFileName) != "None":
						currentTracklist += "\tVolume: " + str(track.Volume) + "\n"
						
					# If songSwitch is enabled, check for pinch mode brstm and print info
					if track.SongSwitch:
						currentTracklist += "\t" + getPinchModeStr(track) + "\n"
					
					# Append frequency to output string
					currentTracklist += "\tFrequency: " + str(track.Frequency) + "\n"
					
					# Append song delay to string, if exists
					if track.SongDelay != 0:
						currentTracklist += "\tSong delay: " + str(track.SongDelay) + "\n"
				
					currentTracklist += "\n"
					
				# If file writing is enabled, output all above info to text
				if DO_FILE_WRITE:
					TEXT_FILE.write(currentTracklist)
		
		# After all TLSTs are parsed, close text file
		if DO_FILE_WRITE:
			TEXT_FILE.close()
		
		progressBar.Finish()
		
		# Reopen previously-opened file
		if CURRENT_OPEN_FILE:
			BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
		
		# START RESULTS
		
		# Results: If no tracklists found
		if tracklistOpenedCount == 0:
			BrawlAPI.ShowError("No tlst files found in\n" + str(workingDir), "No tracklists found")
			return
		
		# Determine whether any errors were found
		isMissingTracks = len(missingTracks)
		isDuplicateIDs = len(duplicateIDsTracklists)
		
		# Results: If errors found
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
					missingTracklistMessage += "...and " + str(ERROR_LIST_MAX - isMissingTracks) + " more."
			
			# If one or more tracklists have duplicate Song ID values, list them in error message
			if isDuplicateIDs:
				duplicateIDMessage = str(isDuplicateIDs) + " tracklist(s) use duplicate song IDs:\n"
				
				# Fill message with duplicate song ID tracklists, up to ERROR_LIST_MAX
				
				for i in range(0, min(isDuplicateIDs, ERROR_LIST_MAX), 1):
					duplicateIDMessage += "\n" + str(duplicateIDsTracklists[i]) + "\n"
				
				if isDuplicateIDs > ERROR_LIST_MAX:
					duplicateIDMessage += "...and " + str(ERROR_LIST_MAX - isDuplicateIDs) + " more."
			# Show error message using above logs
			BrawlAPI.ShowError(missingTracklistMessage + "\n" + duplicateIDMessage, "Error")
		
		# Results: Success, file write enabled
		elif DO_FILE_WRITE:
			BrawlAPI.ShowMessage("Contents of " + str(tracklistOpenedCount) + " tracklist files exported with no errors to:\n" + str(FULL_TEXT_FILE_PATH), "Success!")
		
		# Results: Success, no file write
		else:
			BrawlAPI.ShowMessage("Contents of " + str(tracklistOpenedCount) + " tracklist files verified with no errors.", "Success!")

main()
