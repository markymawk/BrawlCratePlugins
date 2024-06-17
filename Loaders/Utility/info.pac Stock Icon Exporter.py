__author__ = "mawwwk"
__version__ = "1.2"

from System.Windows.Forms import ToolStripMenuItem
from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.IO import File
from mawwwkLib import *

STOCKS_PAT0_PATH = AppPath + "\STOCKFACE_PAT0_temp.pat0"

# Name of the pat0 animation that contains frames for each stock icon
STOCKFACE_PAT0_NAME = "InfStockface_TopN__0"
SCRIPT_NAME = "info.pac Stock Icon Exporter"

## Start enable check functions

# Check to ensure the context menu item is only active if it's info.pac
def EnableCheckARC(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.Name == "info_en")
	
# Same as above, but from MiscData 30
def EnableCheckBRES(sender, event_args):
	brres = BrawlAPI.SelectedNode
	sender.Enabled = (brres and "[30]" in brres.Name and brres.Parent and "info_en" in brres.Parent.Name)

## End enable check functions
## Start helper functions

# Within the exported StockFaceTex brres, clear everything that isn't a stock icon tex0 or plt0
def purgeAllExceptStocks(parentBRRES):
	groupsToDelete = []
	
	# Delete any groups other than Textures and Palettes
	for bresGroup in parentBRRES.Children:
		if bresGroup.Name not in ["Textures(NW4R)", "Palettes(NW4R)"]:
			groupsToDelete.append(bresGroup)
	
	removeChildNodes(groupsToDelete)
	
	# Only textures and palette groups should remain
	if len(parentBRRES.Children) != 2:
		BrawlAPI.ShowError("Unexpected data in info.pac MiscData30 brres", "Error")
		return 0
	
	# Generate lists of tex0 and plt0 nodes that aren't stocks
	unusedTEX0List = []
	unusedPLT0List = []
	tex0Group = parentBRRES.FindChild(TEX_GROUP)
	plt0Group = parentBRRES.FindChild(PLT_GROUP)
	
	for tex0 in tex0Group.Children:
		if not tex0.Name.startswith("InfStc."):
			unusedTEX0List.append(tex0)
	
	for plt0 in plt0Group.Children:
		if not plt0.Name.startswith("InfStc."):
			unusedPLT0List.append(plt0)
	
	# Delete remaining non-stock nodes
	removeChildNodes(unusedTEX0List)
	removeChildNodes(unusedPLT0List)

## End helper functions
## Start loader functions

START_MSG = "Export stock icon data from this file to STGRESULT.pac, StockFaceTex.brres, and sc_selcharacter.pac.\n\nPress OK to continue."

# Base info.pac RootNode function to isolate the MiscData 30 brres, then call main()
def export_stocks_from_info_arc(sender, event_args):
	if BrawlAPI.ShowOKCancelPrompt(START_MSG, SCRIPT_NAME):
		main(BrawlAPI.SelectedNode.FindChild("Misc Data [30]"))

# Base MiscData30 function, from selectedNode call main()
def export_stocks_from_miscdata30(sender, event_args):
	if BrawlAPI.ShowOKCancelPrompt(START_MSG, SCRIPT_NAME):
		main(BrawlAPI.SelectedNode)

## End loader functions
## Start main function

# Given the MiscData30 node, export/import data to the other files
def main(node):
	infoPac_Path = BrawlAPI.RootNode.FilePath
	
	# Derive file paths from the open info.pac file
	pf_Dir = str(infoPac_Path).split("\info2\info.pac")[0]
	stockFaceTex_Path = pf_Dir + "\menu\common\StockFaceTex.brres"
	results_Path = pf_Dir + "\stage\melee\STGRESULT.pac"
	selcharacter_Path = pf_Dir + "\menu2\sc_selcharacter.pac"
	
	node.ExportUncompressed(stockFaceTex_Path)
	
	# Close info.pac and open StockFaceTex brres
	BrawlAPI.OpenFile(stockFaceTex_Path)
	
	# Find pat0 group inside file
	pat0Group = BrawlAPI.RootNode.FindChild(PAT_GROUP)
	
	# Find Stockface pat0 and export to temp file
	stockfacePAT0 = pat0Group.FindChild(STOCKFACE_PAT0_NAME)
	stockfacePAT0.Export(STOCKS_PAT0_PATH)
	
	purgeAllExceptStocks(BrawlAPI.RootNode)
	BrawlAPI.SaveFile()
	
	# Open STGRESULT, and import pat0 and new brres (file 2 of 3)
	BrawlAPI.OpenFile(results_Path)
	brres = BrawlAPI.RootNode.Children[1].FindChild("Misc Data [120]")
	brres.Replace(stockFaceTex_Path)
	
	brres = BrawlAPI.RootNode.Children[1].FindChild("Misc Data [110]")
	pat0 = brres.FindChild(PAT_GROUP).FindChild(STOCKFACE_PAT0_NAME)
	pat0.Replace(STOCKS_PAT0_PATH)
	BrawlAPI.SaveFile()
	
	# Open selcharacter and import brres (file 3 of 3)
	BrawlAPI.OpenFile(selcharacter_Path)
	brres = BrawlAPI.RootNode.FindChild("Misc Data [90]")
	brres.Replace(stockFaceTex_Path)
	BrawlAPI.SaveFile()
	
	# Re-open info.pac after all other files are handled
	BrawlAPI.OpenFile(infoPac_Path)
	
	# Delete temp files
	File.Delete(STOCKS_PAT0_PATH)
	
	# Results
	msg = "Stock tex0, plt0, and pat0 successfully exported from info.pac to: \n\n"
	msg += stockFaceTex_Path + "\n\n" + results_Path + "\n\n" + selcharacter_Path
	BrawlAPI.ShowMessage(msg, "Success!")

## End main function
## Start context menu add

CONTEXT_HOVER_TEXT = "Export data to STGRESULT, StockFaceTex, and selcharacter files"

# From parent ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", CONTEXT_HOVER_TEXT, EnableCheckARC, ToolStripMenuItem("Export stock icons", None, export_stocks_from_info_arc))

# From MiscData30 BRRES
BrawlAPI.AddContextMenuItem(BRESWrapper, "", CONTEXT_HOVER_TEXT, EnableCheckBRES, ToolStripMenuItem("Export stock icons", None, export_stocks_from_miscdata30))
