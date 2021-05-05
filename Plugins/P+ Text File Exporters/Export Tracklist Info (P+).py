__author__ = "mawwwk"
__version__ = "1.5"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow

BRAWL_SONG_ID_LIST = [ "X02", "X03", "X04", "X05", "X06", "X07", "X08", "X09", "X10", "X11", "X12", "X13", "X14", "X15", "X16", "X17",
 "X18", "X19", "X20", "X21", "X22", "X23", "X24", "X25", "X26", "X27", "A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09",
 "A10", "A11", "A12", "A13", "A14", "A15", "A16", "A17", "A20", "A21", "A22", "A23", "B01", "B02", "B03", "B04", "B05", "B06", "B07",
 "B08", "B09", "B10", "C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12", "C13", "C14", "C15", "C16",
 "C17", "C18", "C19", "D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "E01", "E02", "E03", "E04", "E05", "E06",
 "E07", "F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10", "F11", "F12", "G01", "G02", "G03", "G04", "G05", "G06",
 "G07", "G08", "G09", "G10", "G11", "H01", "H02", "H03", "H04", "H05", "H06", "H07", "H08", "H09", "H10", "I01", "I02", "I03", "I04",
 "I05", "I06", "I07", "I08", "I09", "I10", "J01", "J02", "J03", "J04", "J05", "J06", "J07", "J08", "J09", "J10", "J11", "J12", "J13",
 "K01", "K02", "K03", "K04", "K05", "K06", "K07", "K08", "K09", "K10", "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "M01",
 "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "N01", "N02",
 "N03", "N04", "N05", "N06", "N07", "N08", "N09", "N10", "N11", "N12", "P01", "P02", "P03", "P04", "Q01", "Q02", "Q03", "Q04", "Q05",
 "Q06", "Q07", "Q08", "Q09", "Q10", "Q11", "Q12", "Q13", "Q14", "R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R09", "R10",
 "R11", "R12", "R13", "R14", "R15", "R16", "R17", "S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "T01",
 "T02", "T03", "T04", "T05", "U01", "U02", "U03", "U04", "U05", "U06", "U07", "U08", "U09", "U10", "U11", "U12", "U13", "W01", "W02",
 "W03", "W04", "W05", "W06", "W07", "W08", "W09", "W10", "W11", "W12", "W13", "W14", "W15", "W16", "W17", "W18", "W19", "W20", "W21",
 "W22", "W23", "W24", "W25", "W26", "W27", "W28", "W29", "W30", "W31", "W32", "Y01", "Y02", "Y03", "Y04", "Y05", "Y06", "Y07", "Y08",
 "Y09", "Y10", "Y11", "Y12", "Y13", "Y14", "Y15", "Y16", "Y17", "Y18", "Y19", "Y20", "Y21", "Y22", "Y23", "Y24", "Y25", "Y26", "Y27",
 "Y28", "Y29", "Y30", "Z01", "Z02", "Z03", "Z04", "Z05", "Z06", "Z07", "Z08", "Z09", "Z10", "Z11", "Z12", "Z13", "Z14", "Z15", "Z16",
 "Z17", "Z18", "Z19", "Z20", "Z21", "Z22", "Z23", "Z24", "Z25", "Z26", "Z27", "Z28", "Z32", "Z33", "Z34", "Z35", "Z37", "Z38", "Z39",
 "Z41", "Z46", "Z47", "Z50", "Z51", "Z52", "Z53", "Z54", "Z55", "Z56" "Z57", "Z58"]

OUTPUT_TEXT_FILENAME = "_Tracklist Data.txt"
 
missingPathTracklists = []		# Global list, contains the names of tlst nodes which contain missing file paths
missingTracks = []				# Global list, contains the track names corresponding to missing file paths
duplicateIDsTracklists = []		# Global list, contains the names of tlst nodes with duplicate song IDs
existingFilePaths = []			# Global list, contains any found file paths for faster checks

DO_ERROR_CHECKING = True		# Set to False to ignore checks for duplicate SongIDs or missing filepaths. Might save time

# Print header for each tracklist containing filename and number of tracks
def writeTracklistHeader(textfile, parentNode):
	trackCount = len(parentNode.Children)
	
	writeStr = "################\n" + str(parentNode.Name) + ".tlst - "
	
	if trackCount == 1:
		writeStr += "1 track\n\n"
	else:
		writeStr += str(trackCount) + " tracks\n\n"

	textfile.write(writeStr)

# Function to get file path of a brstm given a track node
def getBrstmFilePath(track):
	# If file path is empty, track should be from ISO
	if str(track.SongFileName) == "None":
		# Append Brawl track to tracklist string, including BRSTM filename and hex ID
		brawlBrstmFilePath = track.BrawlBRSTMs[track.SongID] + ".brstm"
		brawlSongHex = getBrawlSongHex(track.SongID)
		
		# Return formatted string containing filepath and Brawl hex ID
		return brawlBrstmFilePath + " (" + brawlSongHex + ")"
	
	# If file path isn't empty, the track is a custom .brstm
	else:
		# Start with custom filepath string
		trackStr = str(track.SongFileName) + ".brstm"
		trackFilePath = track.rstmPath
		
		# If track filepath has already been found, return it without extra checks
		if trackFilePath in existingFilePaths:
			return trackStr
			
		# If brstm file is missing, add it to the "missing" list and mark it accordingly in output
		elif DO_ERROR_CHECKING and track.SongFileName not in BRAWL_SONG_ID_LIST and not File.Exists(trackFilePath):
			missingPathTracklists.append(str(parentNode.Name) + ".tlst")
			missingTracks.append(str(track.SongFileName) + ".brstm")
			return trackStr + " [BRSTM FILE MISSING]"
		
		# If brstm file exists, save it in existingFilePaths[] for easier future checking, and return filepath
		else:
			existingFilePaths.append(track.rstmPath)
			return trackStr

