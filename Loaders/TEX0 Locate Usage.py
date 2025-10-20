__author__ = "mawwwk"
__version__ = "2.0"

from BrawlCrate.NodeWrappers import *
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

# Return formatted string of TEX0 use in MDL0 nodes
def getMDL0String(allModelUses, tex0Name, getSingleUse=False):
	outputStr = ""
	for mdl0 in allModelUses:
		brres = mdl0.Parent.Parent
		
		# Append MDL0 name to string
		outputStr += "\nMDL0: " + brres.Name + "/" + mdl0.Name + "\n"
		
		# Get used materials
		for texRef in mdl0.FindChild("Textures").FindChild(tex0Name)._references:
			mat = texRef.Material
			
			# If getting single-use material to select, return this material
			if getSingleUse:
				return mat
			outputStr += "- Material: " + mat.Name + "\n"
			
			# Get objects used by this mat
			if len(mat._objects):
				for obj in mat._objects:
					outputStr += "  - Object: " + obj.Name + "\n"
	
	return outputStr

# Return formatted string of TEX0 use in PAT0 nodes
def getPAT0String(allPat0Uses, tex0Name, getSingleUse=False):
	outputStr = ""
	for pat0TexNode in allPat0Uses:
		pat0 = pat0TexNode.Parent.Parent
		# If getting single-use PAT0 to select, return this
		if getSingleUse:
			return pat0TexNode
		brres = pat0.Parent.Parent
		outputStr += "\nPAT0: " + brres.Name + "/" + pat0.Name + "/" + pat0TexNode.Parent.Name + "/" + pat0TexNode.Name + "\n"
	
	return outputStr

## End helper functions
## Start loader functions

def locate_tex0_usage(sender, event_args):
	tex0Name = BrawlAPI.SelectedNode.Name
	parentBRRES = BrawlAPI.SelectedNode.Parent.Parent
	
	allModelUses = [] # List of MDL0 nodes used
	allPAT0Uses = []  # List of PAT0 nodes used
	
	# If parent brres contains models or PAT0s, only check within that brres
	checkSingleBrres = MDL_GROUP in getChildNames(parentBRRES) or PAT_GROUP in getChildNames(parentBRRES)
	
	if checkSingleBrres:
		# Get individual MDL0 usage, then append to allModelUses[]
		for i in getMDL0Uses(brres, tex0Name):
			allModelUses.append(i)
		
		# Get individual PAT0 usage, then append to allPAT0Uses[]
		for i in getPAT0Uses(brres, tex0Name):
			allPAT0Uses.append(i)
	
	# If parent node is a brres with no MDL0/PAT0s, check all brres nodes in the file
	elif isinstance(parentBRRES, BRRESNode):
		for brres in BrawlAPI.NodeListOfType[BRRESNode]():
			# Get individual MDL0 usage, then append to allModelUses[]
			for i in getMDL0Uses(brres, tex0Name):
				allModelUses.append(i)
				
			# Get individual PAT0 usage, then append to allPAT0Uses[]
			for i in getPAT0Uses(brres, tex0Name):
				allPAT0Uses.append(i)
	
	# If trouble recognizing node layout, show error
	else:
		BrawlAPI.ShowError("Error: can't detect usable textures in parent node", SCRIPT_NAME)
		return
	
	useCount = len(allModelUses + allPAT0Uses)
	
	# If not found, show message and return
	if useCount == 0:
		BrawlAPI.ShowError("No TEX0 usage found", SCRIPT_NAME)
		return
	
	# Get formatted strings
	resultsMsg = tex0Name + " found in:\n"
	resultsMsg += getMDL0String(allModelUses, tex0Name)
	resultsMsg += getPAT0String(allPAT0Uses, tex0Name)
	
	# If single use MDL0, prompt to select material (even if PAT0 is used)
	if len(allModelUses) == 1:
		resultsMsg += "\n\nSelect this material?"
		if not BrawlAPI.ShowYesNoPrompt(resultsMsg, SCRIPT_NAME):
			return
		
		# Select material node
		material = getMDL0String(allModelUses, tex0Name, True)
		selectNode(material)
	
	# If single use PAT0, prompt to select it
	elif len(allPAT0Uses) == 1:
		resultsMsg += "\n\nSelect this PAT0?"
		if not BrawlAPI.ShowYesNoPrompt(resultsMsg, SCRIPT_NAME):
			return
		
		# Select pat0 node
		pat0 = getPAT0String(allPAT0Uses, tex0Name, True)
		selectNode(pat0)
	# If multiple uses, list them
	else:
		BrawlAPI.ShowMessage(resultsMsg, SCRIPT_NAME)
## End loader functions
## Start context menu add

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Find TEX0 usage in models or PAT0 animations", EnableCheckTEX0, ToolStripMenuItem("Locate", None, locate_tex0_usage))
