__author__ = "mawwwk"
__version__ = "1.0.1"

# Always test in-game!! always save backups!!

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from mawwwkLib import *

## Begin global variables

SCRIPT_NAME = "Delete Unused Animation Data"
bonesToDelete = []		# Bone targets for CHR, VIS animations
matsToDelete = []		# Material targets for SRT, CLR, PAT animations
affectedAnimNames = []	# Formatted names containing brres name, anim type, and anim name
affectedAnims = []		# Animation node
brresBoneNameList = []		# Global list populated per-brres
sizeCount = 0				# Size of deleted nodes, in uncompressed bytes

## End global variables
## Begin helper methods

# Given a CHR or VIS animation, parse the parent BRRES for bone usage
def checkForBones(anim):
	if anim.Children and anim.Parent and anim.Parent.Parent:
		
		parentBRRES = anim.Parent.Parent
		
		if "Model Data" in parentBRRES.Name:
			global brresBoneNameList
			global sizeCount
			
			getBoneListFromBRRES(parentBRRES)
			
			
			for bone in anim.Children:
				if not bone.Name in brresBoneNameList:
					bonesToDelete.append(bone)
					affectedAnims.append(anim)
					sizeCount += bone.UncompressedSize
					
					animType = str(type(anim))[7:11]
					affectedAnimNames.append(parentBRRES.Name + "/" + animType + " " + anim.Name + "/" + bone.Name)

def checkForMats(anim):
	if anim.Children:
		global sizeCount
		parentBRRES = anim.Parent.Parent
		
		if "Model Data" in parentBRRES.Name:
			brresMatList = getMatListFromBRRES(parentBRRES)
			
			for mat in anim.Children:
				if not mat.Name in brresMatList:
					matsToDelete.append(mat)
					affectedAnims.append(anim)
					sizeCount += mat.UncompressedSize
					
					animType = str(type(anim))[7:11]
					affectedAnimNames.append(parentBRRES.Name + "/" + animType + " " + anim.Name + "/" + mat.Name)

# Return list of material names in models in this brres
def getMatListFromBRRES(brres):
	modelsGroup = getChildFromName(brres, "3DModels")
	brresMatList = []
	
	# If no models, return none
	if modelsGroup:
		
		for mdl0 in modelsGroup.Children:
			materialsGroup = getChildFromName(mdl0, "Materials")

			if materialsGroup:
				for mat in materialsGroup.Children:
					brresMatList.append(mat.Name)
	
	return brresMatList

# Return list of bone names in models in this brres
def getBoneListFromBRRES(brres):
	global brresBoneNameList
	brresBoneNameList = []
	modelsGroup = getChildFromName(brres, "3DModels")
	
	if "Model Data" in brres.Name and modelsGroup:
		# Start with an empty list, and populate it with each model's bone list
		for mdl0 in modelsGroup.Children:
			bonesGroup = getChildFromName(mdl0, "Bones")
			
			if bonesGroup:
				for b in bonesGroup.Children:
					populateBonesList(b)
					
def populateBonesList(bone):
	brresBoneNameList.append(bone.Name)
	
	if bone.HasChildren:
		for childBone in bone.Children:
			populateBonesList(childBone)

## End helper methods
## Start of main script

# Confirmation prompt
message = "Detect and remove any unused bone or material references within stage animations.\n\n"
message += "DISCLAIMER: Always check the final results in-game.\nNot recommended for Green Hill Zone, Green Greens/Dream Land, or other module-animation-dependent stages.\n"

if BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
	global deletedNodeCount
	
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
	# Iterate through MDL0 nodes
	
	if not len(affectedAnims):
		BrawlAPI.ShowMessage("No unused animation data found", SCRIPT_NAME)
	# Show results
	else:
		message = "Unused data found in:\n\n"
		MAX_LIST = 20
		
		# If more than maximum entries, truncate the list
		if len(affectedAnimNames) > MAX_LIST:
			for i in range(0, MAX_LIST, 1):
				message += affectedAnimNames[i] + "\n"
			message += "...and " + str((len(affectedAnimNames) - MAX_LIST)) + " more\n"
		else:
			for anim in affectedAnimNames:
				message += anim + "\n"
		
		message += "\n" + str(sizeCount) + " bytes\nDelete these references?"
		
		if BrawlAPI.ShowYesNoPrompt(message, SCRIPT_NAME):
			for mat in matsToDelete:
				mat.Remove()
			for bone in bonesToDelete:
				bone.Remove()
				
			## In cases like GHZ, the animation might need to exist?
			
			#for anim in affectedAnims:	
			#	if not anim.HasChildren:
			#		anim.Remove()
