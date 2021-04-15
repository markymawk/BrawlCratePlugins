__author__ = "mawwwk"
__version__ = "0.9.2"
# EXPERIMENTAL - Updated 4/15/21, might break things still.
# Always test in-game!! always save backups!!
from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from System.IO import *

SCRIPT_NAME = "Clear Unused Vertices and Normals"
deletedNodeCount = 0
# Unique lists that cover the whole pac file, and are populated during run
affectedModelsNamesList = []
usedRegeneratedModelsNamesList = []

# Debug message
def message(msg):
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

# point parser to ModelData
def parseBrres(node):
	if "Model Data" in node.Name:
		parseModelData(node)

# Given a ModelData brres, iterate through appropriate child group nodes
def parseModelData(brres):
	# Iterate through models
	modelsGroup = getChildFromName(brres, "3DModels")
	
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			verticesGroup = getChildFromName(mdl0,"Vertices")
			normalsGroup = getChildFromName(mdl0,"Normals")
			# If the mdl0 has Vertices or Normals, dive in
			if verticesGroup or normalsGroup:
				parseMDL0(mdl0, verticesGroup, normalsGroup)

# Given a mdl0 node, delete any unused vertices or normals, and detect any used "Regenerated" nodes
def parseMDL0(mdl0, verticesGroup, normalsGroup):
	global deletedNodeCount
	
	unusedFound = False # If true by the end of this func, add to affected models list
	usedRegeneratedFound = False # Set to true if any "Regenerated" nodes are actually used?
	
	# Iterate from bottom-up
	verticesGroup = reverseResourceList(verticesGroup.Children)
	normalsGroup = reverseResourceList(normalsGroup.Children)
	
	# Iterate through VertexNodes in mdl0. If object count == 0, delete the node
	for node in verticesGroup:
		if not len(node._objects):
			node.Remove()
			unusedFound = True
			deletedNodeCount += 1
		elif node.Name == "Regenerated":
			usedRegeneratedFound = True
	
	for node in normalsGroup:
		if not len(node._objects):
			node.Remove()
			unusedFound = True
			deletedNodeCount += 1
		# Check "Regenerated" nodes that are used
		elif node.Name == "Regenerated":
			usedRegeneratedFound = True
			
	if unusedFound:
		modelDataName = mdl0.Parent.Parent.Name
		affectedModelsNamesList.append(modelDataName + "/" + mdl0.Name)
	
	if usedRegeneratedFound:
		modelDataName = mdl0.Parent.Parent.Name
		usedRegeneratedModelsNamesList.append(modelDataName + "/" + mdl0.Name)

## End parser methods
## 
## Begin getter methods

# Function to return to 2 ARC of current file
def getParentArc():
	for i in BrawlAPI.RootNode.Children:
		if i.Name == "2" and isinstance(i, ARCNode):
			return i
	
	BrawlAPI.ShowError("2 ARC not found", "Error")
	return 0

# Given any node, return its child node whose name contains the given nameStr
def getChildFromName(node, nameStr):
	if node.Children:
		for child in node.Children:
			if str(nameStr) in child.Name:
				return child
	return 0

## End getter methods
##
## Start of main script

# Confirmation prompt
message = "Detect and remove any unused Vertex or Normal nodes inside models.\n\n"
message += "DISCLAIMER: Always check the final results in-game.\n"
if BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
	# Get parent 2 ARC
	global deletedNodeCount
	PARENT_ARC = getParentArc()
	
	# Iterate through brres nodes
	for node in PARENT_ARC.Children:
		if isinstance(node, BRRESNode):
			parseBrres(node)
	
	# Show results
	
	# If none found
	if deletedNodeCount == 0:
		BrawlAPI.ShowMessage("No unused normals or vertex nodes found", SCRIPT_NAME)
	
	# If one or more unused node found and deleted
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
		
		BrawlAPI.ShowMessage(message, SCRIPT_NAME)
	