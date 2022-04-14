__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import *
from mawwwkLib import *

SCRIPT_NAME = "Match All StgPosition BRRES"
MODELDATA_BRRES_NAME = "Model Data [100]"
TEMP_MODELDATA_PATH = AppPath + "\ModelData100.brres"
## Start enable check function

# Check to ensure that the BRES is a ModelData 100 within a stage pac
# Wrapper: BRESWrapper
def EnableCheckBRES(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.Name == MODELDATA_BRRES_NAME \
	and node.Parent and node.Parent.Name == "2")
	
# Check to ensure that the BRES is a ModelData 100 within a stage pac
# Wrapper: MDL0Wrapper
def EnableCheckMDL0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and node.IsStagePosition and node.Parent \
	and node.Parent.Parent and node.Parent.Parent.Name == MODELDATA_BRRES_NAME \
	and node.Parent.Parent.Parent.Name == "2")

## End enable check function
## Start loader function

# Loader function from BRRES (Model Data 100)
def export_stgposition_brres(sender, event_args):
	main(BrawlAPI.SelectedNode)

def export_stgposition_mdl0(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	
	if selNode.Parent and selNode.Parent.Parent and isinstance(selNode.Parent.Parent,BRRESNode):
		main(selNode.Parent.Parent)
	else:
		BrawlAPI.ShowError("Error exporting parent BRRES", "Error")
	
## End loader function
## Start main function
def main(brresNode):
	# Prompt for filename substring to check for
	stageString = BrawlAPI.UserStringInput("Enter stage substring (e.g. \"_DP\")")
	if stageString == "" or stageString == None:
		return
	
	# Save currently opened file path
	SOURCE_FILE = str(BrawlAPI.RootNode.FilePath)
	
	brresNode.ExportUncompressed(TEMP_MODELDATA_PATH)
	
	# Get list of stage pacs in the same folder as the opened file
	STAGE_MELEE_PATH = str(BrawlAPI.RootNode.FilePath).rsplit("\\", 1)[0]
	STAGE_FILES = Directory.CreateDirectory(STAGE_MELEE_PATH).GetFiles()
	
	# Get hash of selected node, to compare with new nodes
	originalHash = brresNode.MD5Str()
	
	# List of files found with the given substring
	filesFound = []
	# List of modified files
	filesModified = []
	
	# Check each pac file in stage/melee for the given substring
	for file in STAGE_FILES:
		if stageString in file.Name and file.FullName != SOURCE_FILE:
			filesFound.append(file.Name)
			
			# Find Model Data 100 node
			BrawlAPI.OpenFile(file.FullName)
			newBRRES = getChildFromName(getParentArc(), MODELDATA_BRRES_NAME, True)
			
			# If hashes aren't identical, replace the brres and save
			if newBRRES and not originalHash == newBRRES.MD5Str():
				newBRRES.Replace(TEMP_MODELDATA_PATH)
				filesModified.append(file.Name)
				BrawlAPI.SaveFile()
	
	# After checking all files, open the original stage pac again
	BrawlAPI.OpenFile(SOURCE_FILE)
	
	# Delete temp brres file
	File.Delete(TEMP_MODELDATA_PATH)
	
	msg = str(len(filesFound)) + " stage file(s) found with substring \"" + stageString + "\"\n"
	
	# If any files modified, list them
	if len(filesModified):
		msg += str(len(filesModified)) + " file(s) edited:\n\n"
		
		for file in filesModified:
			msg += file + "\n"
		BrawlAPI.ShowMessage(msg, "Success!")
	
	# Otherwise, no mismatches found
	elif len(filesFound):
		BrawlAPI.ShowMessage(msg + "\nNo mismatching " + MODELDATA_BRRES_NAME + " nodes found", "Complete")
## End main function
## Start context menu add

# From parent BRRES
BrawlAPI.AddContextMenuItem(BRESWrapper, "", "Export ModelData 100 BRRES to other stages", EnableCheckBRES, ToolStripMenuItem("Export StgPosition to 1:1 stages", None, export_stgposition_brres))

# From stgPosition MDL0 (export BRRES)
BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Export ModelData 100 BRRES to other stages", EnableCheckMDL0, ToolStripMenuItem("Export StgPosition to 1:1 stages", None, export_stgposition_mdl0))
