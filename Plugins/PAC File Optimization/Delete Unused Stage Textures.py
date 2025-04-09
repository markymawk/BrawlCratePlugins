__author__ = "mawwwk"
__version__ = "2.0.3"

from mawwwkLib import *

SCRIPT_NAME = "Delete Unused Stage Textures"
# Relatively safe to use, but WILL break Hanenbow based stages.

def main():
	bytesDeletedCount = 0	# Sum of uncompressed bytes worth of textures deleted
	deletedMatsNamesList = []			# Names of deleted materials (unused by any objects)
	deletedTex0NamesList = []			# Names of deleted tex0 nodes (unused by any material or pat0)
	cullAllMatsNamesList = []
	cullAllMDL0NamesList = []
	tex0NodeList = []
	texturesInMatNamesList = []	# Names of textures used by mats
	texturesInPat0NamesList = []
	
	# Check for intended file structure
	if not BrawlAPI.RootNode.FindChild("2"):
		msg = "2 ARC not found.\nThis script may still be run, but with unintended behavior. Continue?"
		if not BrawlAPI.ShowYesNoDialog(msg, SCRIPT_NAME):
			return
	
	# Confirmation dialog
	startMsg = "Detect and remove unused materials and textures. \n\nTEX0s inside ModelData BRRES nodes are ignored, and must be checked manually.\n\n"
	startMsg += "NOTE: Always check the final results in-game, and save backups!\n\n"
	startMsg += "Only recommended for use with Battlefield, FD, or Palutena-based stages. This WILL break Hanenbow-based stages and potentially stages with other bases."
	
	if not BrawlAPI.ShowOKCancelPrompt(startMsg, SCRIPT_NAME):
		return
	
	brresNodeList = BrawlAPI.NodeListOfType[BRRESNode]()
	
	# Build list of tex0 nodes used in Texture Data brres
	for brresNode in brresNodeList:
		if "Texture Data" in brresNode.Name and brresNode.HasChildren:
			textureGroup = brresNode.FindChild(TEX_GROUP)
			if textureGroup:
				for tex0 in textureGroup.Children:
					tex0NodeList.append(tex0)
		
	tex0NodeList = reverseResourceList(tex0NodeList)
	
	# Populate lists of used textures in Model Data, and also delete any unused materials
	for brresNode in brresNodeList:
		if "Model Data" in brresNode.Name:
			
			# Check 3DModels brres group
			modelsGroup = brresNode.FindChild(MDL_GROUP)
			if modelsGroup:
				
				# Loop through models
				for mdl0 in modelsGroup.Children:
					
					# Check for materials unused by objects
					matsGroup = mdl0.FindChild("Materials")
					if matsGroup:
						for mat in reverseResourceList(matsGroup.Children):
						
							# If not used in any objects, delete the material
							if not len(mat._objects):
								deletedMatsNamesList.append(mat.Name)
								mat.Remove()
							
							# If material set to Cull All, don't delete it, but add to appropriate lists
							elif "Cull_All" in str(mat._cull):
								cullAllMatsNamesList.append(mat.Name)
								cullAllMDL0NamesList.append(mdl0.Parent.Parent.Name + "/" + mdl0.Name)
					
					# In a model, get the Textures folder and populate the list of used textures
					mdl0TexturesGroup = mdl0.FindChild("Textures")
					if mdl0TexturesGroup:
					
						# Loop through texture refs in mdl0
						for texRef in reverseResourceList(mdl0TexturesGroup.Children):
							if texRef.References:
								texturesInMatNamesList.append(texRef.Name)
							
							# If Texture node isn't used by any materials, delete it
							else:
								texRef.Remove()
			# Check PAT0 brres group
			pat0Group = brresNode.FindChild(PAT_GROUP)
			if pat0Group:
				for pat0 in pat0Group.Children:
					for material in pat0.Children:
						for texRef in material.Children:
							# Loop through pat0 frames and append used texture names
							for frame in texRef.Children:
								texturesInPat0NamesList.append(frame.Name)
			
			# Check Textures brres group
			modelDataTexturesGroup = brresNode.FindChild(TEX_GROUP)
			if modelDataTexturesGroup:
				for tex0 in modelDataTexturesGroup.Children:
					# Remove any found ModelData textures from being checked against the "global" TextureData list
					if tex0.Name in texturesInMatNamesList:
						texturesInMatNamesList.remove(tex0.Name)
	
	# If a texture in TextureData is not used by any model or pat0, delete it
	for tex0 in tex0NodeList:
		if not tex0.Name in (texturesInMatNamesList + texturesInPat0NamesList):
			deletedTex0NamesList.append(tex0.Name)
			bytesDeletedCount += tex0.UncompressedSize
			tex0.Remove()
	
	# Results
	matsDeletedCount = len(deletedMatsNamesList)
	tex0DeletedCount = len(deletedTex0NamesList)
	cullAllMatCount = len(cullAllMatsNamesList)
	
	# Print list of deleted tex0 names
	if not matsDeletedCount and not tex0DeletedCount:
		message = "No unused textures or materials detected."
	else:
		message = ""
		
		# Append list of deleted mat names
		if matsDeletedCount:
			message += str(matsDeletedCount) + " materials deleted: \n\n"
			message += listToString(deletedMatsNamesList, 12)
			message += "\n\n"
		
		# Append list of deleted texture names
		if tex0DeletedCount:
			message += str(tex0DeletedCount) + " textures deleted: \n\n"
			message += listToString(deletedTex0NamesList, 12)
			message += "\n\n"
		
		# Include sum of bytes deleted
		if message != "":
			message += "\n" + str(bytesDeletedCount) + " bytes"
	
	BrawlAPI.ShowMessage(message, SCRIPT_NAME)
	
	# List any Cull All mats
	if cullAllMatCount:
		message = "Cull_All materials found:\n\n"
		
		for i in range(cullAllMatCount):
			message += "Model: " + str(cullAllMDL0NamesList[i]) + "\nMaterial: " + str(cullAllMatsNamesList[i]) + "\n\n"
		BrawlAPI.ShowMessage(message, "Possible unused materials found")

main()