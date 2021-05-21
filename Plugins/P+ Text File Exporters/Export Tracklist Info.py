__author__ = "mawwwk"
__version__ = "1.5.1"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from mawwwkLib import *

OUTPUT_TEXT_FILENAME = "_Tracklist Data.txt"
 
missingPathTracklists = []		# Names of tlst nodes which contain missing file paths
missingTracks = []				# Track names corresponding to missing file paths
duplicateIDsTracklists = []		# Names of tlst nodes with duplicate song IDs
existingFilePaths = []			# Saves any found file paths, for faster checks

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
	
		# Append Brawl track to tracklist string, including BRSTM filename and hex ID
		brawlBrstmFilePath = track.BrawlBRSTMs[track.SongID] + ".brstm"
		brawlSongHex = formatHex(track.SongID)
		
		# Return formatted string containing filepath and Brawl hex ID
		return brawlBrstmFilePath + " (" + brawlSongHex + ")"
	
	# If file path isn't empty, the track is a custom .brstm
	else:
		
		# Derive filepath string
		trackStr = str(track.SongFileName) + ".brstm"
		trackFilePath = track.rstmPath
		
		# If track filepath has already been found, return it without extra checks
		if trackFilePath in existingFilePaths:
			return trackStr
			
		# If brstm file is missing, add it to the "missing" list and mark it accordingly in output
		elif track.SongFileName not in BRAWL_SONG_ID_LIST and not File.Exists(trackFilePath):
			missingPathTracklists.append(str(parentNode.Name) + ".tlst")
			missingTracks.append(str(track.SongFileName) + ".brstm")
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
		missingPathTracklists.append(str(parentNode.Name) + ".tlst")
		missingTracks.append(str(track.SongFileName) + "_b.brstm")
		trackStr += " [BRSTM FILE MISSING]"
		
	return trackStr

## End helper methods
## Start of main script

# Prompt for the pf or tracklist directory
tracklistDir = BrawlAPI.OpenFolderDialog("Open pf or tracklist folder")

if str(tracklistDir).endswith("\\pf"):
	tracklistDir += "\\sound\\tracklist"
elif str(tracklistDir).endswith("\\pf\\sound"):
	tracklistDir += "\\tracklist"
	
if tracklistDir and "tracklist" not in tracklistDir and "netplaylist" not in tracklistDir:
	BrawlAPI.ShowError("Invalid directory", "Error")

elif tracklistDir:

	# Confirm dialog box
	message = "Contents of all tracklists in the folder\n\n" + str(tracklistDir)
	message += "\nwill be exported to " + str(OUTPUT_TEXT_FILENAME) + " in the same folder."
	message += "\n\nPress OK to continue. (The process may take 1-2 minutes.)"
	
	if BrawlAPI.ShowOKCancelPrompt(message, "Export Tracklist File Data"):
		
		# Store currently opened file
		CURRENT_OPEN_FILE = getOpenFile()
		
		# Get list of TLST files in tracklist directory
		TRACKLIST_FILES = Directory.CreateDirectory(tracklistDir).GetFiles()
		TLST_FILE_COUNT = len(TRACKLIST_FILES)
		
		# Open text file and clear it, or create if it doesn't already exist
		FULL_TEXT_FILE_PATH = str(tracklistDir) + "\\" + OUTPUT_TEXT_FILENAME
		textfile = open(FULL_TEXT_FILE_PATH,"w+")
		
		tracklistCount = 0	# Number of opened files
		
		# Progress bar start
		progressBar = ProgressWindow()
		progressBar.Begin(0,TLST_FILE_COUNT,0)
		
		# Iterate through all TLST files in folder
		for file in TRACKLIST_FILES:
			if file.Name.lower().EndsWith(".tlst"):
				currentTracklist = ""	# Clear current tracklist output string
				songIDsInTracklist = []	# Clear current tracklist song IDs
				
				# Update progress bar
				tracklistCount += 1
				progressBar.Update(tracklistCount)
				
				# Open TLST file
				BrawlAPI.OpenFile(file.FullName)
				parentNode = BrawlAPI.RootNode
				
				# Write header (tracklist filename and number of tracks)
				writeHeader(textfile, parentNode)

				# Iterate through entry nodes
				for track in parentNode.Children:
				
					# Check for any duplicate song IDs
					if parentNode.Name + ".tlst" not in duplicateIDsTracklists and track.SongID in songIDsInTracklist:
						duplicateIDsTracklists.append(str(parentNode.Name) + ".tlst")
						
					# If not a duplicate, add to songIDs list
					else:
						songIDsInTracklist.append(track.SongID)
						
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
					
				# When finished parsing the current TLST, output the tracklist info to text
				textfile.write(currentTracklist)
		
		# After all TLSTs are parsed, close text file
		textfile.close()
		progressBar.Finish()
		
		# Reopen previously-opened file
		if CURRENT_OPEN_FILE:
			BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
		
		# RESULTS
		
		missingPathFound = len(missingPathTracklists)
		duplicateSongIDsFound = len(duplicateIDsTracklists)
		
		# Success, no errors
		if not missingPathFound and not duplicateSongIDsFound and tracklistCount > 0:
			BrawlAPI.ShowMessage("Contents of " + str(tracklistCount) + " tlst files exported with no errors to:\n" + str(FULL_TEXT_FILE_PATH), "Success!")
		
		# Success, but one or more brstm files missing in sound/strm folder
		if missingPathFound:
			message = ""
			for i in range(0, min(len(missingPathTracklists), 10),1):
				message += "\n" + str(missingPathTracklists[i]) + ":\n"
				message += str(missingTracks[i]) + "\n"
			
			BrawlAPI.ShowError("Tracklist contents exported successfully. \n\n" + \
			str(len(missingTracks)) + " brstm file(s) missing:\n" + message, "BRSTMs missing")
		
		# Success, but one or more tracklists has duplicate Song ID values
		if duplicateSongIDsFound:
			message = ""
			for tracklist in duplicateIDsTracklists:
				message += "\n" + str(tracklist)
			
			BrawlAPI.ShowError("Tracklist contents exported successfully.\n\n" + \
			str(len(duplicateIDsTracklists)) + " tracklist(s) have duplicate song IDs:\n" + message, "Duplicate song IDs found")
		
		# No tracklists found
		elif tracklistCount == 0:
			BrawlAPI.ShowError("No tlst files found in\n" + str(tracklistDir), "No tracklists found")
