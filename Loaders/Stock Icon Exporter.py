__author__ = "mawwwk"
__version__ = "1.0.1"

from BrawlCrate.API import *
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlCrate.NodeWrappers import ARCWrapper
from BrawlCrate.NodeWrappers import BRESWrapper
from BrawlCrate.NodeWrappers import FolderWrapper
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from System.IO import File

# Store temp files in the BrawlCrate program folder.
# These are deleted at the end of the script.
TEMP_BRRES_PATH = AppPath + "\STOCKS_BRRES_EXPORT_temp.brres"
TEMP_STOCKS_PAT0_PATH = AppPath + "\STOCKFACE_PAT0_EXPORT_temp.pat0"

# Name of the pat0 animation that contains frames for each stock icon
STOCKFACE_PAT0_NAME = "InfStockface_TopN__0"

# Any bres groups that aren't palettes or textures
nonTextureFolderNames = ["3DModels(NW4R)", "AnmChr(NW4R)", "AnmVis(NW4R)", "AnmClr(NW4R)", "AnmTexPat(NW4R)", "AnmTexSrt(NW4R)"]

SCRIPT_NAME = "Stock Icon Exporter"

# Text shown before running the plug-in
INIT_PROMPT_TEXT = "Export stock icon data from this file to STGRESULT.pac, StockFaceTex.brres, and sc_selcharacter.pac.\n\nPress OK to continue."

# Check to ensure the context menu item is only active if it's info.pac
def EnableCheckARC(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and BrawlAPI.SelectedNode.Name == "info_en")
	
# Same as above, but from MiscData 30
def EnableCheckBRES(sender, event_args):
	bres = BrawlAPI.SelectedNode
	sender.Enabled = (bres is not None and "[30]" in bres.Name and "info_en" in bres.Parent.Name)

# Locate stockface pat0 in info.pac, and export to a temp pat0 file
def exportStockfacePat0():
	# Determine pat0 folder within selected brres
	for childFolder in BrawlAPI.SelectedNode.Children:
		if "AnmTexPat(NW4R)" in childFolder.Name:
			pat0List = childFolder.Children
			break
	# Find Stockface pat0 and export to temp file
	for pat0 in pat0List:
		if STOCKFACE_PAT0_NAME in pat0.Name:
			pat0.Export(TEMP_STOCKS_PAT0_PATH)
			break

# Assuming parent brres is selected, clear everything that isn't a stock icon tex0 or plt0
def purgeAllExceptStocks():
	parentBrres = BrawlAPI.SelectedNode
	
	# Generate list of extra bres groups (models, vis, chr, ...)
	groupsToDelete = []
	
	for bresGroup in BrawlAPI.SelectedNode.Children:
		if bresGroup.Name in nonTextureFolderNames:
			groupsToDelete.append(bresGroup)
	
	# Delete bres groups
	# Iterate from the bottom-up, as to not throw an error from changing the node positions
	groupsToDelete.reverse()
	for group in groupsToDelete:
		parentBrres.RemoveChild(group)
	
	# Only textures and palette groups should remain. Assign accordingly
	if "Textures" in parentBrres.Children[0].Name:
		tex0Group = parentBrres.Children[0]
		plt0Group = parentBrres.Children[1]
	else:
		tex0Group = parentBrres.Children[1]
		plt0Group = parentBrres.Children[0]
	
	# Generate lists of tex0 and plt0 nodes that aren't stocks
	tex0ToDelete = []
	plt0ToDelete = []
	
	for tex0 in tex0Group.Children:
		if tex0.Name[:7] != "InfStc.":
			tex0ToDelete.append(tex0)
	
	for plt0 in plt0Group.Children:
		if plt0.Name[:7] != "InfStc.":
			plt0ToDelete.append(plt0)
	
	# Reverse lists so nodes get deleted from bottom-up
	tex0ToDelete.reverse()
	plt0ToDelete.reverse()
	
	# Delete non-stocks textures
	for tex0 in tex0ToDelete:
		tex0Group.RemoveChild(tex0)
	for plt0 in plt0ToDelete:
		plt0Group.RemoveChild(plt0)	

# After opening STGRESULT.pac, replace the existing Stockface pat0 inside MiscData 110
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
			existingStockfacePat0 = child
	
	# Replace existing pat0 animation in STGRESULT with the temp pat0 (from info.pac)
	existingStockfacePat0.Replace(TEMP_STOCKS_PAT0_PATH)

