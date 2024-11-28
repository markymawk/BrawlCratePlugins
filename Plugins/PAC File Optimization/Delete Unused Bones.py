__author__ = "mawwwk"
__version__ = "1.2"

from BrawlCrate.UI import MainForm
from mawwwkLib import *

## Begin global variables

SCRIPT_NAME = "Delete Unused Model Bones"
MODEL_NAMES_TO_AVOID = ["poketrainer", "hyakunin_", "stgresult"] # Don't delete any bones inside models containing these names

## End global variables
## Begin helper methods

# Return true if model's objects are all single-bound
def isSingleBindModel(model):
	objectsGroup = model.FindChild("Objects")
	if not objectsGroup:
		return True
	for obj in objectsGroup.Children:
		if obj.SingleBind == "(none)":
			return False
	
	return True
	
# Recursively look at bone's children to determine if it's used by any objects or collisions
def checkBone(bone, safeBones):
	
	# Count bones removed in this model
	bonesRemovedCount = 0
	
	# Check this bone's children recursively
	if bone.HasChildren:
		for childBone in getChildNodes(bone):
		
			# Increment count if bone was removed
			bonesRemovedCount += checkBone(childBone, safeBones)
	
	# If bone isn't the last bone, has no children, and isn't used by any objects, delete the bone
	isOnlyBone = isinstance(bone.Parent, MDL0GroupNode) and len(bone.Parent.Children) == 1 and not bone.HasChildren
	hasGeometry = "HasGeometry" in str(bone._boneFlags)
	
	if not isOnlyBone and not (bone.HasChildren or len(bone.VisibilityDrawCalls) or hasGeometry or bone in safeBones):
		removeNode(bone)
		bonesRemovedCount += 1
	
	return bonesRemovedCount
	
## End helper methods
## Start of main script

def main():
	bonesDeletedCount = 0
	safeBones = [] # Collision bones, etc
	modelsModifiedList = []
	nonSingleBindModels = [] # Models that use non-SingleBind objects, and thus are skipped
	
	if not BrawlAPI.RootNode or not BrawlAPI.RootNode.FindChild("2"):
		BrawlAPI.ShowError("2 ARC not found.", SCRIPT_NAME)
		return
	
	# Confirmation prompt message
	START_MSG = "Delete bones in this stage file that aren't used by objects or collisions.\nSave a backup file, and test any edits in-game!\n\nPress OK to continue."

	# Check parent 2 ARC to verify the open file is a stage, and show prompt
	if not BrawlAPI.ShowOKCancelPrompt(START_MSG, SCRIPT_NAME):
		return
	
	# Get list of bone nodes used by collisions
	for obj in BrawlAPI.NodeListOfType[CollisionObject]():
		safeBones.append(obj.LinkedBone)
	
	# Loop through all MDL0s in file
	for mdl0 in BrawlAPI.NodeListOfType[MDL0Node]():
	
		# If model name matches any certain "safe" model, don't delete any bones
		isSafeModel = False
		for safeName in MODEL_NAMES_TO_AVOID:
			if safeName in mdl0.Name.lower():
				isSafeModel = True
		modelBonesGroup = mdl0.FindChild("Bones")
		
		if isSafeModel or mdl0.IsStagePosition or not modelBonesGroup:
			continue
		
		# If parent model has any non-SingleBind objects, assume there is complex rigging and ignore further child bones, to be safe.
		if not isSingleBindModel(mdl0):
			nonSingleBindModels.append(mdl0.Parent.Parent.Name + "/" + mdl0.Name)
			continue
		
		# Get list of bones in current mdl0, using Lib getChildNodes() to avoid deletion errors	
		modelBonesList = getChildNodes(modelBonesGroup)
		
		# Start looping through bones in the mdl0, and delete any unused bones
		for bone in modelBonesList:
			modelBonesDeletedCount = checkBone(bone, safeBones)
			
			# If any bones deleted, append the BRRES name and MDL0 name to modelsModifiedList[]
			if modelBonesDeletedCount:
				modelsModifiedList.append(mdl0.Parent.Parent.Name + "/" + mdl0.Name)
				bonesDeletedCount += modelBonesDeletedCount
	
	# Results
	# If any edits made, list models modified
	if len(modelsModifiedList):
		resultsMsg = str(bonesDeletedCount) + " unused bones found and deleted in:\n" + listToString(modelsModifiedList)
	
	# If no edits made
	else:
		resultsMsg = "No unused bones found."
	
	# If any non-SingleBind models were skipped, list them for clarity
	if len(nonSingleBindModels):
		resultsMsg += "\n\nSkipped " + str(len(nonSingleBindModels)) + " models from having non-SingleBind objects:\n" + listToString(nonSingleBindModels)
	BrawlAPI.ShowMessage(resultsMsg, SCRIPT_NAME)
	
main()
