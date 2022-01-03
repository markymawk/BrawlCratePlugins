__author__ = "mawwwk"
__version__ = "1.2"

from System.Windows.Forms import ToolStripMenuItem
from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.IO import File
from mawwwkLib import *

# Store temp files in the BrawlCrate program folder.
# These are deleted at the end of the script.
TEMP_STOCKS_PAT0_PATH = AppPath + "\STOCKFACE_PAT0_EXPORT_temp.pat0"

# Name of the pat0 animation that contains frames for each stock icon
STOCKFACE_PAT0_NAME = "InfStockface_TopN__0"
SCRIPT_NAME = "Stock Icon Exporter"

## Start enable check functions

# Check to ensure the context menu item is only active if it's info.pac
def EnableCheckARC(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and BrawlAPI.SelectedNode.Name == "info_en")
	
# Same as above, but from MiscData 30
def EnableCheckBRES(sender, event_args):
	bres = BrawlAPI.SelectedNode
	sender.Enabled = (bres is not None and "[30]" in bres.Name and bres.Parent and "info_en" in bres.Parent.Name)

## End enable check functions
## Start helper functions

# Locate stockface pat0 in brres (temp), and export to a temp pat0 file
def exportStockfacePat0():
	# Find pat0 group inside file
	pat0Group = getChildFromName(BrawlAPI.RootNode, "AnmTexPat")
	
	# Find Stockface pat0 and export to temp file
	stockfacePAT0 = getChildFromName(pat0Group, STOCKFACE_PAT0_NAME)
	stockfacePAT0.Export(TEMP_STOCKS_PAT0_PATH)

# Within the exported StockFaceTex brres, clear everything that isn't a stock icon tex0 or plt0
def purgeAllExceptStocks():
	parentBrres = BrawlAPI.RootNode
	groupsToDelete = []
	
	# Delete any groups other than Textures and Palettes
	for bresGroup in parentBrres.Children:
		if bresGroup.Name not in ["Textures(NW4R)", "Palettes(NW4R)"]:
			groupsToDelete.append(bresGroup)
	
	removeChildNodes(groupsToDelete)
	
	# Only textures and palette groups should remain
	if len(parentBrres.Children) != 2:
		BrawlAPI.ShowError("Unexpected data in info.pac MiscData30 brres", "Error")
		return 0
	
	# Generate lists of tex0 and plt0 nodes that aren't stocks
	unusedTEX0List = []
	unusedPLT0List = []
	tex0Group = getChildFromName(parentBrres, "Textures")
	plt0Group = getChildFromName(parentBrres, "Palettes")
	
	for tex0 in tex0Group.Children:
		if tex0.Name[:7] != "InfStc.":
			unusedTEX0List.append(tex0)
	
	for plt0 in plt0Group.Children:
		if plt0.Name[:7] != "InfStc.":
			unusedPLT0List.append(plt0)
	
	# Delete remaining non-stock nodes
	removeChildNodes(unusedTEX0List)
	removeChildNodes(unusedPLT0List)

# With STGRESULT.pac open, replace the existing Stockface pat0 inside MiscData 110
def importStockfaceIntoSTGRESULTpac():
	# Within Root > ARC 2, find MiscData 110
	MiscData110 = getChildFromName(BrawlAPI.RootNode.Children[1], "Misc Data [110]")
	
	# Within MiscData 110, find pat0 folder
	pat0Folder = getChildFromName(MiscData110, "AnmTexPat")
	
	# Within pat0 folder, find existing stockface pat0
	stockFacePAT0 = getChildFromName(pat0Folder, STOCKFACE_PAT0_NAME)
	
	# Replace existing pat0 animation in STGRESULT with the temp pat0 (from info.pac)
	stockFacePAT0.Replace(TEMP_STOCKS_PAT0_PATH)

