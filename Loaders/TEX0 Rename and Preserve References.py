__author__ = "mawwwk"
__version__ = "1.2.2"

from BrawlCrate.NodeWrappers import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Rename TEX0 (Preserve References)"

## Start enable check function
# Check that tex0 is under a BRRES
# Wrapper: TEX0Wrapper
def EnableCheckTEX0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and node.Parent and node.Parent.Parent

## End enable check function
## Start helper functions

def renamePAT0Refs(pat0, oldName, newName):
	for pat0Material in pat0.Children:
		for pat0TextureEntry in pat0Material.Children:
			for pat0TextureRef in pat0TextureEntry.Children:
				
				# Change texture name
				if pat0TextureRef.Name == oldName:
					pat0TextureRef.Name = newName
				
				# Change palette name, if exists
				if pat0TextureRef.Palette == oldName:
					pat0TextureRef.Palette = newName

def renameMatRefs(mdl0, oldName, newName):
	matsGroup = mdl0.FindChild("Materials")
	if matsGroup:
		for mat in matsGroup.Children:
			if mat.HasChildren:
				for matRef in mat.Children:
					if matRef.Name == oldName:
						matRef.Name = newName
						matRef.Palette = newName
## End helper functions
## Start loader function

def rename_tex0_and_references(sender, event_args):
	textureNode = BrawlAPI.SelectedNode
	originalTEX0Name = textureNode.Name
	deleteAndMerge = False # True if texture is to be renamed/merged into another existing one
	parentBRRES = textureNode.Parent.Parent
	
	# Prompt for new name
	newTEX0Name = BrawlAPI.UserStringInput(SCRIPT_NAME, originalTEX0Name)
	
	if not newTEX0Name:
		return
	
	# If name already exists in the current brres textures, throw an error
	if newTEX0Name in getChildNames(textureNode.Parent):
		msg = "TEX0 with name \"" + newTEX0Name + "\" already exists.\nDelete the currently-selected TEX0 and merge references?"
		deleteAndMerge = BrawlAPI.ShowOKCancelWarning(msg, "Duplicate texture name found")
		if not deleteAndMerge:
			return
	
	# Rename/remove texture
	if deleteAndMerge:
		textureNode.Remove()
	else:
		textureNode.Name = newTEX0Name
	
	# If TEX0 is inside a TextureData BRRES, rename references across the entire file
	if "Texture" in parentBRRES.Name and isinstance(parentBRRES, BRRESNode):
		
		# Rename PAT0 references
		for pat0 in BrawlAPI.NodeListOfType[PAT0Node]():
			renamePAT0Refs(pat0, originalTEX0Name, newTEX0Name)
		
		# Rename mat references 
		for matRef in BrawlAPI.NodeListOfType[MDL0MaterialRefNode]():
			if matRef.Texture == originalTEX0Name:
				matRef.Texture = newTEX0Name
			if matRef.Palette and matRef.Palette == originalTEX0Name:
				matRef.Palette = newTEX0Name
	
	# If TEX0 is inside a ModelData or MiscData brres, rename only within that BRRES
	else:
		PAT0Group = parentBRRES.FindChild(PAT_GROUP)
		modelsGroup = parentBRRES.FindChild(MDL_GROUP)
		
		# Rename PAT0 references
		if PAT0Group:
			for pat0 in PAT0Group.Children:
				renamePAT0Refs(pat0, originalTEX0Name, newTEX0Name)
		
		# Rename material references
		if modelsGroup:
			for mdl0 in modelsGroup.Children:
				renameMatRefs(mdl0, originalTEX0Name, newTEX0Name)

## End loader function
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Rename TEX0 and all matching entries in PAT0s or matRefs", EnableCheckTEX0, ToolStripMenuItem("Rename (preserve references)", None, rename_tex0_and_references))