# Function to get pinch mode info if applicable
def getPinchModeStr(track):
	trackStr = ""
	
	if track.SongSwitch:
		trackStr += "[PINCH MODE TRACK: " + str(track.SongSwitch) + " frames]\n\t" + str(track.SongFileName) + "_b.brstm"
		
		if DO_ERROR_CHECKING and not File.Exists(str(track.rstmPath)[0:-6] + "_b.brstm"):
			missingPathTracklists.append(str(parentNode.Name) + ".tlst")
			missingTracks.append(str(track.SongFileName) + "_b.brstm")
			trackStr += " [BRSTM FILE MISSING]"
		
	return trackStr
	
# Convert to hex with lowercase 0x, and cut off trailing L
def getBrawlSongHex(songID):
	return "0x" + str(hex(songID)).upper()[2:-1]

############################################
########### Start of main script ###########
############################################

# Prompt for the pf or tracklist directory
tracklistDir = BrawlAPI.OpenFolderDialog("Open pf or tracklist folder")

if str(tracklistDir)[-3:] == "\\pf":
	tracklistDir += "\\sound\\tracklist"
elif str(tracklistDir)[-9:] == "\\pf\\sound":
	tracklistDir += "\\tracklist"

if tracklistDir:
	if BrawlAPI.RootNode:
		CURRENT_OPEN_FILE = str(BrawlAPI.RootNode.FilePath)
	else:
		CURRENT_OPEN_FILE = 0
		
	# Get list of TLST files in tracklist directory
	TRACKLIST_FILES = Directory.CreateDirectory(tracklistDir).GetFiles()
	TLST_FILE_COUNT = len(TRACKLIST_FILES)
	
	# Confirm dialog box
	message = "Contents of all tracklists in the folder\n\n" + str(tracklistDir)
	message += "\nwill be exported to " + str(OUTPUT_TEXT_FILENAME) + " in the same folder."
	message += "\n\nPress OK to continue. (The process may take 1-2 minutes.)"
	
	if BrawlAPI.ShowOKCancelPrompt(message, "Export Tracklist File Data"):
		
		# Open text file and clear it, or create if it doesn't already exist
		FULL_TEXT_FILE_PATH = str(tracklistDir) + "\\" + OUTPUT_TEXT_FILENAME
		textfile = open(FULL_TEXT_FILE_PATH,"w+")
		
		###
		### Debug or advanced users: un-comment this dialog box to disable error checking.
		### Didn't save much time for me, but may be helpful for slower PCs or for doing repetitive updates.
		
		### message = "Check tracklists for errors? \n\nThis takes a bit longer, but will find any missing tracks or duplicate IDs."
		### DO_ERROR_CHECKING = BrawlAPI.ShowYesNoPrompt(message, "Export Tracklist Data")
		###
		
		tracklistCount = 0	# Number of opened files
		
		# Progress bar start
		progressBar = ProgressWindow()
		progressBar.Begin(0,TLST_FILE_COUNT,0)
		
		# Iterate through all TLST files in folder
		for file in TRACKLIST_FILES:
			if file.Name.lower().EndsWith(".tlst"):
				currentTracklist = ""	# Clear current tracklist output str
				songIDsInTracklist = []	# Clear current tracklist song IDs
				
				# Update progress bar
				tracklistCount += 1
				progressBar.Update(tracklistCount)
				
				# Open TLST file
				BrawlAPI.OpenFile(file.FullName)
				parentNode = BrawlAPI.RootNode
				
				# Write header (tracklist filename and number of tracks)
				writeTracklistHeader(textfile, parentNode)

				# Iterate through entry nodes
				for track in parentNode.Children:
				
					# Check for any duplicate song IDs
					if DO_ERROR_CHECKING:
						if (str(parentNode.Name) + ".tlst") not in duplicateIDsTracklists and track.SongID in songIDsInTracklist:
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
					
				# When finished parsing the current TLST, close the TLST file and output the tracklist info to text
				BrawlAPI.ForceCloseFile()
				textfile.write(currentTracklist)
		
		# After all TLSTs are parsed, close text file
		textfile.close()
		progressBar.Finish()
		
		# Reopen previously-opened file
		if CURRENT_OPEN_FILE:
			BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
		
		# RESULTS
		
		if DO_ERROR_CHECKING:
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
			
		else:
			BrawlAPI.ShowMessage("Contents of " + str(tracklistCount) + " tlst files exported to:\n" + str(FULL_TEXT_FILE_PATH), "Success! (No error checking)")
