__author__ = "mawwwk"
__version__ = "1.2"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Rename TEX0 (preserve references)"

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

def rename_tex0_and_references(sender, event_args):
	textureNode = BrawlAPI.SelectedNode
	nodeNameOrig = textureNode.Name
	deleteAndMerge = False # True if texture is to be renamed/merged into another existing one
	# Prompt for new name
	newName = BrawlAPI.UserStringInput(SCRIPT_NAME, nodeNameOrig)
	
	if not newName:
		return
	
	# If name already exists in the current brres textures, throw an error
	if newName in getChildNames(textureNode.Parent):
		deleteAndMerge = BrawlAPI.ShowOKCancelWarning("TEX0 with name \"" + newName + "\" already exists.\nDelete the currently-selected TEX0 and merge references?", "Duplicate texture name found")
		if not deleteAndMerge:
			return
	
	# Change TEX0 name
	if not deleteAndMerge:
		textureNode.Name = newName
	
	# If TEX0 is inside a TextureData BRRES, rename references across the entire file
	parentBRRES = textureNode.Parent.Parent
	if "Texture" in parentBRRES.Name and isinstance(parentBRRES, BRRESNode):
	
		# Rename PAT0 references
		for pat0 in BrawlAPI.NodeListOfType[PAT0Node]():
			dmsg(pat0.Name)
			renamePAT0(pat0, nodeNameOrig, newName)
		
		# Rename mat references 
		for matRef in BrawlAPI.NodeListOfType[MDL0MaterialRefNode]():
			if matRef.Name == nodeNameOrig:
				matRef.Texture = newName
			if matRef.Palette.Name == nodeNameOrig:
				matRef.Palette = newName
	
	# If TEX0 is inside a ModelData or MiscData brres, rename only within that BRRES
	else:
		PAT0Group = getChildFromName(parentBRRES, "AnmTexPat")
		modelsGroup = getChildFromName(parentBRRES, "Models")
		
		# Rename PAT0 references
		if PAT0Group:
			for pat0 in PAT0Group.Children:
				renamePAT0(pat0, nodeNameOrig, newName)
		
		# Rename mat references
		if modelsGroup:
			for mdl0 in modelsGroup.Children:
				matsGroup = getChildFromName(mdl0, "Materials")
				if matsGroup:
					for mat in matsGroup.Children:
						if mat.Children:
							for matRef in mat.Children:
								if matRef.Name == nodeNameOrig:
									matRef.Name = newName
									matRef.Palette = newName
	
	if deleteAndMerge:
		textureNode.Remove()

## End loader function
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Rename TEX0 and all matching entries in PAT0s or matRefs", EnableCheckTEX0, ToolStripMenuItem("Rename (preserve references)", None, rename_tex0_and_references))
