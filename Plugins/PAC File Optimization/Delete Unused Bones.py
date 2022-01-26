__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from mawwwkLib import *

## Begin global variables

SCRIPT_NAME = "Delete Unused Model Bones"
MODEL_NAMES_TO_AVOID = ["PokeTrainer", "hyakunin_"] # Don't delete any bones inside models containing these names

## End global variables
## Begin helper methods

# Return true if model uses only SingleBind objects
def isSingleBindModel(model):
	objectsGroup = getChildFromName(model,"Objects")
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
	
	if not isOnlyBone and not (bone.HasChildren or hasGeometry or bone in safeBones):
		removeNode(bone)
		bonesRemovedCount += 1
	
	return bonesRemovedCount
	
## End helper methods
## Start of main script

def main():
	bonesDeletedCount = 0
	collisionBones = []
	modelsModifiedList = []
	nonSingleBindModels = [] # Models that use non-SingleBind objects, and thus are skipped
	
	# Confirmation prompt message
	msg = "Delete bones in this model that aren't used by objects or collisions.\nSave a backup file, and test any edits in-game!\n\nPress OK to continue."

	# Check parent 2 ARC to verify the open file is a stage, and show prompt
	if not getParentArc() or not showMsg(msg, SCRIPT_NAME, 1):
		return
	
	# Get list of bone nodes used by collisions
	for obj in BrawlAPI.NodeListOfType[CollisionObject]():
		collisionBones.append(obj.LinkedBone)
	
	# Loop through all MDL0s in file
	for model in BrawlAPI.NodeListOfType[MDL0Node]():
	
		# If model name matches a defined subset, don't delete any bones
		modelNameToAvoid = False
		for name in MODEL_NAMES_TO_AVOID:
			if name.lower() in model.Name.lower():
				modelNameToAvoid = True
				break
		
		# Move onto the next model if model name's ineligible, or model uses non-SingleBind objects
		if modelNameToAvoid or model.IsStagePosition:
			continue
		
		# If parent model has any non-SingleBind objects, assume there is complex rigging and ignore further child bones, to be safe.
		if not isSingleBindModel(model):
			nonSingleBindModels.append(model.Parent.Parent.Name + "/" + model.Name)
			continue
		
		# Get selected node, and quit script if no bones exist
		modelBonesGroup = getChildFromName(model, "Bones")
		if not modelBonesGroup:
			return
		
		# Get list of bones in current mdl0, using mawwwkLib.getChildNodes() to avoid deletion errors	
		modelBonesList = getChildNodes(modelBonesGroup)
		
		# Start iterating through bones in the mdl0, and delete any unused bones
		for bone in modelBonesList:
			modelBonesDeletedCount = checkBone(bone, collisionBones)
			
			# If any bones deleted, append the BRRES name and MDL0 name to modelsModifiedList[]
			if modelBonesDeletedCount:
				modelsModifiedList.append(model.Parent.Parent.Name + "/" + model.Name)
				bonesDeletedCount += modelBonesDeletedCount
	
	# Results
	msg = ""
	# If any edits made, list models modified
	if len(modelsModifiedList):
		msg += str(bonesDeletedCount) + " unused bones found and deleted in:\n" + listToString(modelsModifiedList)
	
	# If no edits made
	else:
		msg += "No unused bones found."
	
	# If any non-SingleBind models were skipped, list them for clarity
	if len(nonSingleBindModels):
		msg += "\n\nSkipped " + str(len(nonSingleBindModels)) + " models from having non-SingleBind objects:\n" + listToString(nonSingleBindModels)
	showMsg(msg, SCRIPT_NAME)
	
main()
