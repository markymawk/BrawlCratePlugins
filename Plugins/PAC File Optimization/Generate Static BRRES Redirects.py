__author__ = "mawwwk"
__version__ = "1.3"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.SSBB import * #Types.ARCFileType?
from BrawlLib.SSBB.Types import * #Types.ARCFileType
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from mawwwkLib import *

SCRIPT_NAME = "Generate Static Redirects"

## Begin helper methods
	
# Create a new redirect ARCEntryNode given the FileIndex and RedirectIndex values
def createRedirect(baseIndex, newRedirectIndex, parentARC):
	newNode = ARCEntryNode()
	
	parentARC.AddChild(newNode)
	newNode.FileType = ARCFileType.ModelData
	newNode.FileIndex = baseIndex
	newNode.RedirectIndex = newRedirectIndex

## End helper methods
## Start of main method

def main():
	PARENT_2_ARC = getParentArc()
	if not PARENT_2_ARC:
		return
	
	hashIndexDict = {}		# MD5 to AbsoluteIndex key-value dict
	redirectCount = 0		# Number of redirect nodes created
	convertedNodes = []		# List of BRRES nodes converted, to delete later
	
	# Iterate through all brres nodes
	for i in range(0,len(PARENT_2_ARC.Children),1):
	
		node = PARENT_2_ARC.Children[i]
		nodeHash = node.MD5Str()
		
		# If a static brres is found, check if a matching hash exists
		if isStaticBRRES(node):
		
			# If matching hash exists...
			if nodeHash in hashIndexDict.keys():
				# ...create a redirect
				createRedirect(node.FileIndex, hashIndexDict[nodeHash], PARENT_2_ARC)
				redirectCount += 1
				
				# Mark the BRRES to delete later
				convertedNodes.append(node)
			
			# If no matching hash exists, set as a "static root" by saving the hash+index pair
			else:
				hashIndexDict[nodeHash] = node.AbsoluteIndex
	
	# Delete all converted BRRES nodes
	removeChildNodes(convertedNodes)
		
	# Results dialog
	if redirectCount:
		BrawlAPI.ShowMessage(str(redirectCount) + " static redirects generated", SCRIPT_NAME)
	else:
		BrawlAPI.ShowMessage("No possible static redirects found", SCRIPT_NAME)

main()
