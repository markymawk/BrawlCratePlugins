__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import File

# For use with mu_menumain.pac files

# Store temp files in the BrawlCrate program folder.
# These are deleted at the end of the script.
TEMP_ARC_PATH = AppPath + "\SELCHAR2_EXPORT_temp.pac"

SCRIPT_NAME = "Export as selcharacter2"

# Check to ensure the context menu item is only active if it's info.pac
# Wrapper type: ARCWrapper
def EnableCheckARC(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and "MenuRule" in BrawlAPI.SelectedNode.Name and BrawlAPI.SelectedNode.Parent and "mu_menumain" in BrawlAPI.SelectedNode.Parent.Name)

# Base function to export stocks from info.pac to other appropriate locations
def export_selcharacter2(sender, event_args):
	MENUMAIN_PATH = BrawlAPI.RootNode.FilePath
	
	# Derive build pf path from the open menumain.pac file
	MENU2_FOLDER = str(MENUMAIN_PATH).split("mu_menumain.pac")[0]
	SELCHARACTER2_PATH = MENU2_FOLDER + "\sc_selcharacter2.pac"
	message = "Exporting MenuRule_en as a sc_selcharacter2.pac file inside\n" + MENU2_FOLDER
	message += "\n\nPress OK to continue."
	
	if BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
		# Export MenuRule_en as a temp .pac file
		BrawlAPI.SelectedNode.Export(TEMP_ARC_PATH)
		
		# Open existing selchar2
		BrawlAPI.OpenFile(SELCHARACTER2_PATH)
		
		# Replace existing child node
		BrawlAPI.RootNode.Children[0].Replace(TEMP_ARC_PATH)
		
		BrawlAPI.SaveFile()
		BrawlAPI.OpenFile(MENUMAIN_PATH)

		File.Delete(TEMP_ARC_PATH)

		BrawlAPI.ShowMessage("Export complete!", SCRIPT_NAME)
	
# Add right-click contextual menu options
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export archive as a sc_selcharacter2.pac", EnableCheckARC, ToolStripMenuItem("Export as selcharacter2", None, export_selcharacter2))
