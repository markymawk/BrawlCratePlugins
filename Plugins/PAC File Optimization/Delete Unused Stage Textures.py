__author__ = "mawwwk"
__version__ = "1.0.3"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from mawwwkLib import *

# Relatively safe to use, but WILL break Hanenbow based stages.
## Begin global variables

SCRIPT_NAME = "Locate Unused Stage Textures"
texturesInMaterialsNamesList = []	# Names of textures used by mats
texturesInPat0NamesList = []		# Names of textures used in PAT0s
tex0List = []						# Tex0 nodes inside any brres
deletedMatsNamesList = []			# Names of deleted materials (unused by any objects)
deletedTex0NamesList = []			# Names of deleted tex0 nodes (unused by any material or pat0)
cullAllMatsNamesList = []
cullAllMDL0NamesList = []
sizeCount = 0						# Sum of uncompressed bytes deleted

## End global variables
## Begin helper methods

# point parser to ModelData or TextureData behavior
def checkBrres(node):
	if "Model Data" in node.Name:
		checkModelData(node)
	elif "Texture Data" in node.Name:
		checkTextureData(node)

# Given a ModelData brres, loop through mdl0 and pat0 to populate used textures lists, then check for any tex0 nodes in the ModelData
def checkModelData(brresNode):
	modelsGroup = brresNode.FindChild("3DModels(NW4R)")
	pat0Group = brresNode.FindChild("AnmTexPat(NW4R)")
	modelDataTexturesGroup = brresNode.FindChild("Textures(NW4R)")
	
	# Loop through models to tally used textures, and remove unused mats
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			texturesGroup = mdl0.FindChild("Textures")
			modelMaterialsGroup = mdl0.FindChild("Materials")
			# If the mdl0 has Texture references or Materials, dive in
			if texturesGroup or modelMaterialsGroup:
				checkMDL0(mdl0)
	
	# Loop through pat0s to tally the used textures
	if pat0Group:
		for pat0 in pat0Group.Children:
			checkPAT0(pat0)
	
	# Check for tex0s in ModelData
	# DON'T delete these -- in cases like Smashville, the references are loaded from the module or elsewhere outside the brres
	if modelDataTexturesGroup:
		for tex0 in modelDataTexturesGroup.Children:
			# To simulate locality, delete the textures from "textures used" after logging them
			if tex0.Name in texturesInMaterialsNamesList:
				texturesInMaterialsNamesList.remove(tex0.Name)

# Given a mdl0 node, delete any unused materials, then log any texture references
def checkMDL0(mdl0):
	global sizeCount
	matsGroup = mdl0.FindChild("Materials")
	mdl0TexturesGroup = mdl0.FindChild("Textures")
	
	# Check for materials not assigned to objects
	if matsGroup:
		
		# Loop through materials in mdl0
		for m in reverseResourceList(matsGroup.Children):
		
			# If not used in any objects, delete the material
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
	
		# Loop through texture refs in mdl0
		for texRef in reverseResourceList(mdl0TexturesGroup.Children):
			if texRef.References:
				texturesInMaterialsNamesList.append(texRef.Name)
			
			# If Texture node isn't used by any materials, delete it
			else:
				sizeCount += texRef.UncompressedSize
				texRef.Remove()

# Given a pat0 animation, loop through child entries and log textures used
def checkPAT0(pat0):
	for material in pat0.Children:
		for texRef in material.Children:
			# Loop through pat0 frames and log texture names
			for frame in texRef.Children:
				texturesInPat0NamesList.append(frame.Name)

# Given a TextureData brres, log any tex0 nodes found, and delete any unused textures
def checkTextureData(brresNode):
	global tex0List
	if not brresNode.HasChildren:
		return
	for tex0 in brresNode.FindChild("Textures(NW4R)").Children:
		tex0List.append(tex0)

## End helper methods
## Start of main script

# Confirmation prompt
def main():
	global tex0List
	global sizeCount
	msg = "Detect and remove unused materials and textures. \n\nTEX0s inside ModelData BRRES are ignored, and must be checked manually.\n\n"
	msg += "NOTE: Always check the final results in-game, and save backups!\n\n"
	msg += "Only recommended for use with Battlefield, FD, or Palutena-based stages. This WILL break Hanenbow-based stages and potentially stages with other bases."
	PARENT_2_ARC = getParentArc()
	
	# Get parent 2 ARC to verify the open file is a stage
	if not (PARENT_2_ARC or BrawlAPI.ShowOKCancelPrompt(msg, SCRIPT_NAME)):
		return
	
	# Populate lists of used textures, and delete any unused materials
	for brresNode in BrawlAPI.NodeListOfType[BRRESNode]():
		checkBrres(brresNode)
	
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
	cullAllMatCount = len(cullAllMatsNamesList)
	
	# Print list of deleted tex0 names
	if not matsDeletedCount and not tex0DeletedCount and not cullAllMatCount:
		BrawlAPI.ShowMessage("No unused textures or materials detected", SCRIPT_NAME)
	else:
		message = ""
		if matsDeletedCount:
			message += str(matsDeletedCount) + " materials deleted: \n\n"
			message += listToString(deletedMatsNamesList, 10)
			message += "\n\n"
		
		if tex0DeletedCount:
			message += str(tex0DeletedCount) + " textures deleted: \n\n"
			message += listToString(deletedTex0NamesList, 10)
			message += "\n\n"
		
		if message != "":
			message += "\n\n" + str(sizeCount) + " bytes"
			BrawlAPI.ShowMessage(message, "Deleted Unused Textures")
		
		# List any Cull_all mats
		if cullAllMatCount > 0:
			message = "Cull_All materials found:\n\n"
			
			for i in range(0, cullAllMatCount, 1):
				message += "Model: " + str(cullAllMDL0NamesList[i]) + "\nMaterial: " + str(cullAllMatsNamesList[i]) + "\n\n"
			BrawlAPI.ShowMessage(message, "Potential unused materials found")

main()