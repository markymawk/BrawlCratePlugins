__author__ = "mawwwk and soopercool101"
__version__ = "1.2.1"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Locate TEX0 Usage"
SELECTED_TEX0_NAME = ""

modelUses = []		# List of lists[3] which contain model, material, and object names that use the selected tex0
usedPAT0Names = []	# List of PAT0 node names that use the selected tex0

## Start enable check function
# Check that tex0 is under a "2 ARC" to determine that the pac is a stage, not a character
# Wrapper: TEX0Wrapper
def EnableCheckTEX0(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None \
	and BrawlAPI.SelectedNode.Parent is not None \
	and BrawlAPI.SelectedNode.Parent.Parent is not None \
	and BrawlAPI.SelectedNode.Parent.Parent.Parent is not None)
	#and BrawlAPI.SelectedNode.Parent.Parent.Parent.Name == "2")

## End enable check function
## Start helper functions

# Given a modeldata brres, iterate through MDL0 and PAT0 nodes
def parseModelData(brres):
	modelsGroup = getChildFromName(brres, "3DModels")
	pat0Group = getChildFromName(brres, "AnmTexPat")
	
	# Iterate through models
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			parseMDL0(mdl0)
	
	# Iterate through pat0s
	if pat0Group:
		for pat0 in pat0Group.Children:
			parsePAT0(pat0)

# Scan MDL0 node for selected tex0 use, and append to modelUses[]
def parseMDL0(mdl0):
	mdl0TexturesGroup = getChildFromName(mdl0, "Textures")
	
	# If texture exists in the mdl0 Textures group, append an entry to modelUses[]
	if mdl0TexturesGroup and SELECTED_TEX0_NAME in getChildNames(mdl0TexturesGroup):
		# Model name, for entry[0]
		modelName = "MDL0: " + mdl0.Parent.Parent.Name + "/" + mdl0.Name
		
		# Materials names, for entry[1]
		materialsNamesList = getUsedMaterialsNames(mdl0TexturesGroup)
		
		# Objects names, for entry[2]
		objectsNamesList = getUsedObjectsList(mdl0, materialsNamesList)
		
		modelUses.append([modelName, materialsNamesList, objectsNamesList])
	
# Given a mdl0 "Textures" group, return a formatted string containing list of used materials that reference SELECTED_TEX0_NAME
def getUsedMaterialsNames(mdl0TexturesGroup):
	mdl0TextureNode = getChildFromName(mdl0TexturesGroup, SELECTED_TEX0_NAME, True)
	
	materialsNamesList = []
	for i in mdl0TextureNode.References:
		materialsNamesList.append(str(i))
	
	return materialsNamesList

# Given a mdl0 node and list of material names, return a list of objects used by those mats
def getUsedObjectsList(mdl0, materialsList):
	materialsGroup = getChildFromName(mdl0, "Materials")
	objectsList = []
	
	for i in materialsList:
	
		# Get material from name
		mat = getChildFromName(materialsGroup,i)
		
		# If material exists and is used by objects, append the object(s) to objectsList[]
		if mat and len(mat._objects):
			for o in mat._objects:
				objectsList.append(o.Name)
				
	return objectsList

def parsePAT0(pat0):
	# Get material from base pat0 node
	for material in pat0.Children:
		# For texture reference in material
		for texRef in material.Children:
			# If texture exists in the pat0, append to usedPAT0Names[]
			if SELECTED_TEX0_NAME in getChildNames(texRef):
				usedPAT0Names.append("PAT0: " + pat0.Parent.Parent.Name + "/" + pat0.Name)

## End helper functions
## Start loader functions

# Function to scan the stage PAC file
def locate_tex0_usage(sender, event_args):
	global SELECTED_TEX0_NAME
	SELECTED_TEX0_NAME = BrawlAPI.SelectedNode.Name
	PARENT_BRRES = BrawlAPI.SelectedNode.Parent.Parent
	error = False
	
	# Clear lists at the beginning of each run
	del modelUses[:]
	del usedPAT0Names[:]
	
	# Determine where to check for the selected tex0
	# If selected tex0 is in a TextureData, scan all brres in the pac
	if "Texture Data" in PARENT_BRRES.Name:
		for node in BrawlAPI.NodeListOfType[BRRESNode]():
			if "Model Data" in node.Name:
				parseModelData(node)
	
	# If selected tex0 is in a ModelData brres, only scan that ModelData
	elif "Model Data" in PARENT_BRRES.Name or "Misc Data" in PARENT_BRRES.Name:
		parseModelData(PARENT_BRRES)
	
	# Else, error -- can't detect parent brres
	else:
		BrawlAPI.ShowError("Error: can't detect parent BRRES format", SCRIPT_NAME)
		error = True
	
	# Results
	
	if not error:
	
		# If tex0 is used
		if len(modelUses + usedPAT0Names):
			message = SELECTED_TEX0_NAME + " found in:\n\n"
			
			# For each model use, show mdl0, material, and object names
			for entry in modelUses:
			
				# MDL0 name
				message += entry[0] + "\n"
				
				# Material name(s)
				for matName in entry[1]:
					message += "Material: " + matName + "\n"
				
				# Object name(s)
				for objName in entry[2]:
					message += "Object: " + objName + "\n"
				
				message += "\n\n"
				
			# For each pat0 use, add pat0 name
			for i in usedPAT0Names:
				message += i + "\n"
			
			BrawlAPI.ShowMessage(message, SCRIPT_NAME)
		
		# If tex0 not used
		else:
			BrawlAPI.ShowError("No TEX0 usage found", SCRIPT_NAME)

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Detect uses in models or pat0 animations", EnableCheckTEX0, ToolStripMenuItem("Locate", None, locate_tex0_usage))
