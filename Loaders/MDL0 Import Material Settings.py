__author__ = "mawwwk"
__version__ = "1.3"

from System.Windows.Forms import ToolStripMenuItem # Needed for all loaders
from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from mawwwkLib import *

## Start enable check functions
# Wrapper: MDL0Wrapper
def EnableCheck(sender, event_args):
	node = BrawlAPI.SelectedNode
	matsGroup = getChildFromName(node, "Materials")
	shadersGroup = getChildFromName(node, "Shaders")
	sender.Enabled = (node is not None and node.HasChildren and matsGroup and shadersGroup)

## End enable check functions
## Start loader functions

def import_model_settings(sender, event_args):

	# "Dest model" refers to the existing, selected mdl0 whose mats/shaders are being replaced
	DEST_MODEL = BrawlAPI.SelectedNode
	DEST_MODEL_WRAPPER = BrawlAPI.SelectedNodeWrapper
	PARENT_MODELS_GROUP = BrawlAPI.SelectedNode.Parent
	DEST_MODEL_MAT_GROUP = getChildFromName(DEST_MODEL, "Materials")
	DEST_MODEL_SHADERS = getChildFromName(DEST_MODEL, "Shaders").Children
	DEST_MODEL_OBJ_GROUP = getChildFromName(DEST_MODEL, "Objects")
	
	# Count number of models to later determine if one should be deleted
	ORIGINAL_MODEL_COUNT = len(DEST_MODEL.Parent.Children)
	
	# Import temporary external MDL0
	BrawlAPI.SelectedNodeWrapper.Parent.Parent.ImportModel()
	
	# "Source model" refers to the imported model from which settings are being imported
	SOURCE_MODEL_INDEX = len(PARENT_MODELS_GROUP.Children)-1
	SOURCE_MODEL = DEST_MODEL.Parent.Children[SOURCE_MODEL_INDEX]
	SOURCE_MODEL_MAT_GROUP = getChildFromName(SOURCE_MODEL, "Materials")
	SOURCE_MODEL_SHADERS = getChildFromName(SOURCE_MODEL, "Shaders").Children
	SOURCE_MODEL_OBJ_GROUP = getChildFromName(SOURCE_MODEL, "Objects")
	
	# If a model wasn't imported (i.e. window closed), terminate the script
	if (ORIGINAL_MODEL_COUNT == len(DEST_MODEL.Parent.Children)):
		return
	
	# Start shader import
	# If dest model has fewer shaders than source model, add more to dest model until the amount of shaders in each mdl0 is equal
	DEST_SHADER_COUNT = len(DEST_MODEL_SHADERS)
	SOURCE_SHADER_COUNT = len(SOURCE_MODEL_SHADERS)
	
	while DEST_SHADER_COUNT < SOURCE_SHADER_COUNT:
		DEST_MODEL_WRAPPER.NewShader()
		DEST_SHADER_COUNT += 1
		
	# For each shader in dest group, replace it with corresponding source shader
	for i in range(0, DEST_SHADER_COUNT, 1):
		sourceShader = SOURCE_MODEL_SHADERS[i]
		destShader = DEST_MODEL_SHADERS[i]
		
		destShader.Replace(sourceShader)
	
	# End shader import
	# Begin material import
	
	sourceMatsList = getChildNodes(SOURCE_MODEL_MAT_GROUP)
	
	# Replace materials that share names
	for destMat in DEST_MODEL_MAT_GROUP.Children:
		sourceMat = getChildFromName(SOURCE_MODEL_MAT_GROUP, destMat.Name, True)
		
		# If material exists in source model, assign it to dest model
		if sourceMat:
			destMat.Replace(sourceMat)
			sourceMatsList.remove(sourceMat)
			destMat.Shader = sourceMat.Shader
	
	# Copy any remaining materials (those that don't share names)
	for sourceMat in sourceMatsList:
		newMat = DEST_MODEL_WRAPPER.NewMaterial()
		newMat.Replace(sourceMat)
		newMat.Name = sourceMat.Name
	
	# End material import
	# Begin object transparency settings
	
	for destObj in DEST_MODEL_OBJ_GROUP.Children:
		sourceObj = getChildFromName(SOURCE_MODEL_OBJ_GROUP, destObj.Name)
		
		# Copy draw pass settings (XLU/OBJ) to each object
		if sourceObj:
			destObj._drawCalls[0].DrawPass = sourceObj._drawCalls[0].DrawPass
	
	# Delete temp mdl0 
	removeNode(SOURCE_MODEL)
	
	# Select destination mdl0 node again
	DEST_MODEL.Parent.SelectChildAtIndex(DEST_MODEL.Index)
	
	# Number of materials imported that aren't assigned to any objects -- may be incorrectly assigned or unused
	EMPTY_MATS_COUNT = len(sourceMatsList)
	
	message = "Materials and shaders imported successfully!"
	
	if EMPTY_MATS_COUNT:
		message += "\n\n" + str(EMPTY_MATS_COUNT) + " materials unassigned to objects (may be incorrectly assigned, or unused)"
		
	BrawlAPI.ShowMessage(message, "Success")

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Import materials and shaders from an external MDL0 file", EnableCheck, ToolStripMenuItem("Import materials and shaders from...", None, import_model_settings))
