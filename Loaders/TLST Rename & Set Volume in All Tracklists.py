__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Rename in All Tracklists"

## Start enable check functions
# Wrapper: GenericWrapper
def EnableCheckTLSTEntryNode(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and isinstance(node, TLSTEntryNode) and node.Parent and str(node.SongFileName) != "None")

## End enable check functions
## Start helper functions

def getParentFolderPath(filepath):
	path = filepath.rsplit("\\",1)[0] + "\\"
	return path

## End helper functions
## Start loader functions

def rename_in_all_tracklists(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	tracklistsUsedSameName = []
	tracklistsUsedDiffName = []
	originalTrackPath = str(selNode.SongFileName).lower()
	
	# Derive tracklist directory path from selected TLST Entry Node
	tracklistDirPath = getParentFolderPath(selNode.Parent.FilePath)
	
	# Prompt for new track name
	newTrackName = BrawlAPI.UserStringInput("Enter new track name", selNode.Name)
	if newTrackName == "":
		return
	
	# If tracklist folder isn't already open from a previous use, open it. Otherwise, prompt to continue within opened folder
	if BrawlAPI.RootNode.FilePath != tracklistDirPath or not (BrawlAPI.ShowYesNoPrompt("Use currently opened tracklist folder?", SCRIPT_NAME)):
		BrawlAPI.OpenFile(tracklistDirPath)
	
	# Loop through all track nodes in opened tracklist folder
	for track in BrawlAPI.NodeListOfType[TLSTEntryNode]():
		
		# If tracklist is Credits or Results, ignore song titles
		if track.Parent.Name in ["Credits", "Results"]:
			continue
		
		# If file path matches the original track's, check the name
		if str(track.SongFileName).lower() != "none" and track.SongFileName.lower() == originalTrackPath:
			tracklistFileName = track.Parent.Name + ".tlst"
			
			# If name is the same, add tracklist to tracklistsUsedSameName[]
			if track.Name == newTrackName:
				tracklistsUsedSameName.append(tracklistFileName)
			
			# If track name is different, add to tracklistsUsedDiffName[], and rename track node
			else:
				track.Name = newTrackName
				tracklistsUsedDiffName.append(tracklistFileName)
	
	# Results
	
	# If no other uses (total track uses == 1)
	if len(tracklistsUsedSameName + tracklistsUsedDiffName) == 1:
		msg = "No other track uses found"
	else:
		msg = ""
		
		# List tracklists that already used the entered name
		if len(tracklistsUsedSameName):
			msg += str(len(tracklistsUsedSameName)) + " tracklist(s) already use this song as named:\n" + listToString(tracklistsUsedSameName) + "\n\n"
		
		# List tracks that were renamed
		if len(tracklistsUsedDiffName):
			msg += str(len(tracklistsUsedDiffName)) + " track(s) have been renamed in:\n" + listToString(tracklistsUsedDiffName) + "\n\n"
		
		msg = msg[:-1] # Cut off a line break
	
	showMsg(msg, SCRIPT_NAME)

def match_volume_in_all_tracklists(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	tracklistsUsedSameVolume = []
	tracklistsUsedDiffVolume = []
	originalTrackPath = str(selNode.SongFileName).lower()
	
	# Derive tracklist directory path from selected TLST Entry Node
	tracklistDirPath = getParentFolderPath(selNode.Parent.FilePath)
	
	# Prompt for new track volume
	newVolume = BrawlAPI.UserStringInput("Set track volume", str(selNode.Volume))
	if newVolume == "":
		return
	newVolume = int(newVolume)
	
	# If tracklist folder isn't already open from a previous use, open it. Otherwise, prompt to continue within opened folder
	if BrawlAPI.RootNode.FilePath != tracklistDirPath or not (BrawlAPI.ShowYesNoPrompt("Use currently opened tracklist folder?", SCRIPT_NAME)):
		BrawlAPI.OpenFile(tracklistDirPath)
	
	# Loop through all track nodes in opened tracklist folder
	for track in BrawlAPI.NodeListOfType[TLSTEntryNode]():
	
		# If file path matches the original track's, check the name
		if str(track.SongFileName).lower() != "none" and track.SongFileName.lower() == originalTrackPath:
			tracklistFileName = track.Parent.Name + ".tlst"
			
			# If name is the same, add tracklist to tracklistsUsedSameVolume[]
			if track.Volume == newVolume:
				tracklistsUsedSameVolume.append(tracklistFileName)
			
			# If track name is different, add to tracklistsUsedDiffVolume[], and rename track node
			else:
				track.Volume = newVolume
				tracklistsUsedDiffVolume.append(tracklistFileName)
	
	# Results
	
	# If no other uses (total track uses == 1)
	if len(tracklistsUsedSameVolume + tracklistsUsedDiffVolume) == 1:
		msg = "No other track uses found"
	else:
		msg = ""
		
		# List tracklists that already used the set volume
		if len(tracklistsUsedSameVolume):
			msg += str(len(tracklistsUsedSameVolume)) + " entries already use this volume:\n" + listToString(tracklistsUsedSameVolume) + "\n\n"
		
		# List tracks that were renamed
		if len(tracklistsUsedDiffVolume):
			msg += str(len(tracklistsUsedDiffVolume)) + " track(s) volume have been set in:\n" + listToString(tracklistsUsedDiffVolume) + "\n\n"
		
		msg = msg[:-1] # Cut off a line break
	
	showMsg(msg, SCRIPT_NAME)

## End loader functions
## Start context menu add

# Wrapper: GenericWrapper (no TLSTEntryNodeWrapper)
# Rename across all tracklists
BrawlAPI.AddContextMenuItem(GenericWrapper, "", "Rename all occurrences of this song in every TLST file", EnableCheckTLSTEntryNode, ToolStripMenuItem("Rename across all tracklists", None, rename_in_all_tracklists))

# Wrapper: GenericWrapper (no TLSTEntryNodeWrapper)
# Set volume across all tracklists
BrawlAPI.AddContextMenuItem(GenericWrapper, "", "Match volume of all occurrences of this song in every TLST file", EnableCheckTLSTEntryNode, ToolStripMenuItem("Match volume across all tracklists", None, match_volume_in_all_tracklists))
