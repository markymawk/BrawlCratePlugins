__author__ = "mawwwk"
__version__ = "2.1"

from BrawlCrate.NodeWrappers import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

SCRIPT_NAME = "Locate TEX0 Usage"

## Start enable check function
# Wrapper: TEX0Wrapper
def EnableCheckTEX0(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node and node.Parent

## End enable check function
## Start helper functions

# Given a brres and name of the selected tex0, return list of MDL0s that use the tex0
def getMDL0Uses(brres, tex0Name):
	
	# If no MDL0 in brres, return
	modelsGroup = brres.FindChild(MDL_GROUP)
	if not modelsGroup:
		return []
	
	usesList = []
	
	# Loop through MDL0s in brres
	for mdl0 in modelsGroup.Children:
		mdl0TexturesGroup = mdl0.FindChild("Textures")
		
		if not mdl0TexturesGroup:
			continue
		
		if tex0Name in getChildNames(mdl0TexturesGroup):
			usesList.append(mdl0)
	
	return usesList

def getPAT0Uses(brres, tex0Name):
	# If no PAT0 in brres, return
	pat0Group = brres.FindChild(PAT_GROUP)
	if not pat0Group:
		return []
	
	usesList = []
	
	# Loop through PAT0s in brres
	for pat0 in pat0Group.Children:
		for pat0Entry in pat0.Children:
			for pat0TextureNode in pat0Entry.Children:
				# Check frames, aka PAT0TextureEntryNode
				for frame in pat0TextureNode.Children:
					if frame.Name == tex0Name:
						usesList.append(pat0TextureNode)
						break
	
	return usesList

## End helper functions
## Start loader functions

def locate_tex0_usage(sender, event_args):
	tex0Name = BrawlAPI.SelectedNode.Name
	parentBRRES = BrawlAPI.SelectedNode.Parent.Parent
	
	allModelUses = [] # List of MDL0 nodes used
	allPat0Uses = []  # List of PAT0 nodes used
	
	# If parent brres contains models or PAT0s, only check within that brres
	checkSingleBrres = MDL_GROUP in getChildNames(parentBRRES) or PAT_GROUP in getChildNames(parentBRRES)
	
	if checkSingleBrres:
		# Get individual MDL0 usage, then append to allModelUses[]
		for i in getMDL0Uses(brres, tex0Name):
			allModelUses.append(i)
		
		# Get individual PAT0 usage, then append to allPat0Uses[]
		for i in getPAT0Uses(brres, tex0Name):
			allPat0Uses.append(i)
	
	# If parent node is a brres with no MDL0/PAT0s, check all brres nodes in the file
	elif isinstance(parentBRRES, BRRESNode):
		for brres in BrawlAPI.NodeListOfType[BRRESNode]():
			# Get individual MDL0 usage, then append to allModelUses[]
			for i in getMDL0Uses(brres, tex0Name):
				allModelUses.append(i)
				
			# Get individual PAT0 usage, then append to allPat0Uses[]
			for i in getPAT0Uses(brres, tex0Name):
				allPat0Uses.append(i)
	
	# If trouble recognizing node layout, show error
	else:
		BrawlAPI.ShowError("Error: can't detect usable textures in parent node", SCRIPT_NAME)
		return
	
	# If TEX0 not used, show message and return
	if len(allModelUses + allPat0Uses) == 0:
		BrawlAPI.ShowError("No TEX0 usage found", SCRIPT_NAME)
		return
	
	# Start results message
	resultsMsg = tex0Name + " found in:\n"
	modelUseCount = 0
	pat0UseCount = 0
	
	# Get formatted MDL0 strings
	for mdl0 in allModelUses:
		brres = mdl0.Parent.Parent
		
		# Append MDL0 name to string
		resultsMsg += "\nMDL0: " + brres.Name + "/" + mdl0.Name + "\n"
		
		# Loop through used materials
		for texRef in mdl0.FindChild("Textures").FindChild(tex0Name)._references:
			
			# If final use count is 1, this material will be fetched
			modelUseCount += 1
			mat = texRef.Material
			resultsMsg += "- Material: " + mat.Name + "\n"
			
			# Get objects used by this mat
			if len(mat._objects):
				for obj in mat._objects:
					resultsMsg += "  - Object: " + obj.Name + "\n"
	
	# Get formatted PAT0 strings
	for pat0TexNode in allPat0Uses:
		
		# If final use count is 1, this pat0 will be fetched
		pat0UseCount += 1
		pat0 = pat0TexNode.Parent.Parent
		brres = pat0.Parent.Parent
		resultsMsg += "\nPAT0: " + brres.Name + "/" + pat0.Name + "/" + pat0TexNode.Parent.Name + "/" + pat0TexNode.Name + "\n"
	
	## Show results
	# If single use MDL0, prompt to select material
	if len(allModelUses) == 1 and modelUseCount == 1:
		resultsMsg += "\n\nSelect this material?"
		if not BrawlAPI.ShowYesNoPrompt(resultsMsg, SCRIPT_NAME):
			return
		
		selectNode(mat)
	
	# If single use PAT0, prompt to select it
	elif len(allPat0Uses) == 1 and pat0UseCount == 1:
		resultsMsg += "\n\nSelect this PAT0?"
		if not BrawlAPI.ShowYesNoPrompt(resultsMsg, SCRIPT_NAME):
			return
		
		selectNode(allPat0Uses[0])
	
	# If multiple uses, list them
	else:
		BrawlAPI.ShowMessage(resultsMsg, SCRIPT_NAME)

## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Find TEX0 usage in models or PAT0 animations", EnableCheckTEX0, ToolStripMenuItem("Locate", None, locate_tex0_usage))
