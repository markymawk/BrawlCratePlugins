__author__ = "mawwwk"
__version__ = "1.0"

from mawwwkLib import *
from BrawlCrate.API.BrawlAPI import AppPath

SCRIPT_NAME = "Optimize TShadow1 TEX0"

SHADOW_TEX0_PATH = AppPath + "\\BrawlAPI\\Resources\\TShadow1.tex0"
NEW_SHADOW_HASH = "2571A42D"

def main():
	# Don't run if 2 ARC doesn't exist
	if not (BrawlAPI.RootNode and BrawlAPI.RootNode.HasChildren and BrawlAPI.RootNode.FindChild("2")):
		BrawlAPI.ShowError("No 2 ARC found", SCRIPT_NAME)
		return
	
	# Get parent 2 ARC
	parentArc = BrawlAPI.RootNode.FindChild("2")
	
	isShadowFound = False
	newShadowAlreadyExists = False
	duplicateShadowTEX0 = []
	affectedBRRESName = ""
	
	for brres in parentArc.Children:
		if not isinstance(brres, BRRESNode):
			continue
		# Find Texture Data nodes with textures
		if "Texture Data" not in brres.Name:
			continue
		if not brres.HasChildren:
			continue
		
		textureGroup = brres.FindChild(TEX_GROUP)
		
		if not textureGroup:
			continue
		
		# Loop through textures in Texture Data
		for tex0 in textureGroup.Children:
		
			# If TShadow1 texture found, check it
			if tex0.Name == "TShadow1":
			
				# If a duplicate Shadow texture, add to list and continue
				if isShadowFound:
					duplicateShadowTEX0.append(tex0)
				
				# Otherwise, check if hash matches that of a blank texture before replacing
				else:
					isShadowFound = True
					oldHash = tex0.MD5Str()[:8]
					
					# If hash matches, don't replace
					if oldHash == NEW_SHADOW_HASH:
						newShadowAlreadyExists = True
					
					# If hash doesn't match, replace from Resources dir
					else:
						tex0.Replace(SHADOW_TEX0_PATH)
						affectedBRRESName = tex0.Parent.Parent.Name
	
	# Results
	resultsMsg = ""
	if newShadowAlreadyExists:
		resultsMsg += "Black TShadow1 texture already in file. No changes made"
	elif isShadowFound:
		resultsMsg += "TShadow1 texture updated in " + affectedBRRESName
	else:
		resultsMsg += "No TShadow1 texture found in file"
	BrawlAPI.ShowMessage(resultsMsg, SCRIPT_NAME)
	
	# If duplicate TShadow textures found, prompt to remove them
	if len(duplicateShadowTEX0):
		msg = "Duplicate TShadow1 textures found.\nDelete duplicates?"
		
		# Loop through duplicates and remove
		if BrawlAPI.ShowYesNoWarning(msg, SCRIPT_NAME):
			for tex0 in duplicateShadowTEX0:
				tex0.Remove()
main()
