__author__ = "mawwwk"
__version__ = "3.0"

from mawwwkLib import *

SCRIPT_NAME = "Clean MDL0 Data Entries"

def main():
	# Confirmation prompt
	startMsg = "Detect and remove any unused Vertex, Normal, and UV nodes inside models.\n\n"
	startMsg += "DISCLAIMER: Always check the final results in-game!\n"
	if not BrawlAPI.ShowOKCancelPrompt(startMsg, SCRIPT_NAME):
		return
	
	nodesToRemove = []
	MDL0_GROUPS = ["Vertices", "Normals", "UVs"] 
	
	# Loop through models
	for mdl0 in BrawlAPI.NodeListOfType[MDL0Node]():
		for groupName in MDL0_GROUPS:
			group = mdl0.FindChild(groupName)
			if not group:
				continue
			
			# Loop through nodes
			for node in group.Children:
				# If object count == 0, delete the node
				if len(node._objects) == 0:
					nodesToRemove.append(node)
	
	# Results
	# If no nodes deleted
	if len(nodesToRemove) == 0:
		BrawlAPI.ShowMessage("No unused vertex, normal, or UV nodes found", SCRIPT_NAME)
	
	# If one or more unused nodes found, show a list
	else:
		msgList = []
		sizeCount = 0
		for node in nodesToRemove:
			mdl0 = node.Parent.Parent
			msgList.append(mdl0.Name + "/" + node.Parent.Name + "/" + node.Name)
			sizeCount += node.UncompressedSize
		
		resultsMsg = str(len(nodesToRemove)) + " unused node(s) found. Delete these?\n"
		resultsMsg += str(sizeCount) + " bytes\n\n"
		resultsMsg += listToString(msgList, 15)
		
		if not BrawlAPI.ShowYesNoPrompt(resultsMsg, SCRIPT_NAME):
			return
		for node in nodesToRemove:
			node.Remove()

main()