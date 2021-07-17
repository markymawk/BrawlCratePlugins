__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import *
from mawwwkLib import *

TEMP_MDL0_PATH = AppPath + "\MDL0_EXPORT_temp.mdl0"

## Start enable check function
# Check that mdl0 and file path contain "Fit" and ".pac"
# Wrapper: MDL0Wrapper
def EnableCheckMDL0(sender, event_args):
	node = BrawlAPI.SelectedNode
	
	sender.Enabled = (node is not None \
	and "Fit" in node.Name \
	and "Fit" in BrawlAPI.RootNode.FilePath \
	and BrawlAPI.RootNode.FilePath.endswith(".pac"))

## End enable check function
## Start helper functions

def isFighterPac(filename):
	if "Fit" in filename and filename.endswith(".pac"):
		return True
	
	return False

# Given filepath, return the parent directory
def getParentDir(filepath):
	return filepath[:filepath.rindex('\\')+1]

## End helper functions
## Start loader functions

def copy_fighter_model(sender, event_args):
	SELECTED_MDL0_NAME = BrawlAPI.SelectedNode.Name
	PARENT_BRRES_INDEX = BrawlAPI.SelectedNode.Parent.Parent.AbsoluteIndex
	PARENT_BRRES_NAME = BrawlAPI.SelectedNode.Parent.Parent.Name
	CURRENT_OPEN_FILE = getOpenFile()
	
	# Get parent folder name
	PARENT_DIR_PATH = getParentDir(BrawlAPI.RootNode.FilePath)
	
	# Export temp mdl0
	BrawlAPI.SelectedNode.Export(TEMP_MDL0_PATH)
	
	filesEdited = []
	
	# Loop through files in parent directory
	for file in Directory.CreateDirectory(PARENT_DIR_PATH).GetFiles():
	
		# Open file, unless it's the base file
		if isFighterPac(file.Name) and file.FullName != CURRENT_OPEN_FILE:
			BrawlAPI.OpenFile(file.FullName)
			root = BrawlAPI.RootNode
			
			# If model exists in the same spot
			if root.HasChildren \
			and len(root.Children) >= PARENT_BRRES_INDEX+1 \
			and isinstance(root.Children[PARENT_BRRES_INDEX], BRRESNode) \
			and root.Children[PARENT_BRRES_INDEX].Name == PARENT_BRRES_NAME:
			
				# and if model name matches
				thisModel = root.Children[PARENT_BRRES_INDEX].Children[0].Children[0]
				if thisModel.Name == SELECTED_MDL0_NAME:
				
					# Replace with base mdl0
					thisModel.Replace(TEMP_MDL0_PATH)
					BrawlAPI.SaveFile()
					filesEdited.append(file.Name)
	
	# Delete temp mdl0
	File.Delete(TEMP_MDL0_PATH)
	
	# Reopen previously-opened file
	BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
			
	# Results
	
	# If no files edited, show help/error
	if len(filesUpdated) == 0:
		BrawlAPI.ShowError("No files updated.\n\n(If this is unexpected, verify the MDL0 names and locations are identical among files you want to update.)")
	# If any files are modified, list changed file names
	else:
		msg = str(len(filesUpdated)) + " files updated!\n\n"
		for i in filesEdited:
			msg += i + "\n"
		
		BrawlAPI.ShowMessage(msg, "Success!")
## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Copy the MDL0 to other fighter files in this folder", EnableCheckMDL0, ToolStripMenuItem("Copy fighter model", None, copy_fighter_model))
