__author__ = "mawwwk"
__version__ = "2.1"

from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *
from System.IO import File

TEMP_ARC_PATH = AppPath + "\MenuRule_temp.pac"
SCRIPT_NAME = "Export MenuRule ARC"

## Start enable check functions

# Run from menumain MenuRule ARC
# Wrapper type: ARCWrapper
def EnableCheck_menumain_RuleARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and "MenuRule" in node.Name and node.Parent and "mu_menumain" in node.Parent.Name

# Run from menumain root ARC 
def EnableCheck_menumain_RootARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and "mu_menumain" in node.Name and node.Children and findChildByName(node, "MenuRule_")

# Run from selcharacter2 MenuRule ARC
def EnableCheck_selchar2_RuleARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and "MenuRule" in node.Name and node.Parent and "sc_selcharacter2_" in node.Parent.Name
	
# Run from selcharacter2 root ARC
def EnableCheck_selchar2_rootARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and "sc_selcharacter2_" in node.Name and node.Children and findChildByName(node,"MenuRule_")

## End enable check functions
## Start loader functions

# Loader from MenuRule ARC
def export_menumain_menurule(sender, event_args):
	main_menumain(BrawlAPI.SelectedNode)

# Loader from MenuMain ARC (root node)
def export_menumain_rootnode(sender, event_args):
	menuRuleNode = findChildByName(BrawlAPI.SelectedNode, "MenuRule_")
	if menuRuleNode and isinstance(menuRuleNode, ARCNode):
		main_menumain(node)
	else:
		BrawlAPI.ShowMessage("MenuRule ARC not found", "Error")

# Loader from selchar2 (root node)
def export_selchar2_rootnode(sender, event_args):
	menuRuleNode = findChildByName(BrawlAPI.SelectedNode, "MenuRule_")
	if menuRuleNode and isinstance(menuRuleNode, ARCNode):
		main_selchar2(menuRuleNode)
	else:
		BrawlAPI.ShowMessage("MenuRule ARC not found", "Error")

def export_selchar2_MenuRule(sender, event_args):
	main_selchar2(BrawlAPI.SelectedNode)

## End loader functions
## Start main function

# Main function to handle selcharacter2.pac
def main_menumain(node):

	# Derive build pf path from the open menumain.pac file
	menumain_path = BrawlAPI.RootNode.FilePath
	menu2_path = getParentFolderPath(menumain_path)
	selcharacter2_path = menu2_path + "\sc_selcharacter2.pac"
	
	START_MSG = "Exporting MenuRule_en as a sc_selcharacter2.pac file inside\n" + menu2_path
	START_MSG += "\n\nPress OK to continue."
	
	# Show prompt
	if not BrawlAPI.ShowOKCancelPrompt(START_MSG, SCRIPT_NAME):
		return
	
	# Export MenuRule_en as a temp .pac file
	node.Export(TEMP_ARC_PATH)
	
	# Replace node in selchar2
	BrawlAPI.OpenFile(selcharacter2_path)
	BrawlAPI.RootNode.Children[0].Replace(TEMP_ARC_PATH)
	BrawlAPI.SaveFile()
	
	# Re-open menumain
	BrawlAPI.OpenFile(menumain_path)
	
	# Delete temp file
	File.Delete(TEMP_ARC_PATH)
	
	# Results
	BrawlAPI.ShowMessage("Export complete!", SCRIPT_NAME)

def main_selchar2(node):
	selcharacter2_path = BrawlAPI.RootNode.FilePath
	menu2_path = getParentFolderPath(selcharacter2_path)
	menumain_path = menu2_path + "\mu_menumain.pac"
	
	START_MSG = "Exporting MenuRule_en into the mu_menumain.pac file inside\n" + menu2_path
	START_MSG += "\n\nPress OK to continue."
	
	# Show prompt
	if not BrawlAPI.ShowOKCancelPrompt(START_MSG, SCRIPT_NAME):
		return
	
	# Export MenuRule_en as a temp .pac file
	node.Export(TEMP_ARC_PATH)
	
	# Replace node in menumain
	BrawlAPI.OpenFile(menumain_path)
	menuRuleNode = findChildByName(BrawlAPI.RootNode, "MenuRule")
	menuRuleNode.Replace(TEMP_ARC_PATH)
	BrawlAPI.SaveFile()
	
	# Re-open selchar2
	BrawlAPI.OpenFile(selcharacter2_path)
	
	# Delete temp file
	File.Delete(TEMP_ARC_PATH)
	
	# Results
	BrawlAPI.ShowMessage("Export complete!", SCRIPT_NAME)

## End main function
## Start context menu add

# From menumain > MenuRule ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export MenuRule ARC as a sc_selcharacter2.pac", EnableCheck_menumain_RuleARC, ToolStripMenuItem("Export MenuRule as selcharacter2", None, export_menumain_menurule))

# From menumain (root node) ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export MenuRule ARC as a sc_selcharacter2.pac", EnableCheck_menumain_RootARC, ToolStripMenuItem("Export MenuRule as selcharacter2", None, export_menumain_rootnode))

# From selchar2 (root node) ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export selcharacter2 file to MenuRule ARC in menumain.pac", EnableCheck_selchar2_rootARC, ToolStripMenuItem("Export MenuRule into menumain", None, export_selchar2_rootnode))

# From selchar2 > MenuRule ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export selcharacter2 file to MenuRule ARC in menumain.pac", EnableCheck_selchar2_RuleARC, ToolStripMenuItem("Export MenuRule into menumain", None, export_selchar2_MenuRule))