# Find MiscData 120 inside STGRESULT.pac, or MiscData90 inside selcharacter.pac, and replace with stocks BRRES
def importBrresIntoPac(pacFilePath, brresFilePath):
	BrawlAPI.OpenFile(pacFilePath)
	
	# STGRESULT.pac > Root > 2 ARC > MiscData120 brres
	if "result" in BrawlAPI.RootNode.Name.lower() and isinstance(BrawlAPI.RootNode, ARCNode):
		node = getChildFromName(BrawlAPI.RootNode.Children[1], "Misc Data [120]")
	
	# sc_selcharacter.pac > Root > MiscData90 brres
	elif "selcharacter" in BrawlAPI.RootNode.Name.lower() and isinstance(BrawlAPI.RootNode, ARCNode):
		node = getChildFromName(BrawlAPI.RootNode, "Misc Data [90]")
	
	node.Replace(brresFilePath)

## End helper functions
## Start loader functions

# Text shown before running the plug-in
INIT_PROMPT_TEXT = "Export stock icon data from this file to STGRESULT.pac, StockFaceTex.brres, and sc_selcharacter.pac.\n\nPress OK to continue."

# Base info.pac RootNode function to isolate the MiscData 30 brres, then call main()
def export_stocks_from_info_arc(sender, event_args):
	if BrawlAPI.ShowOKCancelPrompt(INIT_PROMPT_TEXT, SCRIPT_NAME):
		main(getChildFromName(BrawlAPI.SelectedNode, "Misc Data [30]"))

# Base MiscData30 function, from selectedNode call main()
def export_stocks_from_miscdata30(sender, event_args):
	if BrawlAPI.ShowOKCancelPrompt(INIT_PROMPT_TEXT, SCRIPT_NAME):
		main(BrawlAPI.SelectedNode)

## End loader functions
## Start main function

# Given the MiscData30 node, export/import data to the other files
def main(node):
	INFO_PAC_PATH = BrawlAPI.RootNode.FilePath
	
	# Derive file paths from the open info.pac file
	PF_FOLDER = str(INFO_PAC_PATH).split("\info2\info.pac")[0]
	STOCKFACETEX_BRRES_PATH = PF_FOLDER + "\menu\common\StockFaceTex.brres"
	RESULTS_PAC_PATH = PF_FOLDER + "\stage\melee\STGRESULT.pac"
	SELCHARACTER_PAC_PATH = PF_FOLDER + "\menu2\sc_selcharacter.pac"
	
	node.ExportUncompressed(STOCKFACETEX_BRRES_PATH)
	
	# Close info.pac and open StockFaceTex brres
	BrawlAPI.OpenFile(STOCKFACETEX_BRRES_PATH)
	
	# With StockFaceTex brres open, export stockface pat0 animation as a temp, and clear out any non-stocks data
	exportStockfacePat0()
	purgeAllExceptStocks()
	BrawlAPI.SaveFile()
	
	# Open STGRESULT, and import pat0 and new brres (file 2 of 3)
	importBrresIntoPac(RESULTS_PAC_PATH, STOCKFACETEX_BRRES_PATH)
	importStockfaceIntoSTGRESULTpac()
	BrawlAPI.SaveFile()
	
	# Open selcharacter and import brres (file 3 of 3)
	importBrresIntoPac(SELCHARACTER_PAC_PATH, STOCKFACETEX_BRRES_PATH)
	BrawlAPI.SaveFile()
	
	# Re-open info.pac after all other files are handled
	BrawlAPI.OpenFile(INFO_PAC_PATH)
	
	# Delete temp files
	File.Delete(TEMP_STOCKS_PAT0_PATH)
	
	# Script complete!
	msg = "Stock tex0, plt0, and pat0 successfully exported from info.pac to: \n\n" + \
	STOCKFACETEX_BRRES_PATH + "\n\n" + RESULTS_PAC_PATH + "\n\n" + SELCHARACTER_PAC_PATH
	BrawlAPI.ShowMessage(msg, "Success!")

## End main function
## Start context menu add

CONTEXT_HOVER_TEXT = "Export data to STGRESULT, StockFaceTex, and selcharacter files"

# From parent ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", CONTEXT_HOVER_TEXT, EnableCheckARC, ToolStripMenuItem("Export stock icons", None, export_stocks_from_info_arc))

# From MiscData30 BRRES
BrawlAPI.AddContextMenuItem(BRESWrapper, "", CONTEXT_HOVER_TEXT, EnableCheckBRES, ToolStripMenuItem("Export stock icons", None, export_stocks_from_miscdata30))
