__author__ = "mawwwk"
__version__ = "0.9.3"
# EXPERIMENTAL - Updated 4/23/21, might break things still.
# Always test in-game!! always save backups!!
from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *

SCRIPT_NAME = "Clear Unused Vertices and Normals"
deletedNodeCount = 0
affectedModelsNamesList = []			# Names of all mdl0 nodes that contain nodes deleted during the script
usedRegeneratedModelsNamesList = []		# Names of all mdl0 nodes that contain vertex/normal nodes named "Regenerated" that are used by objects

# Debug message
def dmessage(msg):
	BrawlAPI.ShowMessage(msg, "DEBUG")

##
## Begin node-parser methods

# Basic impl of list.reverse() to accommodate ResourceNode lists
def reverseResourceList(nodeList):
	nodeListReverse = []
	for i in nodeList:
		nodeListReverse.append(i)
	
	nodeListReverse.reverse()
	return nodeListReverse

# Given any node, return the first child node whose name contains the given nameStr, or return 0 if not found
def getChildFromName(node, nameStr):
	if node.HasChildren:
		for child in node.Children:
			if str(nameStr) in child.Name:
				return child
	return 0

# point parser to ModelData brres
def parseBrres(node):
	if "Model Data" in node.Name:
		parseModelData(node)

# Given a ModelData brres, iterate through appropriate child group nodes
def parseModelData(brres):
	# Iterate through models inside brres
	modelsGroup = getChildFromName(brres, "3DModels")
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			parseMDL0(mdl0)

# Given a mdl0 node, delete any unused vertices or normals, and detect any used "Regenerated" nodes
def parseMDL0(mdl0):
	global deletedNodeCount
	unusedFound = False 			# Set to true if any unused nodes found
	usedRegeneratedFound = False 	# Set to true if any nodes named "Regenerated" are actually used
	
	for group in [getChildFromName(mdl0, "Vertices"), getChildFromName(mdl0, "Normals")]:
		if group:
		# Iterate through VertexNodes in mdl0. If object count == 0, delete the node
			nodesList = reverseResourceList(group.Children)
			for node in nodesList:
				if len(node._objects) == 0:
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

## End parser methods
## 
## Begin getter methods

# Return 2 ARC of currently opened file
def getParentArc():
	for i in BrawlAPI.RootNode.Children:
		if i.Name == "2" and isinstance(i, ARCNode):
			return i
	
	BrawlAPI.ShowError("2 ARC not found", "Error")
	return 0

## End getter methods
##
## Start of main script

# Confirmation prompt
message = "Detect and remove any unused Vertex or Normal nodes inside models.\n\n"
message += "DISCLAIMER: Always check the final results in-game.\n"

if BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
	global deletedNodeCount
	
	# Iterate through brres nodes
	for node in getParentArc().Children:
		if isinstance(node, BRRESNode):
			parseBrres(node)
	
	# Show results
	
	# If no nodes deleted
	if deletedNodeCount == 0:
		BrawlAPI.ShowMessage("No unused normals or vertex nodes found", SCRIPT_NAME)
	
	# If one or more unused nodes found and deleted
	else:
		message = str(deletedNodeCount) + " unused nodes found and deleted.\n\n"
		for i in affectedModelsNamesList:
			message += i + "\n"
		BrawlAPI.ShowMessage(message, SCRIPT_NAME)
	
	# If any used "Regenerated" nodes exist, warn the user
	if len(usedRegeneratedModelsNamesList):
		message = "Regenerated nodes in-use (consider renaming these):\n\n"
		
		for i in usedRegeneratedModelsNamesList:
			message += i + "\n"
		
		BrawlAPI.ShowError(message, SCRIPT_NAME)
	