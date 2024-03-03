__author__ = "mawwwk and soopercool101"
__version__ = "2.0"

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
	and BrawlAPI.SelectedNode.Parent is not None \
	and BrawlAPI.SelectedNode.Parent.Parent is not None \
	and BrawlAPI.SelectedNode.Parent.Parent.Parent is not None)

## End enable check function
## Start helper functions

# Given a modeldata brres, check any MDL0 and PAT0 nodes
# Returns list as [MDL0 uses, PAT0 uses]
def checkModelData(brres, tex0Name):
	modelsGroup = brres.FindChild("3DModels(NW4R)")
	pat0Group = brres.FindChild("AnmTexPat(NW4R)")
	modelData_mdl0_uses = []
	modelData_pat0_uses = []
	
	# Loop through models
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			modelData_mdl0_uses = scanMDL0(mdl0, tex0Name)
	
	# Loop through PAT0 animations
	if pat0Group:
		for pat0 in pat0Group.Children:
			modelData_pat0_uses = scanPAT0(pat0, tex0Name)
	
	return [modelData_mdl0_uses, modelData_pat0_uses]

# Scan MDL0 node for selected TEX0 use, and append to modelUses[]
def scanMDL0(mdl0, tex0Name):
	mdl0TexturesGroup = mdl0.FindChild("Textures")
	modelUses = []
	
	# If texture exists in the mdl0 Textures group, append an entry to modelUses[]
	isTextureUsed = mdl0TexturesGroup and mdl0TexturesGroup.FindChild(tex0Name)
	if isTextureUsed:
		# Model name, for modelUses[0]
		modelName = "MDL0: " + mdl0.Parent.Parent.Name + "/" + mdl0.Name
		
		# Materials' names, for modelUses[1]
		usedMaterialNames = getUsedMatNames(mdl0TexturesGroup, tex0Name)
		
		# Objects' names, for modelUses[2]
		usedObjectNames = getUsedObjectNames(mdl0, usedMaterialNames)
		
		modelUses.append([modelName, usedMaterialNames, usedObjectNames])
	return modelUses
	
# Given a MDL0 "Textures" group, return a formatted string containing list of used materials that reference the TEX0 name
def getUsedMatNames(mdl0TexturesGroup, tex0Name):
	textureRef = mdl0TexturesGroup.FindChild(tex0Name)
	usedMaterialNames = []
	for i in textureRef.References:
		usedMaterialNames.append(str(i))
	
	return usedMaterialNames

# Given a MDL0 node and list of material names, return a list of objects used by those mats
def getUsedObjectNames(mdl0, usedMaterialNames):
	materialsGroup = mdl0.FindChild("Materials")
	usedObjectNames = []
	
	for mat in usedMaterialNames:
		mat = materialsGroup.FindChild(mat)
		
		# If material exists and is used by objects, append the object name to usedObjectNames[]
		if mat and len(mat._objects):
			for o in mat._objects:
				usedObjectNames.append(o.Name)
				
	return usedObjectNames

def scanPAT0(pat0, tex0Name):
	brresName = pat0.Parent.Parent.Name
	usedPAT0Names = []
	# Get material from base pat0 node
	for material in pat0.Children:
		for texRef in material.Children:
			# If texture exists in the pat0, append to usedPAT0Names[]
			if tex0Name in getChildNames(texRef):
				usedPAT0Names.append("PAT0: " + brresName + "/" + pat0.Name)
	return usedPAT0Names

## End helper functions
## Start loader functions

# Function to scan the stage PAC file
def locate_tex0_usage(sender, event_args):
	tex0Name = BrawlAPI.SelectedNode.Name
	parentBrres = BrawlAPI.SelectedNode.Parent.Parent
	modelUses = []	# List of lists[3] which contain model, material, and object names that use the selected tex0
	pat0Uses = []	# List of PAT0 node names that use the selected tex0
	
	# Determine where to check for the selected tex0
	# If selected tex0 is in a TextureData, scan all brres in the pac
	if "Texture Data" in parentBrres.Name:
		for brres in BrawlAPI.NodeListOfType[BRRESNode]():
			brresUses = checkModelData(brres, tex0Name)
			# Append MDL0 use
			for mdl0Usage in brresUses[0]:
				modelUses.append(mdl0Usage)
			# Append PAT0 use
			for pat0Usage in brresUses[1]:
				pat0Uses.append(pat0Usage)
	
	# If selected tex0 is in a ModelData or MiscData brres, only scan that brres
	elif parentBrres.FindChild("3DModels(NW4R)"):
		brresUses = checkModelData(parentBrres, tex0Name)
		# Append MDL0 use
		for mdl0Usage in brresUses[0]:
			modelUses.append(mdl0Usage)
		# Append PAT0 use
		for pat0Usage in brresUses[1]:
			pat0Uses.append(pat0Usage)
	
	# If brres not found, error & quit
	else:
		BrawlAPI.ShowError("Error: can't detect parent BRRES format", SCRIPT_NAME)
		return
	
	# Results
	# If tex0 is not used
	if not len(modelUses + pat0Uses):
		BrawlAPI.ShowError("No TEX0 usage found", SCRIPT_NAME)
		return
	
	# If tex0 is used
	message = tex0Name + " used in:\n\n"
	
	# For each model use, show mdl0, material, and object names
	for entry in modelUses:
		message += entry[0] + "\n"	# MDL0 name
		
		for matName in entry[1]:
			message += "Material: " + matName + "\n" # Material name(s)
		
		for objName in entry[2]:
			message += "Object: " + objName + "\n"	# Object name(s)
		
		message += "\n\n"
		
	message = message[:-2]	# Chop ending line breaks
	if len(pat0Uses):
		# For each pat0 use, add pat0 name
		message += "\n\n" + listToString(pat0Uses)
	
	BrawlAPI.ShowMessage(message, SCRIPT_NAME)

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Detect texture usage in models or PAT0 animations", EnableCheckTEX0, ToolStripMenuItem("Locate", None, locate_tex0_usage))
