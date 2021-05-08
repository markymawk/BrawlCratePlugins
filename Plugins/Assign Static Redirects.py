__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB import * #Types.ARCFileType?
from BrawlLib.SSBB.Types import * #Types.ARCFileType
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *

SCRIPT_NAME = "Assign Static Redirects"

## Begin helper methods

# Given any node, return its child node whose name contains the given nameStr
def getChildFromName(node, nameStr):
	if node.Children:
		for child in node.Children:
			if str(nameStr) in child.Name:
				return child
	return 0	# If not found, return 0

# Function to return to 2 ARC of current file
def getParentArc():
	for i in BrawlAPI.RootNode.Children:
		if i.Name == "2" and isinstance(i, ARCNode):
			return i
	# If not found, show an error and return 0
	BrawlAPI.ShowError("2 ARC not found", "Error")
	return 0	

# Return true if given node is a brres, of exactly 640 bytes, and has exactly one mdl0 node named appropriately
def isStaticBRRES(node):
	modelsGroup = getChildFromName(node,"3DModels")
	
	if node.UncompressedSize == 640 \
	and isinstance(node, BRRESNode) \
	and modelsGroup and modelsGroup.HasChildren and len(modelsGroup.Children) == 1 \
	and isStaticModelName(modelsGroup.Children[0].Name):
		return True
	else:
		return False

# Return true if the given string matches pre-defined static model names
def isStaticModelName(name):
	name = name.lower()
	return name == "static" or name == "null" or name == "nodeindex"
	
# Create a new redirect ARCEntryNode given the FileIndex and RedirectIndex values
def createRedirect(baseIndex, newRedirectIndex):
	global PARENT_2_ARC
	newNode = ARCEntryNode()
	
	PARENT_2_ARC.AddChild(newNode)
	newNode.FileType = ARCFileType.ModelData
	newNode.FileIndex = baseIndex
	newNode.RedirectIndex = newRedirectIndex

## End helper methods
## Start of main method

PARENT_2_ARC = getParentArc()
staticNodeIndex = -1	# Number of loops taken to reach the first static brres
redirectCount = 0		# Number of redirect nodes created

# Iterate through all brres nodes to find the first static 
for i in range(0,len(PARENT_2_ARC.Children),1):
	node = PARENT_2_ARC.Children[i]
	
	# If a static brres is found, mark it accordingly and exit the loop
	if isStaticBRRES(node):
		REDIRECT_ROOT_INDEX = node.FileIndex
		staticNodeIndex = i
		break

# If a static node's been found, continue looping through
if staticNodeIndex >= 0:

	# Continue iterating through brres, starting from the first static node
	for node in PARENT_2_ARC.Children[staticNodeIndex+1:]:
	
		# If node is a brres and matches the static hash
		if isStaticBRRES(node):
		
			# Create a new redirect, and delete the original brres
			createRedirect(node.FileIndex, REDIRECT_ROOT_INDEX)
			node.Remove()
			redirectCount += 1

# Results dialog
if redirectCount:
	BrawlAPI.ShowMessage(str(redirectCount) + " static redirects generated", SCRIPT_NAME)
else:
	BrawlAPI.ShowMessage("No possible static redirects found", SCRIPT_NAME)
