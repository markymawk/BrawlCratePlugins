__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Rename Within PAT0"

## Start enable check function
# Check that tex0 is under a BRRES
# Wrapper: TEX0Wrapper
def EnableCheckTEX0(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None \
	and BrawlAPI.SelectedNode.Parent is not None \
	and BrawlAPI.SelectedNode.Parent.Parent is not None)

## End enable check function
## Start helper functions

def renamePAT0(pat0, oldName, newName):
	for pat0Material in pat0.Children:
		for pat0TextureEntry in pat0Material.Children:
			for pat0TextureRef in pat0TextureEntry.Children:
				
				# Change texture name
				if pat0TextureRef.Name == oldName:
					pat0TextureRef.Name = newName
				
				# Change palette name, if exists
				if pat0TextureRef.Palette == oldName:
					pat0TextureRef.Palette = newName

## End helper functions
## Start loader function

def rename_tex0_within_pat0(sender, event_args):
	textureNode = BrawlAPI.SelectedNode
	nodeNameOrig = textureNode.Name
	
	# Prompt for new name
	newName = BrawlAPI.UserStringInput(SCRIPT_NAME, nodeNameOrig)
	
	if not newName:
		return
	
	# If name already exists in the current brres textures, throw an error
	if newName in getChildNames(textureNode.Parent):
		BrawlAPI.ShowError("TEX0 with that name already exists.","Error")
		return
	
	# Change TEX0 name
	textureNode.Name = newName
	
	# If TEX0 is inside a TextureData BRRES, change PAT0s across the entire file
	parentBRRES = textureNode.Parent.Parent
	if "Texture" in parentBRRES.Name and isinstance(parentBRRES, BRESNode):
		for pat0 in BrawlAPI.NodeListOfType[PAT0Node]():
			dmsg(pat0.Name)
			renamePAT0(pat0, nodeNameOrig, newName)
	
	# if TEX0 is inside a ModelData or MiscData brres, change PAT0 only inside that BRRES
	else:
		PAT0Group = getChildFromName(parentBRRES, "AnmTexPat")
		
		if PAT0Group:
			for pat0 in PAT0Group.Children:
				renamePAT0(pat0, nodeNameOrig, newName)

## End loader function
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Rename TEX0 and all matching entries in PAT0 animations", EnableCheckTEX0, ToolStripMenuItem("Rename (Preserve PAT0 entries)", None, rename_tex0_within_pat0))
