__author__ = "mawwwk and soopercool101"
__version__ = "1.2"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem

SCRIPT_NAME = "Locate TEX0 Usage"
SELECTED_TEX0_NAME = ""

modelUses = []
usedPAT0Names = []

# Check that tex0 is under a "2 ARC" to determine that the pac is a stage, not a character
# Wrapper: TEX0Wrapper
def EnableCheckTEX0(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and BrawlAPI.SelectedNode.Parent is not None and BrawlAPI.SelectedNode.Parent.Parent is not None and BrawlAPI.SelectedNode.Parent.Parent.Parent is not None and BrawlAPI.SelectedNode.Parent.Parent.Parent.Name == "2")

# Function to return to 2 ARC of current file
def getParentArc():
	for i in BrawlAPI.RootNode.Children:
		if i.Name == "2" and isinstance(i, ARCNode):
			return i
	
	BrawlAPI.ShowError("2 ARC not found", "Error")
	return 0	# If not found, return 0

# Given any node, return its child node whose name contains the given nameStr
def getChildFromName(node, nameStr, EXACT_NEEDED=False):
	if node.Children:
		for child in node.Children:
			if EXACT_NEEDED and child.Name == str(nameStr):
				return child
			elif str(nameStr) in child.Name:
				return child
	return 0	# If not found, return 0

def parseBrres(node):
	if "Model Data" in node.Name:
		parseModelData(node)

# Return list of strings of node names in a given group
def getChildNames(group):
	list = []
	for i in group.Children:
		list.append(i.Name)
	return list

def parseModelData(brres):
	modelsGroup = getChildFromName(brres, "3DModels")
	pat0Group = getChildFromName(brres, "AnmTexPat")
	
	# Iterate through models
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			# Ignore static models
			if mdl0.Name.lower() != "static":
				parseMDL0(mdl0)
	
	# Iterate through pat0s
	if pat0Group:
		for pat0 in pat0Group.Children:
			parsePAT0(pat0)

def parseMDL0(mdl0):
	mdl0TexturesGroup = getChildFromName(mdl0, "Textures")
	
	# If texture exists in the mdl0 Textures group, append an entry to modelUses[]
	if mdl0TexturesGroup and SELECTED_TEX0_NAME in getChildNames(mdl0TexturesGroup):
		materialsNamesList = getUsedMaterialsNames(mdl0TexturesGroup)
		
		entry = ["MDL0: " + mdl0.Parent.Parent.Name + "/" + mdl0.Name, 	# entry[0] MDL0 name
		materialsNamesList,								# entry[1] List of names of materials used in the mdl0
		getUsedObjectsList(mdl0, materialsNamesList)]		# entry[2] List of objects that use the texture
		
		modelUses.append(entry)
	
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

# Function to scan the stage PAC file
def locate_tex0_usage(sender, event_args):
	global SELECTED_TEX0_NAME
	SELECTED_TEX0_NAME = BrawlAPI.SelectedNode.Name
	PARENT_BRRES = BrawlAPI.SelectedNode.Parent.Parent
	error = False
	
	# Clear lists at the beginning of each run
	del modelUses[:]
	del usedPAT0Names[:]
	
	# If selected tex0 is in a TextureData, scan all brres in the pac
	if "Texture Data" in PARENT_BRRES.Name:
		for node in getParentArc().Children:
			if isinstance(node, BRRESNode):
				parseBrres(node)
	# If selected tex0 is in a ModelData brres, only scan that ModelData
	elif "Model Data" in PARENT_BRRES.Name:
		parseBrres(PARENT_BRRES)
	# Else, error -- can't detect parent brres
	else:
		BrawlAPI.ShowError("Error: can't detect parent BRRES format", SCRIPT_NAME)
		error = True
	
	IS_MDL0_FOUND = len(modelUses)
	IS_PAT0_FOUND = len(usedPAT0Names)
	
	if not error:
		message = ""
		if IS_MDL0_FOUND or IS_PAT0_FOUND:
			message += SELECTED_TEX0_NAME + " found in:\n\n"
			for entry in modelUses:
				message += entry[0] + "\n"# MDL0 name
				for matName in entry[1]:
					message += "Material: " + matName + "\n"
				for objName in entry[2]:
					message += "Object: " + objName + "\n"
				message += "\n\n"
			for i in usedPAT0Names:
				message += i + "\n"
			BrawlAPI.ShowMessage(message, SCRIPT_NAME)
		else:
			BrawlAPI.ShowError("No TEX0 usage found", SCRIPT_NAME)

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Detect uses in models or pat0 animations", EnableCheckTEX0, ToolStripMenuItem("Locate", None, locate_tex0_usage))
