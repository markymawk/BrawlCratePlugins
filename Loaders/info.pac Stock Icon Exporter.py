__author__ = "mawwwk"
__version__ = "1.0.2"

from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import ARCWrapper
from BrawlCrate.NodeWrappers import BRESWrapper
from BrawlCrate.NodeWrappers import FolderWrapper
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import File
from mawwwkLib import *

# Store temp files in the BrawlCrate program folder.
# These are deleted at the end of the script.
TEMP_STOCKS_PAT0_PATH = AppPath + "\STOCKFACE_PAT0_EXPORT_temp.pat0"

# Name of the pat0 animation that contains frames for each stock icon
STOCKFACE_PAT0_NAME = "InfStockface_TopN__0"
SCRIPT_NAME = "Stock Icon Exporter"
STOCKFACETEX_BRRES_PATH = ""

# Text shown before running the plug-in
INIT_PROMPT_TEXT = "Export stock icon data from this file to STGRESULT.pac, StockFaceTex.brres, and sc_selcharacter.pac.\n\nPress OK to continue."

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

# Locate stockface pat0 in temp brres, and export to a temp pat0 file
def exportStockfacePat0():
	# Determine pat0 folder within selected brres
	for childFolder in BrawlAPI.RootNode.Children:
		if "AnmTexPat(NW4R)" in childFolder.Name:
			pat0List = childFolder.Children
			break
	# Find Stockface pat0 and export to temp file
	for pat0 in BrawlAPI.NodeListOfType[PAT0Node]():
		if STOCKFACE_PAT0_NAME in pat0.Name:
			pat0.Export(TEMP_STOCKS_PAT0_PATH)
			break

# Within the exported StockFaceTex brres, clear everything that isn't a stock icon tex0 or plt0
def purgeAllExceptStocks():
	parentBrres = BrawlAPI.RootNode
	unusedTEX0List = []
	unusedPLT0List = []

	# Delete any groups other than Textures and Palettes
	groupsToDelete = []
	
	for bresGroup in parentBrres.Children:
		if bresGroup.Name not in ["Textures(NW4R)", "Palettes(NW4R)"]:
			groupsToDelete.append(bresGroup)
	
	removeChildNodes(groupsToDelete)
	
	# Only textures and palette groups should remain
	if len(parentBrres.Children) != 2:
		BrawlAPI.ShowError("Unexpected data in info.pac MiscData30 brres", "Error")
		return 0
	
	# Generate lists of tex0 and plt0 nodes that aren't stocks
	tex0Group = getChildFromName(parentBrres,"Textures")
	plt0Group = getChildFromName(parentBrres,"Palettes")
	
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

	# Iterate through children of ARC 2 to find MiscData 110
	for child in BrawlAPI.RootNode.Children[1].Children:
		if isinstance(child, BRRESNode) and child.HasChildren and "[110]" in child.Name:
			MiscData110 = child
			break
	
	# Iterate through MiscData 110 to find pat0 folder
	for child in MiscData110.Children:
		if "AnmTexPat(NW4R)" in child.Name:
			pat0Folder = child
			break
	
	# Iterate through pat0 folder to find existing stockface pat0
	for child in pat0Folder.Children:
		if STOCKFACE_PAT0_NAME in child.Name:
			# Replace existing pat0 animation in STGRESULT with the temp pat0 (from info.pac)
			child.Replace(TEMP_STOCKS_PAT0_PATH)
			return

# Find MiscData 120 inside STGRESULT.pac, or MiscData90 inside selcharacter.pac, and replace with stocks BRRES
def importBrresIntoPac(pacFilePath, brresFilePath):
	BrawlAPI.OpenFile(pacFilePath)
	
	# STGRESULT.pac > MiscData120 brres
	if "result" in BrawlAPI.RootNode.Name.lower() and isinstance(BrawlAPI.RootNode, ARCNode):
		for child in BrawlAPI.RootNode.Children[1].Children:
			if "[120]" in child.Name and isinstance(child, BRRESNode) and child.HasChildren:
				child.Replace(brresFilePath)
				return
	
	# sc_selcharacter.pac > MiscData90 brres
	elif "selcharacter" in BrawlAPI.RootNode.Name and isinstance(BrawlAPI.RootNode, ARCNode):
		for child in BrawlAPI.NodeListOfType[BRRESNode]():
			if "[90]" in child.Name and isinstance (child, BRRESNode) and child.HasChildren:
				child.Replace(brresFilePath)
				return		

## End helper functions
## Start loader functions

# Base info.pac RootNode function to isolate the MiscData 30 brres, then call main()
def export_stocks_from_info_arc(sender, event_args):
	if BrawlAPI.ShowOKCancelPrompt(INIT_PROMPT_TEXT, SCRIPT_NAME):
	
		# Locate MiscData30 inside info.pac
		for child in BrawlAPI.SelectedNode.Children:
			# Export MiscData 30 brres to a temp file
			if isinstance(child, BRRESNode) and child.HasChildren and "[30]" in child.Name:
				main(child)
				return
		

# Base MiscData30 function to isolate the MiscData 30 brres, then call main()
def export_stocks_from_miscdata30(sender, event_args):
	if BrawlAPI.ShowOKCancelPrompt(INIT_PROMPT_TEXT, SCRIPT_NAME):
		main(BrawlAPI.SelectedNode)
		return

## End loader functions
## Start main function

# Given the MiscData30 node, export/import data to the other files
def main(node):
	global STOCKFACETEX_BRRES_PATH
	
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

# From parent ARC
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export data to STGRESULT, StockFaceTex, and selcharacter files", EnableCheckARC, ToolStripMenuItem("Export stock icons", None, export_stocks_from_info_arc))

# From MiscData30 BRRES
BrawlAPI.AddContextMenuItem(BRESWrapper, "", "Export data to STGRESULT, StockFaceTex, and selcharacter files", EnableCheckBRES, ToolStripMenuItem("Export stock icons", None, export_stocks_from_miscdata30))
