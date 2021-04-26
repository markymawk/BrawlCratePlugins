__author__ = "mawwwk"
__version__ = "1.1"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import GenericWrapper
from BrawlCrate.NodeWrappers import STEXWrapper
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import STEXNode
from System.Windows.Forms import ToolStripMenuItem
from System.IO import File

# Single PAC enable check: if StageName is not empty && no children exist
# Wrapper: STEXWrapper
def EnableCheckPAC(sender, event_args):
	param = BrawlAPI.RootNode
	sender.Enabled = (param is not None and param.StageName is not "" and str(param.SubstageVarianceType) == "None")

# Substage PACs enable check: if parent is a STEX Node
# Wrapper: GenericWrapper
def EnableCheckSubstagePAC(sender, event_args):
	substageNode = BrawlAPI.SelectedNode
	sender.Enabled = (substageNode is not None and isinstance(substageNode.Parent, STEXNode))

# TLST enable check: if TrackList is not empty
# Wrapper: STEXWrapper
def EnableCheckTLST(sender, event_args):
	param = BrawlAPI.RootNode
	sender.Enabled = (param is not None and param.TrackList is not "")

# Function to open single stage PAC file
def open_stage_pac(sender, event_args):
	PAC_FILE_PATH = str(BrawlAPI.RootNode.FilePath).split("\stageinfo\\")[0] + "\melee\\STG" + BrawlAPI.RootNode.StageName + ".pac"
	
	if File.Exists(PAC_FILE_PATH):
		BrawlAPI.OpenFile(PAC_FILE_PATH)
	else:
		BrawlAPI.ShowError("STG" + BrawlAPI.RootNode.StageName + ".pac" + " not found.", "Error")

# Function to open substage PAC file
def open_substage_pac(sender, event_args):
	STAGE_MELEE_DIR_PATH = str(BrawlAPI.RootNode.FilePath).split("\stageinfo\\")[0] + "\melee\\"
	
	# First, try combining (stage)_(substage) with an underscore
	PAC_FILE_PATH = STAGE_MELEE_DIR_PATH + "STG" + BrawlAPI.RootNode.StageName + "_" + BrawlAPI.SelectedNode.Name + ".pac"
	
	if File.Exists(PAC_FILE_PATH):
		BrawlAPI.OpenFile(PAC_FILE_PATH)
	else:
	# As a backup, try (stage)(substage) with no underscore (i.e. Smashville substages)
		PAC_FILE_PATH = STAGE_MELEE_DIR_PATH + "STG" + BrawlAPI.RootNode.StageName + BrawlAPI.SelectedNode.Name + ".pac"
		
		if File.Exists(PAC_FILE_PATH):
			BrawlAPI.OpenFile(PAC_FILE_PATH)
		else:
	# As another backup, try just the substage name (DualLoad i.e. Castle Siege)
			PAC_FILE_PATH = STAGE_MELEE_DIR_PATH + "STG" + BrawlAPI.SelectedNode.Name + ".pac"
			
			if File.Exists(PAC_FILE_PATH):
				BrawlAPI.OpenFile(PAC_FILE_PATH)
			else:
				BrawlAPI.ShowError("Substage .pac not found.", "Error")

# Function to open stage TLST file
def open_stage_tlst(sender, event_args):
	PF_FOLDER = str(BrawlAPI.RootNode.FilePath).split("stage\stageinfo\\")[0]
	TLST_FILE_PATH = PF_FOLDER + "\sound\\tracklist\\" + BrawlAPI.RootNode.TrackList + ".tlst"
	
	BrawlAPI.OpenFile(TLST_FILE_PATH)
	
# Add right-click contextual menu options
BrawlAPI.AddContextMenuItem(STEXWrapper, "", "Open associated stage .pac file", EnableCheckPAC, ToolStripMenuItem("Open stage .pac", None, open_stage_pac))
BrawlAPI.AddContextMenuItem(GenericWrapper, "", "Open substage .pac file", EnableCheckSubstagePAC, ToolStripMenuItem("Open substage .pac", None, open_substage_pac))
BrawlAPI.AddContextMenuItem(STEXWrapper, "", "Open associated .tlst file", EnableCheckTLST, ToolStripMenuItem("Open tracklist", None, open_stage_tlst))