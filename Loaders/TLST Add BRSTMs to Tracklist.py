__author__ = "mawwwk"
__version__ = "1.0.3"

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
## Start loader functions

def add_brstms_to_tracklist(sender, event_args):
	tlstNode = BrawlAPI.SelectedNode
	
	# Store song IDs of all tracks currently in the tracklist
	usedSongIDs = []
	for track in tlstNode.Children:
		if track.SongID >= 0xF000:
			usedSongIDs.append(track.SongID)
	
	currentSongID = 0xF000 	# Starts at 0xF000, stores the lowest-used SongID
	if "Menu" in tlstNode.Name:
		currentSongID += 0x40
	
	# Prompt for brstms to add
	brstmFilesList = BrawlAPI.OpenMultiFileDialog(SCRIPT_NAME, BRSTM_FILTER)
	
	if not brstmFilesList:
		return
	
	# If brstms are inside strm directory, use normal path derivation
	isInsideStrmDir = "\strm\\" in brstmFilesList[0]
	
	# If brstms exist outside of the strm dir, prompt for a custom prefix such as ../../
	if not isInsideStrmDir:
		message = "strm directory not found in filepath.\n\nEnter a custom prefix relative to the strm folder."
		if not BrawlAPI.ShowOKCancelPrompt(message, "strm directory not found"):
			return
		
		filePathPrefix = BrawlAPI.UserStringInput("Enter filepath prefix (e.g. \"../../\")")
			
		if not filePathPrefix:
			return
	
	# Add tracklist entries
	for filePath in brstmFilesList:
	
		# Use uniform slash formatting
		filePath = filePath.replace("\\", "/")
		
		# Create new tlst entry
		track = TLSTEntryNode()
		tlstNode.AddChild(track)
		
		# Set name based on brstm name
		track.Name = filePath.rsplit("/",1)[1].rsplit(".brstm",1)[0]
		
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
			filePathPrefix = ""
			fileName = filePath.rsplit("strm/")[1]
		
		# If "strm" isn't in filepath, add user-defined prefix to the beginning (i.e. "../../")
		else:
			fileName = filePath.rsplit("/",1)[1]
		
		# Remove extension
		fileName = fileName.rsplit(".brstm",1)[0]
		fileName = filePathPrefix + fileName
		track.SongFileName = fileName

## End loader functions
## Start context menu add

# From parent tracklist node
BrawlAPI.AddContextMenuItem(TLSTWrapper, "", "Generate tracklist entries directly from BRSTMs", EnableCheck, ToolStripMenuItem("Add BRSTMs to tracklist...", None, add_brstms_to_tracklist))