__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import *
from mawwwkLib import *

## Start enable check function
# Wrapper: TLSTWrapper
def EnableCheckTLST(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.HasChildren)

## End enable check function
## Start of main script

def check_for_missing_brstm_filepaths(sender, event_args):
	missingTrackNames = []
	
	# Check tracks
	for track in BrawlAPI.SelectedNode.Children:
		if track.SongID >= 61440:	# 0xF000
			if not File.Exists(str(track.rstmPath)):
				missingTrackNames.append(track.Name)
			
			# If pinch mode, check for track_b.brstm
			if track.SongSwitch and not File.Exists(str(track.rstmPath)[0:-6] + "_b.brstm"):
				missingTrackNames.append("[SONGSWITCH] " + track.Name)
	
	# Results
	if len(missingTrackNames) == 0:
		BrawlAPI.ShowMessage("No missing tracks found!","Success")
	else:
		message = str(len(missingTrackNames)) + " missing track(s) found:\n\n"
		for track in missingTrackNames:
			message += track + "\n"

		BrawlAPI.ShowError(message, "Missing tracks found")

BrawlAPI.AddContextMenuItem(TLSTWrapper, "", "Check all tracklist entries for missing BRSTM file paths", EnableCheckTLST, ToolStripMenuItem("Check for missing track paths", None, check_for_missing_brstm_filepaths))
