__author__ = "mawwwk"
__version__ = "2.1"

from BrawlCrate.API import *
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from mawwwkLib import *

SCRIPT_NAME = "Clear Unused Vertices and Normals"

def main():
	# Confirmation prompt
	startMsg = "Detect and remove any unused Vertex or Normal nodes inside models.\n\n"
	startMsg += "DISCLAIMER: Always check the final results in-game!\n"
	if not BrawlAPI.ShowOKCancelPrompt(startMsg, SCRIPT_NAME):
		return
	
	deletedNodeCount = 0
	sizeCount = 0					# Sum of deleted nodes file size, in uncompressed bytes
	affectedModelsNames = []		# All mdl0s that contain nodes deleted during the script
	
	# Loop through models
	for mdl0 in BrawlAPI.NodeListOfType[MDL0Node]():
		unusedNodesFound = False
		brresName = mdl0.Parent.Parent.Name
		
		for group in [mdl0.FindChild("Vertices"), mdl0.FindChild("Normals")]:
			if not group:
				continue
			
			# Loop through Vertex & normal nodes
			nodeList = reverseResourceList(group.Children)
			for node in nodeList:
				# If object count == 0, delete the node
				if len(node._objects) == 0:
					sizeCount += node.UncompressedSize
					node.Remove()
					deletedNodeCount += 1
					unusedNodesFound = True
		
		# If any unused vertices or normals found, append brres name and mdl0 name to "affected" list
		if unusedNodesFound:
			affectedModelsNames.append(brresName + "/" + mdl0.Name)
	
	# Results
	# If no nodes deleted
	if deletedNodeCount == 0:
		BrawlAPI.ShowMessage("No unused normals or vertex nodes found", SCRIPT_NAME)
	
	# If one or more unused nodes found and deleted
	else:
		message = str(deletedNodeCount) + " unused node(s) found and deleted.\n\n"
		message += listToString(affectedModelsNames)
		message += "\n" + str(sizeCount) + " bytes"
		
		BrawlAPI.ShowMessage(message, SCRIPT_NAME)

main()