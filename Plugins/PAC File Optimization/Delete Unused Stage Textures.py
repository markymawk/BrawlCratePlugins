__author__ = "mawwwk"
__version__ = "1.0.2"
# Relatively safe to use, but WILL break Hanenbow based stages.
# Always test in game!!
# Does anyone read the python comments lol
from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from mawwwkLib import *

## Begin global variables

SCRIPT_NAME = "Delete Unused Stage Textures"
texturesInMaterialsNamesList = []	# Names of textures used by mats
texturesInPat0NamesList = []		# Names of textures used in PAT0s
tex0List = []						# Tex0 nodes inside any brres
deletedMatsNamesList = []			# Names of deleted materials (unused by any objects)
deletedTex0NamesList = []			# Names of deleted tex0 nodes (unused by any material or pat0)
cullAllMatsNamesList = []			# Names of any mats set to Cull_All
cullAllMDL0NamesList = []			# Names of any models containing Cull_All mats
unusedNodesModelsNamesList = []		# Names of any MDL0 containing "Regenerated" vertices or normals
sizeCount = 0						# Sum of uncompressed bytes deleted

## End global variables
## Begin helper methods

# point parser to ModelData or TextureData behavior
def parseBrres(node):
	if "Model Data" in node.Name:
		parseModelData(node)
	elif "Texture Data" in node.Name:
		parseTextureData(node)

# Given a ModelData brres, iterate through mdl0 and pat0 to populate used textures lists, then check for any tex0 nodes in the ModelData
def parseModelData(brres):
	modelsGroup = getChildFromName(brres, "3DModels")
	pat0Group = getChildFromName(brres, "AnmTexPat")
	modelDataTexturesGroup = getChildFromName(brres, "Textures(NW4R)")
	
	# Iterate through models to tally the used textures, and remove unused mats
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			texturesGroup = getChildFromName(mdl0, "Textures")
			modelMaterialsGroup = getChildFromName(mdl0, "Materials")
			verticesGroup = getChildFromName(mdl0,"Vertices")
			normalsGroup = getChildFromName(mdl0,"Normals")
			# If the mdl0 has Texture references or Materials, dive in
			if texturesGroup or modelMaterialsGroup or verticesGroup or normalsGroup:
				parseMDL0(mdl0)
	
	# Iterate through pat0s to tally the used textures
	if pat0Group:
		for pat0 in pat0Group.Children:
			parsePAT0(pat0)
	
	# Check for tex0s in ModelData
	# DON'T delete these -- in cases like Smashville, the references are loaded from the module or elsewhere outside the brres
	if modelDataTexturesGroup:
		for tex0 in modelDataTexturesGroup.Children:
			# To simulate locality, delete the textures from "textures used" after logging them
			if tex0.Name in texturesInMaterialsNamesList:
				texturesInMaterialsNamesList.remove(tex0.Name)

# Given a mdl0 node, delete any unused materials, then log any texture references
def parseMDL0(mdl0):
	global sizeCount
	matsGroup = getChildFromName(mdl0, "Materials")
	mdl0TexturesGroup = getChildFromName(mdl0, "Textures")
	verticesGroup = getChildFromName(mdl0, "Vertices")
	normalsGroup = getChildFromName(mdl0, "Normals")
	isUnusedFound = False # Gets set if any unused verts/norms found
	
	# Check for materials not assigned to objects
	if matsGroup:
		
		# Iterate through materials in mdl0
		for m in reverseResourceList(matsGroup.Children):
		
			# If object count == 0, delete the material
			if len(m._objects) == 0:
				deletedMatsNamesList.append(m.Name)
				sizeCount += m.UncompressedSize
				m.Remove()
			
			# If material set to Cull All, don't delete it, but add to appropriate lists
			elif "Cull_All" in str(m._cull):
				cullAllMatsNamesList.append(m.Name)
				cullAllMDL0NamesList.append(mdl0.Parent.Parent.Name + "/" + mdl0.Name)
	
	# In each model, get the "Textures" folder and populate the script's list of used textures
	if mdl0TexturesGroup:
	
		# Iterate through texture references in mdl0, from bottom-up.
		for t in reverseResourceList(mdl0TexturesGroup.Children):
			if t.References:
				texturesInMaterialsNamesList.append(t.Name)
			
			# If Texture node isn't used by any materials, delete it
			else:
				sizeCount += t.UncompressedSize
				t.Remove()

	# Scan for unused vertices or normals not used by any object.
	# If found in the given mdl0, append to unusedNodesModelsNamesList[]
	if verticesGroup:
		for node in verticesGroup.Children:
			if len(node._objects) == 0:
				isUnusedFound = True
				break
	
	# If no unused nodes have been found yet, check Normals
	if normalsGroup and not isUnusedFound:
		for node in normalsGroup.Children:
			if len(node._objects) == 0:
				isUnusedFound = True
				break
	
	if isUnusedFound:
		unusedNodesModelsNamesList.append(mdl0.Parent.Parent.Name + "/" + mdl0.Name)

