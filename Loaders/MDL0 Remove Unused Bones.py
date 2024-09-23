__author__ = "mawwwk"
__version__ = "1.1"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Remove Unused Bones"
## Start enable check function

# Check that model has Bones group
# Wrapper: MDL0Wrapper
def EnableCheckMDL0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and node.FindChild("Bones") and node.FindChild("Objects")

## End enable check function
## Begin helper methods

def deleteBonesRecursive(bone):
	bonesRemovedCount = 0
	
	if bone.HasChildren:
		for childBone in getChildNodes(bone):
			bonesRemovedCount += deleteBonesRecursive(childBone)
	
	# If bone isn't the last bone, has no children, and isn't used by any objects, delete the bone
	isOnlyBone = isinstance(bone.Parent, MDL0GroupNode) and len(bone.Parent.Children) == 1 and not bone.HasChildren
	hasGeometry = "HasGeometry" in str(bone._boneFlags)
	
	if not isOnlyBone and not (bone.HasChildren or len(bone.VisibilityDrawCalls) or hasGeometry):
		removeNode(bone)
		bonesRemovedCount += 1
	
	return bonesRemovedCount

## End helper methods
## Start of loader functions

def delete_unused_bones(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	objectsGroup = selNode.FindChild("Objects")
	bonesGroup = selNode.FindChild("Bones")
	bonesRemovedCount = 0
	
	# Quit if non-SingleBind objects exist
	for obj in objectsGroup.Children:
		if obj.SingleBind == "(none)":
			msg = "Cannot detect unused bones.\nOne or more objects are not set to SingleBind."
			BrawlAPI.ShowError(msg, SCRIPT_NAME)
			return
	
	for rootBone in getChildNodes(bonesGroup):
		bonesRemovedCount += deleteBonesRecursive(rootBone)
	
	BrawlAPI.ShowMessage("Bones removed: " + str(bonesRemovedCount), SCRIPT_NAME)

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(MDL0Wrapper, "", "Remove bones unused by objects", EnableCheckMDL0, ToolStripMenuItem("Remove unused bones", None, delete_unused_bones))
