__author__ = "mawwwk"
__version__ = "1.4.2"

from BrawlLib.SSBB import * #Types.ARCFileType?
from mawwwkLib import *

SCRIPT_NAME = "Generate Static Redirects"

def main():
	arcNode = BrawlAPI.RootNode.FindChild("2")
	if not arcNode:
		BrawlAPI.ShowError("2 ARC not found.", SCRIPT_NAME)
		return
	
	hashIndexDict = {}		# MD5 : AbsoluteIndex
	nodesToDelete = []		# List of BRRES nodes converted, to delete later
	
	# Store childCount early, as it may change after adding redirect nodes
	childCount = len(arcNode.Children)
	
	# Loop through all brres nodes
	for i in range(childCount):
		
		# Check if node is a BRRES
		node = arcNode.Children[i]
		if not isinstance(node, BRRESNode):
			continue
		
		# If a static brres is found, check if a matching hash exists
		modelsGroup = node.FindChild(MDL_GROUP)
		isStaticBRRES = node.UncompressedSize == 640 and modelsGroup and modelsGroup.HasChildren and len(modelsGroup.Children) == 1
		if not isStaticBRRES:
			continue
		
		nodeHash = node.MD5Str()
		# If nodeHash not in hashIndexDict, add it as a hash:index entry
		if nodeHash not in hashIndexDict.keys():
			hashIndexDict[nodeHash] = node.AbsoluteIndex
		
		# If matching hash exists
		else:
			# Create a new redirect
			newNode = ARCEntryNode()
			arcNode.AddChild(newNode)
			
			# Set properties
			newNode.FileType = ARCFileType.ModelData
			newNode.FileIndex = node.FileIndex
			newNode.RedirectIndex = hashIndexDict[nodeHash]
			
			# Mark the BRRES to delete later
			nodesToDelete.append(node)
	
	# Delete all converted BRRES nodes
	for node in nodesToDelete:
		node.Remove()
		
	# Results dialog
	if len(nodesToDelete):
		BrawlAPI.ShowMessage(str(len(nodesToDelete)) + " static redirects generated.", SCRIPT_NAME)
	else:
		BrawlAPI.ShowMessage("No possible static redirects found.", SCRIPT_NAME)

main()
