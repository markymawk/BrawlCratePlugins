__author__ = "mawwwk"
__version__ = "2.0"

from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *
from System.IO import File

TEMP_ARC_PATH = AppPath + "\SELCHAR2_EXPORT_temp.pac"
SCRIPT_NAME = "Export as selcharacter2"

## Start enable check functions

# Run from MenuRule ARC - MenuRule in name and parent is named mu_menumain
# Wrapper type: ARCWrapper
def EnableCheckMenuRuleARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None and "MenuRule" in node.Name and node.Parent and "mu_menumain" in node.Parent.Name

# Run from root menumain ARC 
def EnableCheckMenumainARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None and "mu_menumain" in node.Name and node.Children and getChildFromName(node, "MenuRule_")

# Run from selcharacter2 root ARC
def EnableCheckSelchar2RootARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None and "sc_selcharacter2_" in node.Name and node.Children and getChildFromName(node,"MenuRule_")

# Run from selcharacter2 MenuRule ARC
def EnableCheckSelchar2MenuruleARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None and "MenuRule" in node.Name and node.Parent and "sc_selcharacter2_" in node.Parent.Name

## End enable check functions
## Start loader functions

# Loader from MenuRule ARC
def export_menumain_menurule(sender, event_args):
	main_menumain(BrawlAPI.SelectedNode)

# Loader from MenuMain ARC (root node)
def export_menumain_rootnode(sender, event_args):
	
	node = getChildFromName(BrawlAPI.SelectedNode, "MenuRule_")
	
	# Make sure MenuRule node exists, then call main()
	if node and "ARCNode" in node.NodeType:
		main_menumain(node)
		
	# If MenuRule node not found, show an error
	else:
		showMsg("MenuRule ARC not found", "Error")

# Loader from selchar2 (root node)
def export_selchar2_rootnode(sender, event_args):
	node = getChildFromName(BrawlAPI.SelectedNode, "MenuRule_")
	if not node or "ARCNode" not in node.NodeType:
		BrawlAPI.ShowMessage("MenuRule ARC not found", "Error")
	
	main_selchar2(node)

def export_selchar2_MenuRule(sender, event_args):
	main_selchar2(BrawlAPI.SelectedNode)
## End loader functions
## Start main function

# Main function to handle selcharacter2.pac
def main_menumain(node):

	# Derive build pf path from the open menumain.pac file
	MENUMAIN_PATH = BrawlAPI.RootNode.FilePath
	MENU2_FOLDER = str(MENUMAIN_PATH).split("mu_menumain.pac")[0]
	SELCHARACTER2_PATH = MENU2_FOLDER + "\sc_selcharacter2.pac"
	message = "Exporting MenuRule_en as a sc_selcharacter2.pac file inside\n" + MENU2_FOLDER
	message += "\n\nPress OK to continue."
	
	# Show prompt
	if not BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
		return
	
	# Export MenuRule_en as a temp .pac file
	node.Export(TEMP_ARC_PATH)
	
	# Open existing selcharacter2 file
	BrawlAPI.OpenFile(SELCHARACTER2_PATH)
	
	# Replace existing child node
	BrawlAPI.RootNode.Children[0].Replace(TEMP_ARC_PATH)
	BrawlAPI.SaveFile()
	
	# Re-open menumain
	BrawlAPI.OpenFile(MENUMAIN_PATH)
	
	# Delete temp file
	File.Delete(TEMP_ARC_PATH)
	
	# Results
	BrawlAPI.ShowMessage("Export complete!", SCRIPT_NAME)

def main_selchar2(node):
	SELCHAR2_PATH = BrawlAPI.RootNode.FilePath
	MENU2_FOLDER = str(SELCHAR2_PATH).split("sc_selcharacter2.pac")[0]
	MENUMAIN_PATH = MENU2_FOLDER + "\mu_menumain.pac"
	
	message = "Exporting MenuRule_en into the mu_menumain.pac file\n" + MENU2_FOLDER
	message += "\n\nPress OK to continue."
	
	# Show prompt
	if not BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
		return
	
	# Export MenuRule_en as a temp .pac file
	node.Export(TEMP_ARC_PATH)
	
	# Open menumain
	BrawlAPI.OpenFile(MENUMAIN_PATH)
	
	# Replace existing child node
	menuRuleNode = getChildFromName(BrawlAPI.RootNode, "MenuRule")
	menuRuleNode.Replace(TEMP_ARC_PATH)
	BrawlAPI.SaveFile()
	
	# Re-open selchar2
	BrawlAPI.OpenFile(SELCHAR2_PATH)
	
	# Delete temp file
	File.Delete(TEMP_ARC_PATH)
	
	# Results
	BrawlAPI.ShowMessage("Export complete!", SCRIPT_NAME)

## End main function
## Start context menu add

# From menumain > MenuRule ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export MenuRule ARC as a sc_selcharacter2.pac", EnableCheckMenuRuleARC, ToolStripMenuItem("Export as selcharacter2", None, export_menumain_menurule))

# From menumain (root node) ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export MenuRule ARC as a sc_selcharacter2.pac", EnableCheckMenumainARC, ToolStripMenuItem("Export MenuRule as selcharacter2", None, export_menumain_rootnode))

# From selchar2 (root node) ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export selcharacter2 file to MenuRule ARC in menumain .pac", EnableCheckSelchar2RootARC, ToolStripMenuItem("Export into menumain", None, export_selchar2_rootnode))

# From selchar2 > MenuRule ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export selcharacter2 file to MenuRule ARC in menumain .pac", EnableCheckSelchar2MenuruleARC, ToolStripMenuItem("Export into menumain", None, export_selchar2_MenuRule))
