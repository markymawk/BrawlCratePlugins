__author__ = "mawwwk"
__version__ = "1.4.1"

from BrawlLib.SSBB import * #Types.ARCFileType?
from mawwwkLib import *

SCRIPT_NAME = "Generate Static Redirects"

## Start of main method

def main():
	arc_2 = BrawlAPI.RootNode.FindChild("2")
	if not arc_2:
		BrawlAPI.ShowError("2 ARC not found.", SCRIPT_NAME)
		return
	
	hashIndexDict = {}		# MD5 to AbsoluteIndex key-value dict
	convertedNodes = []		# List of BRRES nodes converted, to delete later
	
	# Store childCount early, as it may change after adding redirect nodes
	childCount = len(arc_2.Children)
	
	# Loop through all brres nodes
	for i in range(childCount):
	
		node = arc_2.Children[i]
		nodeHash = node.MD5Str()
		
		modelsGroup = node.FindChild(MDL_GROUP)
		
		isStaticBRRES = (node.UncompressedSize == 640 and isinstance(node, BRRESNode) and modelsGroup and modelsGroup.HasChildren and len(modelsGroup.Children) == 1)
		# If a static brres is found, check if a matching hash exists
		if isStaticBRRES:
		
			# If matching hash exists...
			if nodeHash in hashIndexDict.keys():
				# ...create a redirect
				newNode = ARCEntryNode()
				arc_2.AddChild(newNode)
				
				# Set redirect properties
				newNode.FileType = ARCFileType.ModelData
				newNode.FileIndex = node.FileIndex
				newNode.RedirectIndex = hashIndexDict[nodeHash]
				
				# Mark the BRRES to delete later
				convertedNodes.append(node)
			
			# If no matching hash exists, set as a "static root" by saving the hash+index pair
			else:
				hashIndexDict[nodeHash] = node.AbsoluteIndex
	
	# Delete all converted BRRES nodes
	redirectCount = len(convertedNodes)
	removeChildNodes(convertedNodes)
		
	# Results dialog
	if redirectCount:
		BrawlAPI.ShowMessage(str(redirectCount) + " static redirects generated", SCRIPT_NAME)
	else:
		BrawlAPI.ShowMessage("No possible static redirects found", SCRIPT_NAME)

main()