# Find MiscData 120 inside STGRESULT.pac and replace with temp brres
def importBrresIntoSTGRESULTpac():
	for child in BrawlAPI.RootNode.Children[1].Children:
		if isinstance(child, BRRESNode) and child.HasChildren and "[120]" in child.Name:
			child.Replace(TEMP_BRRES_PATH)
			break

# Find MiscData 90 inside sc_selcharacter.pac and replace with temp brres
def importBrresIntoSelCharacterPac():
	if "selcharacter" in BrawlAPI.RootNode.Name and isinstance(BrawlAPI.RootNode, ARCNode):
		for child in BrawlAPI.RootNode.Children:
			if isinstance(child, BRRESNode) and child.HasChildren and "[90]" in child.Name:
				child.Replace(TEMP_BRRES_PATH)
				break		

# Base function to export stocks from info.pac to other appropriate locations
def export_stocks_from_info_arc(sender, event_args):
	if BrawlAPI.ShowOKCancelPrompt(INIT_PROMPT_TEXT, SCRIPT_NAME):
	
		# Locate MiscData30 inside info.pac
		for child in BrawlAPI.SelectedNode.Children:
			# Export MiscData 30 brres to a temp file
			if isinstance(child, BRRESNode) and child.HasChildren and "[30]" in child.Name:
				child.ExportUncompressed(TEMP_BRRES_PATH)
		main()

# Same function as above, but ran from the MiscData 30 brres
def export_stocks_from_miscdata30(sender, event_args):
	if BrawlAPI.ShowOKCancelPrompt(INIT_PROMPT_TEXT, SCRIPT_NAME):
		BrawlAPI.SelectedNode.ExportUncompressed(TEMP_BRRES_PATH)
		main()

def main():
	INFO_PAC_PATH = BrawlAPI.SelectedNode.FilePath
	
	# Derive build pf path from the open info.pac file
	PF_FOLDER = str(INFO_PAC_PATH).split("\info2\info.pac")[0]
	STOCKFACETEX_BRRES_PATH = PF_FOLDER + "\menu\common\StockFaceTex.brres"
	RESULTS_PAC_PATH = PF_FOLDER + "\stage\melee\STGRESULT.pac"
	SELCHARACTER_PAC_PATH = PF_FOLDER + "\menu2\sc_selcharacter.pac"
	
	# Close info.pac and open the temp brres
	BrawlAPI.CloseFile()
	BrawlAPI.OpenFile(TEMP_BRRES_PATH)
	
	# With temp brres open, export stockface pat0 animation, and clear out any unused data
	exportStockfacePat0()
	purgeAllExceptStocks()
	BrawlAPI.SaveFile()
	
	# Save to StockFaceTex.brres (file 1 of 3)
	BrawlAPI.SaveFileAs(STOCKFACETEX_BRRES_PATH)
	
	# Close temp brres
	BrawlAPI.CloseFile()
	
	# Open STGRESULT, and import pat0 and new brres
	BrawlAPI.OpenFile(RESULTS_PAC_PATH)
	importStockfaceIntoSTGRESULTpac()
	importBrresIntoSTGRESULTpac()
	
	# Close STGRESULT (file 2 of 3)
	BrawlAPI.SaveFile()
	BrawlAPI.CloseFile()
	
	# Import into selcharacter MiscData90 (file 3 of 3)
	BrawlAPI.OpenFile(SELCHARACTER_PAC_PATH)
	importBrresIntoSelCharacterPac()
	BrawlAPI.SaveFile()
	BrawlAPI.CloseFile()
	
	# Re-open info.pac after all other files are handled
	BrawlAPI.OpenFile(INFO_PAC_PATH)
	
	# Delete temp files
	File.Delete(TEMP_BRRES_PATH)
	File.Delete(TEMP_STOCKS_PAT0_PATH)
	
	# Script complete!
	msg = "Stock tex0, plt0, and pat0 successfully exported from info.pac to: \n\n" + \
	STOCKFACETEX_BRRES_PATH + "\n\n" + RESULTS_PAC_PATH + "\n\n" + SELCHARACTER_PAC_PATH
	BrawlAPI.ShowMessage(msg, "Success!")
	
# Add right-click contextual menu options
BrawlAPI.AddContextMenuItem(ARCWrapper, "", "Export data to STGRESULT, StockFaceTex, and selcharacter files", EnableCheckARC, ToolStripMenuItem("Export stock icons", None, export_stocks_from_info_arc))
BrawlAPI.AddContextMenuItem(BRESWrapper, "", "Export data to STGRESULT, StockFaceTex, and selcharacter files", EnableCheckBRES, ToolStripMenuItem("Export stock icons", None, export_stocks_from_miscdata30))
