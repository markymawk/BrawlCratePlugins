__author__ = "mawwwk"
__version__ = "1.4"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import * # GenericWrapper, STEXWrapper
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB.ResourceNodes.ProjectPlus import STEXNode
from System.Windows.Forms import ToolStripMenuItem
from System.IO import File
from mawwwkLib import *

## Start enable check functions
# Single PAC enable check: if StageName is not empty && no children exist
# Wrapper: STEXWrapper
def EnableCheckPAC(sender, event_args):
	param = BrawlAPI.SelectedNode
	sender.Enabled = (param is not None and param.StageName is not "" and str(param.SubstageVarianceType) == "None")

# Substage PACs enable check: if parent is a STEX Node
# Wrapper: GenericWrapper
def EnableCheckSubstagePAC(sender, event_args):
	substageNode = BrawlAPI.SelectedNode
	sender.Enabled = (substageNode is not None and isinstance(substageNode.Parent, STEXNode))

# TLST enable check: if TrackList is not empty
# Wrapper: STEXWrapper
def EnableCheckTLST(sender, event_args):
	param = BrawlAPI.SelectedNode
	sender.Enabled = (param is not None and param.TrackList is not "")

# ASL Entry enable check: SelectedNode is an ASLSEntryNode
def EnableCheckASLEntry(sender, event_args):
	entry = BrawlAPI.SelectedNode
	sender.Enabled = (entry is not None and "ASLSEntryNode" in str(type(entry)))

## End enable check functions
## Start loader functions

# Function to open single stage PAC file
def open_stage_pac(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	stagePac_Path = getParentFolderPath(BrawlAPI.RootNode.FilePath) + "\melee\\STG" + selNode.StageName + ".pac"
	
	if File.Exists(stagePac_Path):
		BrawlAPI.OpenFile(stagePac_Path)
	else:
		BrawlAPI.ShowError("STG" + selNode.StageName + ".pac" + " not found.", "Error")

# Function to open substage PAC file
def open_substage_pac(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	stageMelee_Path = getParentFolderPath(BrawlAPI.RootNode.FilePath) + "\melee\\"
	
	# Attempt 1: try combining (stage)_(substage) with an underscore
	stagePac_Path = stageMelee_Path + "STG" + selNode.Parent.StageName + "_" + selNode.Name + ".pac"
	if File.Exists(stagePac_Path):
		BrawlAPI.OpenFile(stagePac_Path)
		return
	
	# Attempt 2: try (stage)(substage) with no underscore (i.e. Smashville substages)
	stagePac_Path = stageMelee_Path + "STG" + selNode.Parent.StageName + selNode.Name + ".pac"
	if File.Exists(stagePac_Path):
		BrawlAPI.OpenFile(stagePac_Path)
		return
		
	# Attempt 3: try just the substage name (DualLoad i.e. Castle Siege)
	stagePac_Path = stageMelee_Path + "STG" + selNode.Name + ".pac"
	if File.Exists(stagePac_Path):
		BrawlAPI.OpenFile(stagePac_Path)
	
	# If no attempts have worked, show error
	else:
		BrawlAPI.ShowError("Substage .pac not found.", "Error")

# Function to open stage TLST file
def open_stage_tlst(sender, event_args):
	PF_FOLDER = str(BrawlAPI.SelectedNode.FilePath).split("stage\stageinfo\\")[0]
	TLST_FILE_PATH = PF_FOLDER + "\sound\\tracklist\\" + BrawlAPI.SelectedNode.TrackList + ".tlst"
	
	BrawlAPI.OpenFile(TLST_FILE_PATH)
	
# Function to open param file
def open_param(sender, event_args):
	STAGE_FOLDER = str(BrawlAPI.RootNode.FilePath).split("\stageslot\\")[0]
	PARAM_FILE_PATH = STAGE_FOLDER + "\stageinfo\\" + BrawlAPI.SelectedNode.Name + ".param"
	
	BrawlAPI.OpenFile(PARAM_FILE_PATH)

## End loader functions
## Start context menu add

# Param > Open stage pac
BrawlAPI.AddContextMenuItem(STEXWrapper, "", "Open associated stage .pac file", EnableCheckPAC, ToolStripMenuItem("Open stage .pac", None, open_stage_pac))

# Param > Open substage pac
BrawlAPI.AddContextMenuItem(GenericWrapper, "", "Open substage .pac file", EnableCheckSubstagePAC, ToolStripMenuItem("Open substage .pac", None, open_substage_pac))

# Param > Open TLST
BrawlAPI.AddContextMenuItem(STEXWrapper, "", "Open associated .tlst file", EnableCheckTLST, ToolStripMenuItem("Open tracklist", None, open_stage_tlst))

# ASL > Open param
BrawlAPI.AddContextMenuItem(GenericWrapper, "", "Open associated .param file", EnableCheckASLEntry, ToolStripMenuItem("Open .param", None, open_param))
