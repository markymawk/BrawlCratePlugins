__author__ = "mawwwk and soopercool101"
__version__ = "1.3"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Locate TEX0 Usage"

## Start enable check function
# Wrapper: TEX0Wrapper
def EnableCheckTEX0(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None \
	and BrawlAPI.SelectedNode.Parent is not None)

## End enable check function
## Start helper functions

# Given a brres Models group, check for usage in MDL0s
def findModelUses(modelsGroup, tex0Name):
	modelUses = []
	for mdl0 in modelsGroup.Children:
		mdl0TexturesGroup = mdl0.FindChild("Textures")
	
		# If texture exists in the mdl0 Textures group, append an entry to modelUses[]
		if mdl0TexturesGroup and tex0Name in getChildNames(mdl0TexturesGroup):
		
			# Model name, for entry[0]
			modelName = "MDL0: " + mdl0.Parent.Parent.Name + "/" + mdl0.Name
			
			# Materials names, for entry[1]
			materialsNamesList = getUsedMaterialsNames(mdl0TexturesGroup, tex0Name)
			
			# Objects names, for entry[2]
			objectsNamesList = getUsedObjectsList(mdl0, materialsNamesList)
			
			modelUses.append([modelName, materialsNamesList, objectsNamesList])
	return modelUses

# Given a brres PAT0 group, check for usage in PAT0s
def checkPAT0Uses(pat0Group, tex0Name):
	pat0Uses = []
	for pat0 in pat0Group.Children:
		# Get material from base pat0 node
		for material in pat0.Children:
			# For texture reference in material
			for texRef in material.Children:
				# If texture exists in the pat0, append to usedPAT0Names[]
				if tex0Name in getChildNames(texRef):
						pat0Uses.append("PAT0: " + pat0.Parent.Parent.Name + "/" + pat0.Name)
	return pat0Uses

# Given a MDL0 Textures group, return a formatted string containing list of used materials that reference selected TEX0 name
def getUsedMaterialsNames(mdl0TexturesGroup, tex0Name):
	mdl0TextureNode = mdl0TexturesGroup.FindChild(tex0Name)
	
	materialsNamesList = []
	for i in mdl0TextureNode.References:
		materialsNamesList.append(str(i))
	
	return materialsNamesList

# Given a mdl0 node and list of material names, return a list of objects used by those mats
def getUsedObjectsList(mdl0, materialsList):
	matsGroup = mdl0.FindChild("Materials")
	objectsList = []
	
	for i in materialsList:
	
		# Get material from name
		mat = matsGroup.FindChild(i)
		
		# If material exists and is used by objects, append the object(s) to objectsList[]
		if mat and len(mat._objects):
			for o in mat._objects:
				objectsList.append(o.Name)
				
	return objectsList

## End helper functions
## Start loader functions

def locate_tex0_usage(sender, event_args):
	tex0Name = BrawlAPI.SelectedNode.Name
	parentBRRES = BrawlAPI.SelectedNode.Parent.Parent
	
	allModelUses = [] # List of lists[3] which contain model, material, and object names that use the selected tex0
	allPAT0Uses = []  # List of PAT0 node names that use the selected tex0
	
	# If selected tex0 is in a TextureData, scan all brres nodes in the file
	if "Texture Data" in parentBRRES.Name:
		for brres in BrawlAPI.NodeListOfType[BRRESNode]():
			modelsGroup = brres.FindChild("3DModels(NW4R)")
			pat0Group = brres.FindChild("AnmTexPat(NW4R)")
			
			# Get individual MDL0 usage, then append to allModelUses[]
			if modelsGroup:
				thisModelUses = findModelUses(modelsGroup, tex0Name)
				
				for i in thisModelUses:
					allModelUses.append(i)
			
			# Get individual PAT0 usage, then append to allPAT0Uses[]
			if pat0Group:
				thisPAT0Uses = checkPAT0Uses(pat0Group, tex0Name)
				
				for i in thisPAT0Uses:
					allPAT0Uses.append(i)
	
	# If parent brres contains models or PAT0s, only check inside that brres
	elif parentBRRES.FindChild("3DModels(NW4R)") or parrentBRRES.FindChild("AnmTexPat(NW4R)"):
		modelsGroup = parentBRRES.FindChild("3DModels(NW4R)")
		pat0Group = parentBRRES.FindChild("AnmTexPat(NW4R)")
		
		# Get individual MDL0 usage, then append to allModelUses[]
		if modelsGroup:
			thisModelUses = findModelUses(modelsGroup, tex0Name)
			
			for i in thisModelUses:
				allModelUses.append(i)
		
		# Get individual PAT0 usage, then append to allPAT0Uses[]
		if pat0Group:
			thisPAT0Uses = checkPAT0Uses(pat0Group, tex0Name)
			
			for i in thisPAT0Uses:
				allPAT0Uses.append(i)
	
	# Else, error
	else:
		BrawlAPI.ShowError("Error: can't detect usable textures in parent BRRES", SCRIPT_NAME)
		return
	
	# Results
	# If tex0 is used, show list of uses
	if len(allModelUses + allPAT0Uses):
		message = tex0Name + " found in:\n\n"
		
		# For each model use, show mdl0, material, and object names
		for entry in allModelUses:
		
			message += entry[0] + "\n"
			
			for matName in entry[1]:
				message += "Material: " + matName + "\n"
			
			for objName in entry[2]:
				message += "Object: " + objName + "\n"
			
			message += "\n\n"
			
		# List PAT0 uses
		for i in allPAT0Uses:
			message += i + "\n"
		
		BrawlAPI.ShowMessage(message, SCRIPT_NAME)
	
	# If tex0 not used
	else:
		BrawlAPI.ShowError("No TEX0 usage found", SCRIPT_NAME)

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Find tex0 usage in models or pat0 animations", EnableCheckTEX0, ToolStripMenuItem("Locate", None, locate_tex0_usage))
