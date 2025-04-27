__author__ = "mawwwk"
__version__ = "1.1"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from mawwwkLib import *

## Begin global variables

SCRIPT_NAME = "Delete Unused Animation Data"
bonesToDelete = []		# Bone targets for CHR, VIS animations
matsToDelete = []		# Material targets for SRT, CLR, PAT animations
affectedAnimNames = []	# Formatted names containing brres name, anim type, and anim name
affectedAnims = []		# Animation node
sizeCount = 0				# Size of deleted nodes, in uncompressed bytes

## End global variables
## Begin helper methods

# Given a CHR or VIS animation, parse the parent BRRES for bone usage
def checkForBones(anim):
	if anim.Children and anim.Parent and anim.Parent.Parent:
		global sizeCount
		parentBRRES = anim.Parent.Parent
		
		if isinstance(parentBRRES, BRRESNode):
			brresBoneNameList = getBoneListFromBRRES(parentBRRES)
			
			for animEntry in anim.Children:
				if not animEntry.Name in brresBoneNameList:
					bonesToDelete.append(animEntry)
					affectedAnims.append(anim)
					sizeCount += animEntry.UncompressedSize
					
					animType = anim.Tag
					affectedAnimNames.append(parentBRRES.Name + "/" + animType + " " + anim.Name + "/" + animEntry.Name)

def checkForMats(anim):
	if anim.Children and anim.Parent and anim.Parent.Parent:
		global sizeCount
		parentBRRES = anim.Parent.Parent
		
		if isinstance(parentBRRES, BRRESNode):
			brresMatList = getMatListFromBRRES(parentBRRES)
			
			for animEntry in anim.Children:
				if not animEntry.Name in brresMatList:
					matsToDelete.append(animEntry)
					affectedAnims.append(anim)
					sizeCount += animEntry.UncompressedSize
					
					animType = anim.Tag
					affectedAnimNames.append(parentBRRES.Name + "/" + animType + " " + anim.Name + "/" + animEntry.Name)

# Return list of material names in models in this brres
def getMatListFromBRRES(brres):
	modelsGroup = brres.FindChild(MDL_GROUP)
	brresMatList = []
	
	# If no models, return none
	if modelsGroup:
		
		for mdl0 in modelsGroup.Children:
			materialsGroup = mdl0.FindChild("Materials")

			if materialsGroup:
				for mat in materialsGroup.Children:
					brresMatList.append(mat.Name)
	
	return brresMatList

# Return list of bone names in models in this brres
def getBoneListFromBRRES(brres):
	brresBoneNameList = []
	modelsGroup = brres.FindChild(MDL_GROUP)
	
	# Add bone names to list
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			bonesGroup = mdl0.FindChild("Bones")
			if bonesGroup:
				for bone in bonesGroup.GetChildrenRecursive():
					brresBoneNameList.append(bone.Name)
	
	return brresBoneNameList

## End helper methods
## Start of main script

# Confirmation prompt
def main():
	START_MSG = "Detect and remove any unused bone or material references within stage animations.\n\n"
	START_MSG += "DISCLAIMER: Always check the final results in-game.\nNot recommended for Green Hill Zone, Green Greens/Dream Land, or other module-animation-dependent stages.\n"

	if not BrawlAPI.ShowOKCancelPrompt(START_MSG, SCRIPT_NAME):
		return
	
	# Start with CHR and VIS bones
	for anim in BrawlAPI.NodeListOfType[CHR0Node]():
		checkForBones(anim)
	for anim in BrawlAPI.NodeListOfType[VIS0Node]():
		checkForBones(anim)
	for anim in BrawlAPI.NodeListOfType[CLR0Node]():
		checkForMats(anim)
	for anim in BrawlAPI.NodeListOfType[SRT0Node]():
		checkForMats(anim)
	for anim in BrawlAPI.NodeListOfType[PAT0Node]():
		checkForMats(anim)
	
	# Results
	if len(affectedAnims):
		message = "Unused data found in:\n\n"
		message += listToString(affectedAnimNames, 20)
		message += "\n\n" + str(sizeCount) + " bytes\nDelete these references?"
		
		if BrawlAPI.ShowYesNoPrompt(message, SCRIPT_NAME):
			for mat in matsToDelete:
				mat.Remove()
			for bone in bonesToDelete:
				bone.Remove()
	else:
		BrawlAPI.ShowMessage("No unused animation data found", SCRIPT_NAME)

main()