__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from mawwwkLib import *

# Verify that any textures whose resolution isn't
# a power of 2 are using Clamp wrap setting in their materials
SCRIPT_NAME = "Check UV Wrap Settings"
VALID_TEXTURE_RES = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

def main():
	startMsg = "Check if all materials using non-power-of-2 textures are correctly set to Clamp.\n" + \
	"Incorrect wrap settings for these materials will cause rendering issues on console.\n\n" + \
	"Press OK to continue."
	
	if not BrawlAPI.ShowOKCancelPrompt(startMsg, SCRIPT_NAME):
		return
	textureNamesToCheck_Width = []
	textureNamesToCheck_Height = []
	
	# Get list of textures to check
	for tex0 in BrawlAPI.NodeListOfType[TEX0Node]():
		if tex0.Width not in VALID_TEXTURE_RES:
			textureNamesToCheck_Width.append(tex0.Name)
		if tex0.Height not in VALID_TEXTURE_RES:
			textureNamesToCheck_Height.append(tex0.Name)

	# If all textures are powers of 2, quit
	if not len(textureNamesToCheck_Width + textureNamesToCheck_Height):
		BrawlAPI.ShowMessage("All textures in this file use powers of 2.", SCRIPT_NAME)
		return
	
	# Get list of materials used by these textures
	badMaterialWraps_U = []
	badMaterialWraps_V = []
	badMaterialRefs = []
	for mat in BrawlAPI.NodeListOfType[MDL0MaterialNode]():
		
		# Skip mats with no tex refs
		if not mat.HasChildren:
			continue
		
		for matRef in mat.Children:
			badMat = False
			
			# Check Height / UWrapMode
			for badTex in textureNamesToCheck_Width:
				
				# If texture found and not set to Clamp, add to list
				if badTex == matRef.Name and matRef.UWrapMode != MatWrapMode.Clamp:
					badMaterialWraps_U.append(matRef)
					badMat = True
				
			# Check Width / VWrapMode
			for badTex in textureNamesToCheck_Height:
				# If texture found and not set to Clamp, add to list
				if badTex == matRef.Name and matRef.VWrapMode != MatWrapMode.Clamp:
					badMaterialWraps_V.append(matRef)
					badMat = True
			
			if badMat:
				badMaterialRefs.append(matRef)
				
	# If all materials are using Clamp as needed, quit
	maxListItems = 15
	
	if not len(badMaterialRefs):
		msg = "No incorrect wrap mode settings found for the following textures:\n\n" + \
		listToStringNoDuplicates(textureNamesToCheck_Height + textureNamesToCheck_Width, maxListItems)
		
		BrawlAPI.ShowMessage(msg, SCRIPT_NAME)
		return
	
	# If materials use incorrect wrap, prompt to auto set them
	formattedBadMats = []
	
	for matRef in badMaterialRefs:
		mat = matRef.Parent
		mdl0 = mat.Parent.Parent
		brres = mdl0.Parent.Parent
		formattedBadMats.append(brres.Name + "/" + mdl0.Name + "/" + mat.Name + ": " + matRef.Name)
	
	msg = "The following material refs are not set to Clamp UVs:\n\n"
	msg += listToString(formattedBadMats, maxListItems)
	msg += "\nSet these to Clamp now?"
	
	# If not auto-setting any materials, quit
	if not BrawlAPI.ShowYesNoError(msg, SCRIPT_NAME):
		return
	
	# Set to Clamp
	for matRef in badMaterialWraps_U:
		matRef.UWrapMode = MatWrapMode.Clamp
	for matRef in badMaterialWraps_V:
		matRef.VWrapMode = MatWrapMode.Clamp
	
	badMatCount = str(len(badMaterialRefs))
	BrawlAPI.ShowMessage(badMatCount + " material(s) wrap mode settings changed to Clamp.", SCRIPT_NAME)

main()
