__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from BrawlCrate.NodeWrappers import * 
from BrawlCrate.UI import MainForm
from System.Windows.Forms import ToolStripMenuItem
from BrawlLib.Internal import *
from mawwwkLib import *

SCRIPT_NAME = "Import BRSTMs into Tracklist"
BRSTM_FILTER = "BRSTM files (*.brstm)|*.brstm"

## Start enable check functions

# Check to ensure that the selected node is a tracklist node
# Wrapper: TLSTWrapper
def EnableCheck(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None

## End enable check functions
## Start helper functions

def getUsedSongIDs(parentNode):
	IDs = []
	
	for track in parentNode.Children:
		if track.SongID >= 61440: #0xF000 
			IDs.append(track.SongID)
	
	return IDs

## End helper functions
## Start loader functions

def add_brstms_to_tracklist(sender, event_args):
	ROOT_NODE = BrawlAPI.SelectedNode
	
	# Store song IDs of all tracks currently in the tracklist
	usedSongIDs = getUsedSongIDs(ROOT_NODE)
	
	currentSongID = 61440 	# Starts at 0xF000, stores the lowest-used SongID
	
	# Prompt for brstms to add
	BRSTM_FILES_LIST = BrawlAPI.OpenMultiFileDialog(SCRIPT_NAME, BRSTM_FILTER)
	
	if not BRSTM_FILES_LIST:
		return # User quit
	
	# If brstms are inside strm directory, use normal path derivation
	isInsideStrmDir = "\strm\\" in BRSTM_FILES_LIST[0]
	
	# If brstms exist outside of the strm dir, prompt for a custom prefix such as ../../
	if not isInsideStrmDir:
	
		if BrawlAPI.ShowOKCancelPrompt("strm directory not found in filepath.\n\nEnter a custom prefix relative to the strm folder.","strm directory not found"):
		
			filePathPrefix = BrawlAPI.UserStringInput("Enter filepath prefix (e.g. \"../../\")")
			
			if not filePathPrefix:
				return # User quit
		
		else:
			return # User quit
	
	# Add tracklist entries
	for file in BRSTM_FILES_LIST:
	
		# Use uniform slash formatting
		file = file.replace("\\", "/")
		
		# Create new tlst entry
		track = TLSTEntryNode()
		ROOT_NODE.AddChild(track)
		
		# Set name based on brstm name
		track.Name = file.rsplit("/",1)[1].rsplit(".brstm",1)[0]
		
		# Set volume and frequency to default values
		track.Volume = 80
		track.Frequency = 40
		
		# Derive an unused SongID value, and then set it
		while currentSongID in usedSongIDs:
			currentSongID += 1
		
		track.SongID = currentSongID
		usedSongIDs.append(currentSongID)
		
		# If "strm" exists in the filepath, base SongFileName off of that
		if isInsideStrmDir:
			track.SongFileName = file.rsplit("strm/")[1].rsplit(".brstm",1)[0]
		
		# If "strm" isn't in filepath, add user-defined prefix to the beginning (i.e. "../../")
		else:
			track.SongFileName = filePathPrefix + file.rsplit("/",1)[1].rsplit(".brstm",1)[0]

## End loader functions
## Start context menu add

# From parent tracklist node
BrawlAPI.AddContextMenuItem(TLSTWrapper, "", "Generate tracklist entries directly from BRSTMs", EnableCheck, ToolStripMenuItem("Add BRSTMs to tracklist...", None, add_brstms_to_tracklist))