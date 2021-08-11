__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from mawwwkLib import *

SCRIPT_NAME = "Copy Tracklist Frequencies"
tracksAffectedCount = 0 		# Count of tracks with changed properties after the script
isTracklistModified = False 	# Whether current tracklist has been changed
modifiedTrackNames = []			# Contains formatted strings containing TLST filename and track name

def setFrequency(trackNode, newValue):
	global tracksAffectedCount
	global isTracklistModified
	global modifiedTracklistNames
	
	if trackNode.Frequency != newValue:
		modifiedTrackNames.append(BrawlAPI.RootNode.FileName + ": " + trackNode.Name + " (" + str(trackNode.Frequency) + " > " + str(newValue) + ")")
		trackNode.Frequency = newValue
		tracksAffectedCount += 1
		isTracklistModified = True
	
def main():
	global isTracklistModified
	tracklistsAffectedCount = 0 # Count of tracklists edited
	openedFileCount = 0			# Number of files opened during the loop
	
	# Get source tracklist dir
	if BrawlAPI.ShowOKCancelPrompt(\
	"Copy track frequencies from one tracklist folder to another.\n\n"\
	"Click OK to continue, then choose the source tracklist folder to copy from (typically  Project+\pf\sound\tracklist)", SCRIPT_NAME):
		sourceDir = BrawlAPI.OpenFolderDialog("Choose source tracklist folder")
	else:
		return
	
	# Get dest tracklist dir
	if sourceDir and BrawlAPI.ShowOKCancelPrompt("Choose destination tracklist folder.", SCRIPT_NAME):
		destDir = BrawlAPI.OpenFolderDialog("Choose destination tracklist folder")
	else:
		return
	
	if not destDir:
		return
	
	# Store currently opened file
	CURRENT_OPEN_FILE = getOpenFile()
		
	SOURCE_DIR_FILES = Directory.CreateDirectory(sourceDir).GetFiles()
	
	# Progress bar start
	progressBar = ProgressWindow()
	progressBar.Begin(0,len(SOURCE_DIR_FILES),0)

	# Iterate through files in sourceDir
	for file in SOURCE_DIR_FILES:
		nameToFrequency = {}	# Primary dict used to assign freqs
		BRSTMToFrequency = {}	# Backup dict if song title is changed
		DEST_FILE_NAME = destDir + "\\" + file.Name
		
		# Update progress bar
		openedFileCount += 1
		progressBar.Update(openedFileCount)
		
		# If file is a TLST, and file.exists of same name in destination directory, then parse the tracklist
		if ".tlst" in file.Name and File.Exists(DEST_FILE_NAME):
		
			# Open source TLST file and iterate through tracks
			BrawlAPI.OpenFile(file.FullName)
			for track in BrawlAPI.RootNode.Children:
			
				# Append to trackName:frequency dict
				nameToFrequency[track.Name] = track.Frequency
				
				# If track is a custom track (SongID >= 0xF000), also build BRSTMPath:Frequency
				if track.SongID >= 61440 and len(track.SongFileName):
					BRSTMToFrequency[track.SongFileName] = track.Frequency
			
			# Store dictionary keys separately for ease
			trackNames = nameToFrequency.keys()
			brstmNames = BRSTMToFrequency.keys()
			
			# Open destDir file
			BrawlAPI.OpenFile(DEST_FILE_NAME)

			# Iterate through destination-track entries
			for track in BrawlAPI.RootNode.Children:
			
				# If trackName in dict, assign trackName:frequency
				if track.Name in trackNames:
					setFrequency(track, nameToFrequency[track.Name])
				
				# If track name is missing but BRSTM path is found in dict, assign BRSTMPath:frequency
				elif str(track.SongFileName) != "None" and track.SongFileName in brstmNames:
					setFrequency(track, BRSTMToFrequency[track.SongFileName])
					
			# If tracklist was changed, save file before closing, and increment affectedCount
			if isTracklistModified:
				tracklistsAffectedCount += 1
				isTracklistModified = False
				BrawlAPI.SaveFile()
				
	# Progress bar close
	progressBar.Finish()
	
	# Reopen previously-opened file
	if CURRENT_OPEN_FILE:
		BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
	# RESULTS
	
	if tracklistsAffectedCount >= 1:
		MAX_LIST = 30
		listPrintedCount = 0
		
		# List track names that have modified frequencies
		message = str(tracksAffectedCount) + " track frequency value(s) updated across " + str(tracklistsAffectedCount) + " tracklist(s)\n\n"
		
		# If greater than max limit, cut off list
		while listPrintedCount < MAX_LIST and listPrintedCount < len(modifiedTrackNames):
			message += modifiedTrackNames[listPrintedCount] + "\n"
			listPrintedCount += 1
		
		# Truncate list at MAX_LIST
		if MAX_LIST < len(modifiedTrackNames):
			message += "...and " + str((len(modifiedTrackNames) - MAX_LIST)) + " more"
		
		BrawlAPI.ShowMessage(message, "Success")

	else:
		BrawlAPI.ShowMessage("No track frequency changes detected. No files have been modified.", SCRIPT_NAME)
	
main()
