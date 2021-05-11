__author__ = "mawwwk"
__version__ = "1.1"

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
	if BrawlAPI.RootNode:
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
	and modelsGroup and modelsGroup.HasChildren and len(modelsGroup.Children) == 1:
		return True
	else:
		return False
	
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
if PARENT_2_ARC:
	hashIndexDict = {}		# MD5 to AbsoluteIndex key-value dict
	redirectCount = 0		# Number of redirect nodes created
	convertedNodes = []		# List of BRRES nodes converted, to delete later
	
	# Iterate through all brres nodes to find the first static 
	for i in range(0,len(PARENT_2_ARC.Children),1):
	
		node = PARENT_2_ARC.Children[i]
		nodeHash = node.MD5Str()
		
		# If a static brres is found, check if a matching hash exists
		if isStaticBRRES(node):
		
			# If matching hash exists...
			if nodeHash in hashIndexDict.keys():
				# ...create a redirect
				createRedirect(node.FileIndex, hashIndexDict[nodeHash])
				redirectCount += 1
				
				# Mark the BRRES to delete later
				convertedNodes.append(node)
			
			# If no matching hash exists, set as a "static root" by saving the hash+index pair
			else:
				hashIndexDict[nodeHash] = node.AbsoluteIndex
	
	# Delete all converted BRRES nodes
	for node in convertedNodes:
		node.Remove()
		
	# Results dialog
	if redirectCount:
		BrawlAPI.ShowMessage(str(redirectCount) + " static redirects generated", SCRIPT_NAME)
	else:
		BrawlAPI.ShowMessage("No possible static redirects found", SCRIPT_NAME)