# Given a pat0 animation, iterate through child entries and log textures used
def parsePAT0(pat0):
	for material in pat0.Children:
		# For texture reference in material
		for texRef in material.Children:
			# Iterate through frames and log texture names
			for frame in texRef.Children:
				texturesInPat0NamesList.append(frame.Name)

# Given a TextureData brres, log any tex0 nodes found, and delete any unused textures
def parseTextureData(brresNode):
	global tex0List
	for tex0 in getChildFromName(brresNode, "Textures(NW4R)").Children:
		tex0List.append(tex0)

## End helper methods
## Start of main script

# Confirmation prompt
msg = "Optimize file size for a stage .pac by auto-detecting and removing unused materials and textures. \n\nTEX0s inside ModelData BRRES are ignored, and must be checked manually.\n\n"
msg += "DISCLAIMER: Always check the final results in-game, and save backups!\n\n"
msg += "Only recommended for use with Battlefield, FD, or Palutena-based stages. This WILL break Hanenbow-based stages!"
PARENT_2_ARC = getParentArc()
# Get parent 2 ARC to verify the open file is a stage
if PARENT_2_ARC and BrawlAPI.ShowOKCancelPrompt(msg, SCRIPT_NAME):
	
	# Populate lists of used textures, and delete any unused materials
	for node in BrawlAPI.NodeListOfType[BRRESNode]():
		parseBrres(node)
	
	# If a texture in TextureData is not used by any model or pat0, delete it
	tex0List = reverseResourceList(tex0List)
	for tex0 in tex0List:
		if not tex0.Name in (texturesInMaterialsNamesList + texturesInPat0NamesList):
			deletedTex0NamesList.append(tex0.Name)
			sizeCount += tex0.UncompressedSize
			tex0.Remove()

	# RESULTS dialog boxes
	
	matsDeletedCount = len(deletedMatsNamesList)
	tex0DeletedCount = len(deletedTex0NamesList)
	CULL_ALL_COUNT = len(cullAllMatsNamesList)
	UNUSED_NODE_MDL0_COUNT = len(unusedNodesModelsNamesList)	# Amount of MDL0 nodes with unused normals/vertices
	
	# Print list of deleted tex0 names
	if not matsDeletedCount and not tex0DeletedCount and not CULL_ALL_COUNT and not UNUSED_NODE_MDL0_COUNT:
		BrawlAPI.ShowMessage("No unused textures or materials detected", SCRIPT_NAME)
	else:
		message = ""
		if matsDeletedCount:
			message += str(matsDeletedCount) + " materials deleted: \n\n"
			
			# Truncate mats list at 10 max, if more than 10
			if matsDeletedCount > 10: 
				for i in range(0,10,1):
					message += deletedMatsNamesList[i] + "\n"
				message += "...and " + str(matsDeletedCount - 10) + " others"
				
			else: # 10 or fewer mats deleted
				for mat in deletedMatsNamesList:
					message += mat + "\n"
			message += "\n\n"
		
		if tex0DeletedCount:
			message += str(tex0DeletedCount) + " textures deleted: \n\n"
			
			if tex0DeletedCount > 10: # Truncate tex0 list at 10 max, if more than 10
				for i in range(0,10,1):
					message += deletedTex0NamesList[i] + "\n"
				message += "...and " + str(tex0DeletedCount - 10) + " others"
			
			else: # 10 or fewer tex0's deleted
				for tex0 in deletedTex0NamesList:
					message += tex0 + "\n"
				message += "\n\n"
		
		if message != "":
			message += "\n\n" + str(sizeCount) + " bytes"
			BrawlAPI.ShowMessage(message, "Deleted Unused Textures")
		
		# List any Cull_all mats
		if CULL_ALL_COUNT > 0:
			message = "Cull_All materials found:\n\n"
			
			for i in range(0, CULL_ALL_COUNT, 1):
				message += "Model: " + str(cullAllMDL0NamesList[i]) + "\nMaterial: " + str(cullAllMatsNamesList[i]) + "\n\n"
			BrawlAPI.ShowMessage(message, "Potential unused materials found")
		
		# List any unused vertex/normals nodes
		if UNUSED_NODE_MDL0_COUNT > 0:
			message = "Unused vertex/normal nodes found:\n\n"
			
			for i in unusedNodesModelsNamesList:
				message += i + "\n"
			BrawlAPI.ShowMessage(message, "Unused nodes found")