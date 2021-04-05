__author__ = "mawwwk"
__version__ = "0.9.0.2"
# EXPERIMENTAL - Updated 4/4/21, might break things still.
# Always test in-game!! always save backups!!
from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *

texturesInMaterialsNamesList = []
texturesInPat0NamesList = []
deletedMatsNamesList = []
tex0List = []
deletedTex0NamesList = []

# Debug message
def message(msg):
	BrawlAPI.ShowMessage(msg, "DEBUG")

# Basic impl of list.reverse() to accommodate ResourceNode lists
def reverseResourceList(nodeList):
	nodeListReverse = []
	for i in nodeList:
		nodeListReverse.append(i)
	
	nodeListReverse.reverse()
	return nodeListReverse

# Function to return to 2 ARC of current file
def getParentArc():
	for i in BrawlAPI.RootNode.Children:
		if i.Name == "2" and isinstance(i, ARCNode):
			return i
	
	BrawlAPI.ShowError("2 ARC not found", "Error")
	return 0
	
# Retrieve texture data (materials, pat0, or tex0) from a given brres node
def parseBrres(node):
	if "Model Data" in node.Name:
		parseModelData(node)
	elif "Texture Data" in node.Name:
		parseTextureData(node)

# Given a ModelData brres, iterate through mdl0 and pat0 to populate used textures lists, then check for any tex0 nodes in the ModelData
def parseModelData(brres):
	# Iterate through models
	modelsGroup = getModelsGroup(brres)
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			texturesGroup = getModelTexturesGroup(mdl0)
			# If the mdl0 has Texture references or Materials, dive in
			if getModelTexturesGroup(mdl0) or getModelMaterialsGroup(mdl0):
				parseMDL0(mdl0)
	
	# Iterate through pat0s
	pat0Group = getPat0Group(brres)
	if pat0Group:
		for pat0 in pat0Group.Children:
			parsePAT0(pat0)
	
	# Check for tex0s in ModelData
	# DON'T delete these -- in cases like Smashville, the references are loaded from the module or elsewhere outside the brres
	modelDataTexturesGroup = getModelDataTexturesGroup(brres)
	if modelDataTexturesGroup:
		for tex0 in modelDataTexturesGroup.Children:
			# To simulate locality, delete the textures from "textures used" after logging them
			if tex0.Name in texturesInMaterialsNamesList:
				texturesInMaterialsNamesList.remove(tex0.Name)

# Given a mdl0 node, delete any unused materials, then log any texture references
def parseMDL0(mdl0):
	matsGroup = getModelMaterialsGroup(mdl0)
	
	# Start with deleting materials assigned to no objects
	if matsGroup:
		# Iterate from bottom-up
		mats = reverseResourceList(matsGroup.Children)
		
		# Iterate through materials in mdl0. If object count == 0, delete the material
		for m in mats:
			if not len(m._objects):
				deletedMatsNamesList.append(m.Name)
				m.Remove()
	
	# In each model, get the "Textures" folder and populate the script's list of used textures
	mdl0TexturesGroup = getModelTexturesGroup(mdl0)
	if mdl0TexturesGroup:
		textures = reverseResourceList(mdl0TexturesGroup.Children)
		for t in textures:
			if t.References:
				texturesInMaterialsNamesList.append(t.Name)
			# If Texture node isn't used by any materials, delete it instead
			else:
				t.Remove()

# Given a pat0 animation, iterate through child entries and log textures used
def parsePAT0(pat0):
	# Get material from base pat0 node
	for material in pat0.Children:
		# For texture reference in material
		for texRef in material.Children:
			# Iterate through frames and log texture names
			for frame in texRef.Children:
				texturesInPat0NamesList.append(frame.Name)

def getModelDataTexturesGroup(brresNode):
	if brresNode.Children:
		for group in brresNode.Children:
			if "Textures(" in group.Name:
				return group
	return 0

# Given a ModelData brres, return its PAT0 folder. Return 0 if not found
def getPat0Group(brresNode):
	if brresNode.Children:
		for group in brresNode.Children:
			if "AnmTexPat" in group.Name:
				return group
	return 0

# Given a ModelData brres, return its "3DModels" folder. Return 0 if not found
def getModelsGroup(brresNode):
	if brresNode.Children:
		for group in brresNode.Children:
			if "3DModels" in group.Name:
				return group
	return 0

# Given a mdl0 node, return its "Materials" folder. Return 0 if not found
def getModelMaterialsGroup(mdl0):
	for group in mdl0.Children:
		if "Materials" in group.Name:
			return group
	return 0

# Given a mdl0 node, return its "Textures" folder. Return 0 if not found
def getModelTexturesGroup(mdl0):
	for group in mdl0.Children:
		if "Textures" in group.Name:
			return group
	return 0

# Given a TextureData brres, log any tex0 nodes found, and delete any unused textures
def parseTextureData(brresNode):
	global tex0List
	TEX0_GROUP = getTextureDataTex0Group(brresNode)
	
	for tex0 in TEX0_GROUP.Children:
		tex0List.append(tex0)
	
	tex0List = reverseResourceList(tex0List)

# Given a TextureData brres, return the texture group inside
def getTextureDataTex0Group(brresNode):
	for i in brresNode.Children:
		if "Textures(" in i.Name:
			return i
	return 0

############################################
########### Start of main script ###########
############################################

# Confirmation prompt
msg = "Optimize textures for a stage .pac by auto-detecting unused materials and files.\n\n"
msg += "DISCLAIMER: Always check the final results in-game. Only recommended for use with Battlefield, FD, or Palutena-based stages."
if BrawlAPI.ShowOKCancelPrompt(msg, "Optimize Stage Textures"):
	# Get parent 2 ARC
	PARENT_ARC = getParentArc()
	
	# Populate lists of used textures, and delete any unused materials
	for node in PARENT_ARC.Children:
		if isinstance(node, BRRESNode):
			parseBrres(node)
	
	# THE PURGE: if a texture in TextureData is not used by any model or pat0, axe it
	for tex0 in tex0List:
		if (not tex0.Name in texturesInMaterialsNamesList) and (not tex0.Name in texturesInPat0NamesList):
			deletedTex0NamesList.append(tex0.Name)
			tex0.Remove()

	matsDeletedCount = len(deletedMatsNamesList)
	tex0DeletedCount = len(deletedTex0NamesList)
	# Print list of deleted tex0 names
	if (not matsDeletedCount) and (not tex0DeletedCount):
		BrawlAPI.ShowMessage("No unused textures or materials found", "Optimize Stage Textures")
	else:
		message = ""
		if matsDeletedCount:
			message += str(matsDeletedCount) + " materials deleted: \n\n"
			for mat in deletedMatsNamesList:
				message += mat + "\n"
			message += "\n\n"
		if tex0DeletedCount:
			message += str(tex0DeletedCount) + " textures deleted: \n\n"
			for tex0 in deletedTex0NamesList:
				message += tex0 + "\n"
			message += "\n\n"
		BrawlAPI.ShowMessage(message, "Optimize Stage Textures")