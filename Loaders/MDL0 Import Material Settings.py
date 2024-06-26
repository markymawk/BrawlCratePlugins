__author__ = "mawwwk"
__version__ = "1.4"

from System.Windows.Forms import ToolStripMenuItem # Needed for all loaders
from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from mawwwkLib import *

SCRIPT_NAME = "Import Material Settings"

## Start enable check functions
# Wrapper: MDL0Wrapper
def EnableCheck(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and node.FindChild("Materials") and node.FindChild("Shaders")

## End enable check functions
## Start loader functions

def import_model_settings(sender, event_args):
	
	# "Destination" model refers to the existing, selected mdl0 whose mats/shaders are being replaced
	selNode = BrawlAPI.SelectedNode
	selNodeWrapper = BrawlAPI.SelectedNodeWrapper
	destination_MatGroup = selNode.FindChild("Materials") 
	destination_Shaders = selNode.FindChild("Shaders")
	destination_Objects = selNode.FindChild("Objects")
	
	# Count number of models pre-import to later ensure one was added
	startingModelCount = len(selNode.Parent.Children)
	
	# Import temporary external MDL0
	BrawlAPI.SelectedNodeWrapper.Parent.Parent.ImportModel()
	
	# "Source model" refers to the imported model from which settings are being imported
	sourceModelIndex = len(BrawlAPI.SelectedNode.Parent.Children)-1
	sourceModel = selNode.Parent.Children[sourceModelIndex]
	source_MatGroup = sourceModel.FindChild("Materials")
	source_Shaders = sourceModel.FindChild("Shaders")
	source_Objects = sourceModel.FindChild("Objects")
	
	# If number of models is unchanged (i.e. window closed), terminate the script
	if (startingModelCount == len(selNode.Parent.Children)):
		return
	
	# Start shader import
	dest_ShaderCount = len(destination_Shaders.Children)
	source_ShaderCount = len(source_Shaders.Children)
	
	# If destination model has more shaders than the imported model, don't add more (mostly an error check, this usually shouldn't happen)
	if source_ShaderCount < dest_ShaderCount:
		BrawlAPI.ShowWarning("Source model has more shaders than selected model.\nSome shaders may be unaffected.", SCRIPT_NAME)
		dest_ShaderCount = source_ShaderCount
	# If dest model has fewer shaders than source model, add shaders to the destination model until the amount of shaders is equal between each
	else:
		while dest_ShaderCount < source_ShaderCount:
			selNodeWrapper.NewShader()
			dest_ShaderCount += 1
	
	# For each shader in dest group, replace it with corresponding source shader
	for i in range(dest_ShaderCount):
		sourceShader = source_Shaders.Children[i]
		destShader = destination_Shaders.Children[i]
		
		destShader.Replace(sourceShader)
	
	# End shader import
	# Begin material import
	sourceMatsList = getChildNodes(source_MatGroup)
	
	# Replace materials that share names
	for destMat in destination_MatGroup.Children:
		sourceMat = source_MatGroup.FindChild(destMat.Name)
		
		# If material exists in source model, assign it to dest model
		if sourceMat:
			destMat.Replace(sourceMat)
			sourceMatsList.remove(sourceMat)
			destMat.Shader = sourceMat.Shader
	
	# Copy any remaining materials (those that don't share names)
	for sourceMat in sourceMatsList:
		newMat = selNodeWrapper.NewMaterial()
		newMat.Replace(sourceMat)
		newMat.Name = sourceMat.Name
	
	# End material import
	# Begin object DrawPass setings (transparency, etc.)
	for destObj in destination_Objects.Children:
		sourceObj = source_Objects.FindChild(destObj.Name)
		
		# Copy draw pass settings (XLU/OBJ) to each object
		if sourceObj and destObj._drawCalls:
			destObj._drawCalls[0].DrawPass = sourceObj._drawCalls[0].DrawPass
	
	# Delete temp mdl0 
	removeNode(sourceModel)
	
	# Select destination mdl0 node again. (This may seem redundant, but Index is preserved from before)
	selNode.Parent.SelectChildAtIndex(selNode.Index)
	
	# Number of materials imported that are not assigned to any objects
	EMPTY_MATS_COUNT = len(sourceMatsList)
	
	# I don't know what this does but it was requested
	selNode.Rebuild(True)
	
	message = "Materials and shaders imported successfully!"
	
	if EMPTY_MATS_COUNT:
		message += "\n\n" + str(EMPTY_MATS_COUNT) + " materials unassigned to objects (may be incorrectly assigned, or unused)"
		
	BrawlAPI.ShowMessage(message, SCRIPT_NAME)

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Import materials and shaders from an external MDL0 file", EnableCheck, ToolStripMenuItem("Import materials and shaders from...", None, import_model_settings))
