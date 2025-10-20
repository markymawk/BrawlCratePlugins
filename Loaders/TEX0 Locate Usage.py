__author__ = "mawwwk and soopercool101"
__version__ = "1.6"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Locate TEX0 Usage"

## Start enable check function
# Wrapper: TEX0Wrapper
def EnableCheckTEX0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node and node.Parent)

## End enable check function
## Start helper functions

# Given a brres Models group, check for usage in MDL0s
def getModelUsage(modelsGroup, tex0Name):
	modelUses = []
	for mdl0 in modelsGroup.Children:
		mdl0TexturesGroup = mdl0.FindChild("Textures")
	
		# If texture exists in the mdl0 Textures group, append an entry to modelUses[]
		if mdl0TexturesGroup and tex0Name in getChildNames(mdl0TexturesGroup):
			
			# Model name, for entry[0]
			brres = mdl0.Parent.Parent
			modelName = "MDL0: " + brres.Name + "/" + mdl0.Name
			
			# Materials names, for entry[1]
			materialsList = getUsedMaterials(mdl0TexturesGroup, tex0Name)
			
			# If materials list is empty, skip this entry
			if len(materialsList) == 0:
				continue
			# Objects names, for entry[2]
			objectsNamesList = getUsedObjectsList(mdl0, materialsList)
			
			modelUses.append([modelName, materialsList, objectsNamesList])
	return modelUses

# Given a MDL0 Textures group, return a formatted string containing list of used materials that reference selected TEX0 name
def getUsedMaterials(mdl0TexturesGroup, tex0Name):
	mdl0TextureNode = mdl0TexturesGroup.FindChild(tex0Name)
	
	matList = []
	for texRef in mdl0TextureNode._references:
		matList.append(texRef.Material)
	
	return matList

# Given a mdl0 node and list of material names, return a list of objects used by those mats
def getUsedObjectsList(mdl0, materialsList):
	objectsList = []
	
	for mat in materialsList:
		
		# If material exists and is used by objects, append the object(s) to objectsList[]
		if mat and len(mat._objects):
			for obj in mat._objects:
				objectsList.append(obj.Name)
				
	return objectsList

# Given a brres PAT0 group, check for usage in PAT0s
def getPAT0Usage(pat0Group, tex0Name):
	pat0Uses = []
	
	for pat0 in pat0Group.Children:
		for pat0Entry in pat0.Children:
			for pat0TextureNode in pat0Entry.Children:
				
				framesUsed = []
				
				# Loop through texture entry nodes to find frames used
				for pat0TextureEntryNode in pat0TextureNode.Children:
					if pat0TextureEntryNode.Name == tex0Name:
						framesUsed.append(int(pat0TextureEntryNode.FrameIndex))
				
				# If texture used, append to pat0Uses[]
				if len(framesUsed):
					pat0Uses.append([pat0, framesUsed])
					
	return pat0Uses

## End helper functions
## Start loader functions

def locate_tex0_usage(sender, event_args):
	tex0Name = BrawlAPI.SelectedNode.Name
	parentBRRES = BrawlAPI.SelectedNode.Parent.Parent
	modelsGroup = parentBRRES.FindChild(MDL_GROUP)
	pat0Group = parentBRRES.FindChild(PAT_GROUP)
	
	allModelUses = [] # List of lists[3] which contain model, material, and object names that use the selected tex0
	allPAT0Uses = []  # List of PAT0 node names that use the selected tex0
	
	# If parent brres contains models or PAT0s, only check within that brres
	if modelsGroup or pat0Group:

		# Get individual MDL0 usage, then append to allModelUses[]
		if modelsGroup:
			thisModelUses = getModelUsage(modelsGroup, tex0Name)
			
			for i in thisModelUses:
				allModelUses.append(i)
		
		# Get individual PAT0 usage, then append to allPAT0Uses[]
		if pat0Group:
			thisPAT0Uses = getPAT0Usage(pat0Group, tex0Name)
			
			for i in thisPAT0Uses:
				allPAT0Uses.append(i)
	
	# Assume selected tex0 is in a TextureData; check all brres nodes in the file
	elif isinstance(parentBRRES, BRRESNode):
		for brres in BrawlAPI.NodeListOfType[BRRESNode]():
			modelsGroup = brres.FindChild(MDL_GROUP)
			pat0Group = brres.FindChild(PAT_GROUP)
			
			# Get individual MDL0 usage, then append to allModelUses[]
			if modelsGroup:
				thisModelUses = getModelUsage(modelsGroup, tex0Name)
				
				for i in thisModelUses:
					allModelUses.append(i)
			
			# Get individual PAT0 usage, then append to allPAT0Uses[]
			if pat0Group:
				thisPAT0Uses = getPAT0Usage(pat0Group, tex0Name)
				
				for i in thisPAT0Uses:
					allPAT0Uses.append(i)
	
	# If trouble recognizing node layout, show error
	else:
		BrawlAPI.ShowError("Error: can't detect usable textures in parent node", SCRIPT_NAME)
		return
	
	# Results
	# If tex0 is used, show list of uses
	if len(allModelUses + allPAT0Uses):
		resultsMsg = tex0Name + " found in:\n\n"
		
		# Get list of MDL0 uses
		if len(allModelUses):
			# For each model use, show MDL0, material, and object names
			for entry in allModelUses:
				
				resultsMsg += entry[0] + "\n"
				
				for material in entry[1]:
					resultsMsg += "Material: " + material.Name + "\n"
				
				for objName in entry[2]:
					resultsMsg += "Object: " + objName + "\n"
				
				resultsMsg += "\n"
			
		# Get list of PAT0 uses
		if len(allPAT0Uses):
			dmsg(len(allPAT0Uses))
			for pat0Use in allPAT0Uses:
				pat0 = pat0Use[0]
				framesUsed = pat0Use[1]
				usageStr = "PAT0: " + pat0Use[0].Parent.Parent.Name + "/" + pat0.Name
				usageStr += "\n  Frame "
				
				# List frames used
				for i in pat0Use[1]:
					usageStr += str(i) + ", "
				
				usageStr = usageStr[:-2]
			
			resultsMsg += usageStr
		else:
			resultsMsg = resultsMsg[:-1] # Remove last \n
		
		# If TEX0 is only used in one location, add prompt message to select it
		if len(allModelUses + allPAT0Uses) == 1:
			resultsMsg += "\n\nSelect this material?"
			if not BrawlAPI.ShowYesNoPrompt(resultsMsg, SCRIPT_NAME):
				return
			
			# This "[0][1][0]" organization is a mess tbh
			if len(allModelUses) == 1:
				node = allModelUses[0][1][0]
			else:
				node = allPAT0Uses[0][0]
			index = node.Index
			wrapper = getWrapperFromNode(node)
			wrapper.Expand()
			node.Parent.SelectChildAtIndex(index)
			
		# If TEX0 is used in more than one place, show list of uses
		else:
			BrawlAPI.ShowMessage(resultsMsg, SCRIPT_NAME)
	
	# If tex0 not used
	else:
		BrawlAPI.ShowError("No TEX0 usage found", SCRIPT_NAME)

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Find TEX0 usage in models or PAT0 animations", EnableCheckTEX0, ToolStripMenuItem("Locate", None, locate_tex0_usage))
