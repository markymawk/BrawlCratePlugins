__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.Internal import * # Vector3 etc
from mawwwkLib import *

# Verify that any textures whose resolution isn't
# a power of 2 are using Clamp wrap setting in their materials
SCRIPT_NAME = "Check UV Wrap Settings"
VALID_TEXTURE_RES = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]

def main():
	startMsg = "Check if all materials using non-power-of-2 textures are correctly set to Clamp.\n"
	startMsg += "Incorrect wrap settings for these materials will cause rendering issues on console.\n\n"
	startMsg += "Press OK to continue."
	
	if not BrawlAPI.ShowOKCancelPrompt(startMsg, SCRIPT_NAME):
		return
	textureNamesToCheck = []
	
	# Get list of textures to check
	for tex0 in BrawlAPI.NodeListOfType[TEX0Node]():
		if tex0.Width not in VALID_TEXTURE_RES \
		or tex0.Height not in VALID_TEXTURE_RES:
			textureNamesToCheck.append(tex0.Name)
	
	# If all textures are powers of 2, quit
	if not len(textureNamesToCheck):
		BrawlAPI.ShowMessage("All textures in this file use powers of 2.", SCRIPT_NAME)
		return
	
	# Get list of materials used by these textures
	matRefsToCheck = []
	badMaterialWraps = []
	for mat in BrawlAPI.NodeListOfType[MDL0MaterialNode]():
		# Skip mats with no tex refs
		if not mat.HasChildren:
			continue
		
		for matRef in mat.Children:
			for badTex in textureNamesToCheck:
				
				# If texture found and not set to Clamp, add to list
				if badTex == matRef.Name and (matRef.UWrapMode != MatWrapMode.Clamp or matRef.VWrapMode != MatWrapMode.Clamp):
					badMaterialWraps.append(matRef)
	
	# If all materials are using Clamp as needed, quit
	if not len(badMaterialWraps):
		BrawlAPI.ShowMessage("No incorrect wrap mode settings found for the following textures:\n\n" + listToString(textureNamesToCheck), SCRIPT_NAME)
		return
	
	# If materials use incorrect wrap, prompt to auto set them
	msg = "The following material refs are not set to Clamp UVs:\n\n"
	for matRef in badMaterialWraps:
		mat = matRef.Parent
		mdl0 = mat.Parent.Parent
		brres = mdl0.Parent.Parent
		msg += brres.Name + "/" + mdl0.Name + "/" + mat.Name + ": " + matRef.Name
	msg += "\n\nSet these to Clamp now?"
	
	# If not auto-setting any materials, quit
	if not BrawlAPI.ShowYesNoError(msg, "Incorrect wrap mode settings found"):
		return
	
	# Set to Clamp
	for matRef in badMaterialWraps:
		matRef.UWrapMode = MatWrapMode.Clamp
		matRef.VWrapMode = MatWrapMode.Clamp
	
	badMatCount = str(len(badMaterialWraps))
	BrawlAPI.ShowMessage(badMatCount + " material(s) wrap mode set to Clamp.", SCRIPT_NAME)

main()
