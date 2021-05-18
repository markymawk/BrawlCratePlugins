__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from BrawlLib.Imaging import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow

SCRIPT_NAME = "Detect Unused BRSTM Files"

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
		# Compare lower-case for case-insensitivity
		trackName = trackName.lower() + ".brstm"
		# Swap backslash (\) with forward slash (/) for consistency
		trackName = trackName.replace("\\", "/")
	#	dmessage(trackName)
		
		# If track is found, return index of the track
		for i in range(0, len(brstmFiles), 1):
			fileName = brstmFiles[i].lower()
			if trackName == fileName.lower():
				return i
	
	# If not found, return -1
	return -1

## End helper methods
## Start of main script

# Prompt for the pf or sound directory
workingDir = BrawlAPI.OpenFolderDialog("Open pf, sound, or strm folder")
workingDir = str(workingDir)

# Derive strm and tracklist folder paths
[STRM_DIR, TRACKLIST_DIR] = [0,0]
if workingDir[-3:] == "\\pf":
	STRM_DIR = workingDir + "\\sound\\strm"
	TRACKLIST_DIR = workingDir + "\\sound\\tracklist"
elif workingDir[-9:] == "\\pf\\sound":
	STRM_DIR = workingDir + "\\strm"
	TRACKLIST_DIR = workingDir + "\\tracklist"
elif workingDir [-5:] == "\\strm":
	STRM_DIR = workingDir
	TRACKLIST_DIR = workingDir.replace("\\strm", "\\tracklist")

if workingDir and not STRM_DIR:
	BrawlAPI.ShowError("Invalid directory", "Error")

elif workingDir:
	# Save currently opened file, if any
	if BrawlAPI.RootNode:
		CURRENT_OPEN_FILE = str(BrawlAPI.RootNode.FilePath)
	else:
		CURRENT_OPEN_FILE = 0
	
	# Initialize list of tracklist files to scan
	TRACKLIST_FILES = Directory.CreateDirectory(TRACKLIST_DIR).GetFiles()
	filesOpenedCount = 0	# Number of opened files
	
	# Get list of brstm file names in sound/strm directory, and store in brstmFiles[]
	populateBrstmFilesList(STRM_DIR)
	BRSTM_FILE_COUNT = len(brstmFiles)
	
	# Progress bar start
	progressBar = ProgressWindow()
	progressBar.Begin(0,len(TRACKLIST_FILES),0)
	
	# Iterate through all files in tracklist folder
	for file in TRACKLIST_FILES:
		
		# Update progress bar
		filesOpenedCount += 1
		progressBar.Update(filesOpenedCount)
		
		# Open tracklist file
		if file.Name.lower().EndsWith(".tlst"):
			BrawlAPI.OpenFile(file.FullName)
			
			# Iterate through entries in tracklist
			for track in BrawlAPI.RootNode.Children:
				trackName = str(track.SongFileName)
				
				# If file exists, get its index and delete it from brstmFiles[]
				trackIndex = checkTrackName(track)
				if trackIndex >= 0:
					del brstmFiles[trackIndex]
			
		# Stop the loop if all brstm files are used
		if len(brstmFiles) == 0:
			break
			
	# Progress bar close
	progressBar.Finish()
	
	# Reopen previously-opened file
	if CURRENT_OPEN_FILE:
		BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
	
	# RESULTS
	
	# If no unused files found, show success dialog
	if len(brstmFiles) == 0:
		message = "No unused BRSTM files detected!" + \
		"\n(" + str(BRSTM_FILE_COUNT) + " files)"
		
		# If any Brawl file IDs detected, list them to be safe
		if len(brawlBrstmFiles):
			message += "\n\nBrawl song IDs found (possibly used):\n"
			for i in brawlBrstmFiles:
				message += i + "\n"
		
		BrawlAPI.ShowMessage(message, "Success!")
	
	# If unused files found
	else:
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
			message += "...and" + str((len(brawlBrstmFiles) - MAX_BRAWL_LIST)) + " more\n"
		
		# List unused brstm files with custom names
		while customListPrintedCount < MAX_CUSTOM_LIST and customListPrintedCount < len(brstmFiles):
			name = brstmFiles[customListPrintedCount]
			message += name + "\n"
			customListPrintedCount += 1
		
		# Truncate list at MAX_CUSTOM_LIST
		if MAX_CUSTOM_LIST < len(brstmFiles):
			message += "...and " + str((len(brstmFiles) - MAX_CUSTOM_LIST)) + " more\n"
		
		BrawlAPI.ShowError(message, SCRIPT_NAME)
