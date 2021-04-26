__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem

SCRIPT_NAME = "Locate TEX0 Usage"
SELECTED_TEX0_NAME = ""
usedMDL0Names = []
usedPAT0Names = []

# Function to return to 2 ARC of current file
def getParentArc():
	for i in BrawlAPI.RootNode.Children:
		if i.Name == "2" and isinstance(i, ARCNode):
			return i
	
	BrawlAPI.ShowError("2 ARC not found", "Error")
	return 0	# If not found, return 0

# Given any node, return its child node whose name contains the given nameStr
def getChildFromName(node, nameStr):
	if node.Children:
		for child in node.Children:
			if str(nameStr) in child.Name:
				return child
	return 0	# If not found, return 0

def parseBrres(node):
	if "Model Data" in node.Name:
		parseModelData(node)

# Return list of strings of node names in a given group
def getChildNames(group):
	list = []
	for i in group.Children:
		list.append(i.Name)
	return list

def parseModelData(brres):
	modelsGroup = getChildFromName(brres, "3DModels")
	pat0Group = getChildFromName(brres, "AnmTexPat")
	
	# Iterate through models
	if modelsGroup:
		for mdl0 in modelsGroup.Children:
			# Ignore static models
			if mdl0.Name.lower() != "static":
				parseMDL0(mdl0)
	
	# Iterate through pat0s
	if pat0Group:
		for pat0 in pat0Group.Children:
			parsePAT0(pat0)

def parseMDL0(mdl0):
	mdl0TexturesGroup = getChildFromName(mdl0, "Textures")
	
	# If texture exists in the mdl0 Textures group, append to usedMDL0Names[]
	if mdl0TexturesGroup and SELECTED_TEX0_NAME in getChildNames(mdl0TexturesGroup):
		usedMDL0Names.append("MDL0 " + mdl0.Parent.Parent.Name + "/" + mdl0.Name)

def parsePAT0(pat0):
	# Get material from base pat0 node
	for material in pat0.Children:
		# For texture reference in material
		for texRef in material.Children:
			# If texture exists in the pat0, append to usedPAT0Names[]
			if SELECTED_TEX0_NAME in getChildNames(texRef):
				usedPAT0Names.append("PAT0 " + pat0.Parent.Parent.Name + "/" + pat0.Name)

# Check that tex0 is under a "2 ARC" to determine that the pac is a stage, not a character
def EnableCheckTEX0(sender, event_args):
	sender.Enabled = (BrawlAPI.SelectedNode is not None and BrawlAPI.SelectedNode.Parent.Parent.Parent.Name == "2")

# Function to open single stage PAC file
def locate_tex0_usage(sender, event_args):
	global SELECTED_TEX0_NAME
	SELECTED_TEX0_NAME = BrawlAPI.SelectedNode.Name
	PARENT_BRRES = BrawlAPI.SelectedNode.Parent.Parent
	error = False
	
	# Clear lists at the beginning of each run - for some reason they persist otherwise
	#usedMDL0Names.clear()	# Only works in newer Python lol
	#usedPAT0Names.clear()	#
	del usedMDL0Names[:]
	del usedPAT0Names[:]
	
	# If selected tex0 is in a TextureData, scan all brres in the pac
	if "Texture Data" in PARENT_BRRES.Name:
		for node in getParentArc().Children:
			if isinstance(node, BRRESNode):
				parseBrres(node)
	# If selected tex0 is in a ModelData brres, only scan that ModelData
	elif "Model Data" in PARENT_BRRES.Name:
		parseBrres(PARENT_BRRES)
	# Else, error -- can't detect parent brres
	else:
		BrawlAPI.ShowError("Error: can't detect parent BRRES format", SCRIPT_NAME)
		error = True
	
	IS_MDL0_FOUND = len(usedMDL0Names)
	IS_PAT0_FOUND = len(usedPAT0Names)
	
	if not error:
		message = ""
		if IS_MDL0_FOUND or IS_PAT0_FOUND:
			message += SELECTED_TEX0_NAME + " found in:\n\n"
			for i in (usedMDL0Names + usedPAT0Names):
				message += i + "\n"
			
			BrawlAPI.ShowMessage(message, SCRIPT_NAME)
		else:
			BrawlAPI.ShowError("No TEX0 usage found",SCRIPT_NAME)

BrawlAPI.AddContextMenuItem(TEX0Wrapper, "", "Detect uses in models or pat0 animations", EnableCheckTEX0, ToolStripMenuItem("Locate", None, locate_tex0_usage))