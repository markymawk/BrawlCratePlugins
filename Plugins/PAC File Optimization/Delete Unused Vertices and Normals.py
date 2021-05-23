__author__ = "mawwwk"
__version__ = "1.0.1"

# Always test in-game!! always save backups!!

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *
from mawwwkLib import *

SCRIPT_NAME = "Clear Unused Vertices and Normals"

deletedNodeCount = 0
affectedModelsNamesList = []			# Names of all mdl0 nodes that contain nodes deleted during the script
usedRegeneratedModelsNamesList = []		# Names of all mdl0 nodes that contain vertex/normal nodes named "Regenerated" that are used by objects
sizeCount = 0							# Sum of deleted nodes file size, in uncompressed bytes

## Begin helper methods
# Given a mdl0 node, delete any unused vertices or normals, and detect any used "Regenerated" nodes
def parseMDL0(mdl0):
	global deletedNodeCount
	global sizeCount
	unusedFound = False 			# Set to true if any unused nodes found
	usedRegeneratedFound = False 	# Set to true if any nodes named "Regenerated" are actually used
	
	for group in [getChildFromName(mdl0, "Vertices"), getChildFromName(mdl0, "Normals")]:
		if group:
		# Iterate through VertexNodes in mdl0. If object count == 0, delete the node
			nodesList = reverseResourceList(group.Children)
			for node in nodesList:
				if len(node._objects) == 0:
					sizeCount += node.UncompressedSize
					node.Remove()
					deletedNodeCount += 1
					unusedFound = True
				elif node.Name == "Regenerated":
					usedRegeneratedFound = True
	
	# If any unused vertices or normals found, append brres name and mdl0 name to "affected" list
	if unusedFound:
		affectedModelsNamesList.append(mdl0.Parent.Parent.Name + "/" + mdl0.Name)
	
	# If any "Regenerated" nodes are used, append brres name and mdl0 name to "usedRegenerated" list
	if usedRegeneratedFound:
		usedRegeneratedModelsNamesList.append(mdl0.Parent.Parent.Name + "/" + mdl0.Name)

## End helper methods
## Start of main script

# Confirmation prompt
message = "Detect and remove any unused Vertex or Normal nodes inside models.\n\n"
message += "DISCLAIMER: Always check the final results in-game!\n"

if BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
	global deletedNodeCount
	
	# Iterate through MDL0 nodes
	for node in BrawlAPI.NodeListOfType[MDL0Node]():
		parseMDL0(node)
	
	# Show results
	
	# If no nodes deleted
	if deletedNodeCount == 0:
		BrawlAPI.ShowMessage("No unused normals or vertex nodes found", SCRIPT_NAME)
	
	# If one or more unused nodes found and deleted
	else:
		message = str(deletedNodeCount) + " unused nodes found and deleted.\n\n"
		for i in affectedModelsNamesList:
			message += i + "\n"
		message += "\n" + str(sizeCount) + " bytes"
		BrawlAPI.ShowMessage(message, SCRIPT_NAME)
	
	# If any used "Regenerated" nodes exist, warn the user
	if len(usedRegeneratedModelsNamesList):
		message = "Regenerated nodes in-use (consider renaming these):\n\n"
		
		for i in usedRegeneratedModelsNamesList:
			message += i + "\n"
		
		BrawlAPI.ShowError(message, SCRIPT_NAME)
