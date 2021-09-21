version = "1.2"
# mawwwkLib
# Common functions for use with BrawlAPI scripts

# i don't like naming things after myself but eh

from BrawlCrate.API import *	# BrawlAPI
from BrawlLib.SSBB.ResourceNodes import *

## Start constants

BRAWL_SONG_ID_LIST = [
 "X02", "X03", "X04", "X05", "X06", "X07", "X08", "X09", "X10", "X11", "X12", "X13",
 "X14", "X15", "X16", "X17", "X18", "X19", "X20", "X21", "X22", "X23", "X24", "X25", 
 "X26", "X27", "A01", "A02", "A03", "A04", "A05", "A06", "A07", "A08", "A09", "A10", 
 "A11", "A12", "A13", "A14", "A15", "A16", "A17", "A20", "A21", "A22", "A23", "B01", 
 "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B09", "B10", "C01", "C02", "C03", 
 "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12", "C13", "C14", "C15", 
 "C16", "C17", "C18", "C19", "D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", 
 "D09", "D10", "E01", "E02", "E03", "E04", "E05", "E06", "E07", "F01", "F02", "F03", 
 "F04", "F05", "F06", "F07", "F08", "F09", "F10", "F11", "F12", "G01", "G02", "G03", 
 "G04", "G05", "G06", "G07", "G08", "G09", "G10", "G11", "H01", "H02", "H03", "H04", 
 "H05", "H06", "H07", "H08", "H09", "H10", "I01", "I02", "I03", "I04", "I05", "I06", 
 "I07", "I08", "I09", "I10", "J01", "J02", "J03", "J04", "J05", "J06", "J07", "J08", 
 "J09", "J10", "J11", "J12", "J13", "K01", "K02", "K03", "K04", "K05", "K06", "K07", 
 "K08", "K09", "K10", "L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08", "M01", 
 "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12", "M13", 
 "M14", "M15", "M16", "M17", "M18", "N01", "N02", "N03", "N04", "N05", "N06", "N07", 
 "N08", "N09", "N10", "N11", "N12", "P01", "P02", "P03", "P04", "Q01", "Q02", "Q03", 
 "Q04", "Q05", "Q06", "Q07", "Q08", "Q09", "Q10", "Q11", "Q12", "Q13", "Q14", "R01", 
 "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R09", "R10", "R11", "R12", "R13", 
 "R14", "R15", "R16", "R17", "S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", 
 "S09", "S10", "S11", "T01", "T02", "T03", "T04", "T05", "U01", "U02", "U03", "U04", 
 "U05", "U06", "U07", "U08", "U09", "U10", "U11", "U12", "U13", "W01", "W02", "W03", 
 "W04", "W05", "W06", "W07", "W08", "W09", "W10", "W11", "W12", "W13", "W14", "W15", 
 "W16", "W17", "W18", "W19", "W20", "W21", "W22", "W23", "W24", "W25", "W26", "W27", 
 "W28", "W29", "W30", "W31", "W32", "Y01", "Y02", "Y03", "Y04", "Y05", "Y06", "Y07", 
 "Y08", "Y09", "Y10", "Y11", "Y12", "Y13", "Y14", "Y15", "Y16", "Y17", "Y18", "Y19", 
 "Y20", "Y21", "Y22", "Y23", "Y24", "Y25", "Y26", "Y27", "Y28", "Y29", "Y30", "Z01", 
 "Z02", "Z03", "Z04", "Z05", "Z06", "Z07", "Z08", "Z09", "Z10", "Z11", "Z12", "Z13", 
 "Z14", "Z15", "Z16", "Z17", "Z18", "Z19", "Z20", "Z21", "Z22", "Z23", "Z24", "Z25", 
 "Z26", "Z27", "Z28", "Z32", "Z33", "Z34", "Z35", "Z37", "Z38", "Z39", "Z41", "Z46", 
 "Z47", "Z50", "Z51", "Z52", "Z53", "Z54", "Z55", "Z56" "Z57", "Z58"
 ]
 
ASL_FLAGS_TO_BUTTONS = {
	1 : "Left",
	2 : "Right",
	4 : "Down",
	8: "Up",
	16 : "Z", 		# 0x10
	32 : "R",		# 0x20
	64 : "L",       # 0x40
	256 : "A",      # 0x100
	512 : "B",      # 0x200
	1024 : "X",     # 0x400
	2048 : "Y",     # 0x800
	4096 : "Start"  # 0x1000
}

BRAWL_STAGE_PACS = [
 "STGBATTLEFIELD", "STGCHARAROLL", "STGCONFIGTEST", "STGCRAYON",
 "STGDOLPIC", "STGDONKEY", "STGDXBIGBLUE", "STGDXCORNERIA", "STGDXGARDEN",
 "STGDXGREENS", "STGDXONETT", "STGDXONETT", "STGDXPSTADIUM", "STGDXRCRUISE",
 "STGDXSHRINE", "STGDXYORSTER", "STGDXZEBES", "STGEARTH", "STGEDIT_0", "STGEDIT_1",
 "STGEDIT_2", "STGEMBLEM", "STGEMBLEM_00", "STGEMBLEM_01", "STGEMBLEM_02",
 "STGFAMICOM", "STGFINAL", "STGFZERO", "STGGREENHILL", "STGGW", "STGGW",
 "STGHALBERD", "STGHEAL", "STGHOMERUN", "STGHOMERUN", "STGICE", "STGJUNGLE", 
 "STGKART", "STGMADEIN", "STGMANSION", "STGMARIOPAST_00", "STGMARIOPAST_01",
 "STGMETALGEAR_00", "STGMETALGEAR_01", "STGMETALGEAR_02", "STGNEWPORK", "STGNORFAIR",
 "STGOLDIN", "STGONLINETRAINING", "STGORPHEON", "STGPALUTENA", "STGPICTCHAT",
 "STGPIRATES", "STGPLANKTON", "STGRESULT", "STGSTADIUM", "STGSTARFOX_ASTEROID",
 "STGSTARFOX_BATTLESHIP", "STGSTARFOX_CORNERIA", "STGSTARFOX_GDIFF",
 "STGSTARFOX_SPACE", "STGTARGETLV1", "STGTARGETLV2", "STGTARGETLV3", "STGTARGETLV4",
 "STGTARGETLV5", "STGTENGAN_1", "STGTENGAN_2", "STGTENGAN_3", "STGVILLAGE_00",
 "STGVILLAGE_01", "STGVILLAGE_02", "STGVILLAGE_03", "STGVILLAGE_04"
]

BRAWL_MODULES = [
 "st_battle.rel", "st_battles.rel", "st_config.rel", "st_crayon.rel", "st_croll.rel",
 "st_dolpic.rel", "st_donkey.rel", "st_dxbigblue.rel", "st_dxcorneria.rel",
 "st_dxgarden.rel", "st_dxgreens.rel", "st_dxonett.rel", "st_dxpstadium.rel", 
 "st_dxrcruise.rel", "st_dxshrine.rel", "st_dxyorster.rel", "st_dxzebes.rel", 
 "st_earth.rel", "st_emblem.rel", "st_famicom.rel", "st_final.rel", "st_fzero.rel", 
 "st_greenhill.rel", "st_gw.rel", "st_halberd.rel", "st_heal.rel", "st_homerun.rel",
 "st_ice.rel", "st_jungle.rel", "st_kart.rel", "st_madein.rel", "st_mansion.rel", 
 "st_mariopast.rel", "st_metalgear.rel", "st_newpork.rel", "st_norfair.rel", 
 "st_oldin.rel", "st_orpheon.rel", "st_otrain.rel", "st_palutena.rel",
 "st_pictchat.rel", "st_pirates.rel", "st_plankton.rel", "st_stadium.rel", 
 "st_stageedit.rel", "st_starfox.rel", "st_tbreak.rel", "st_tengan.rel", 
 "st_village.rel"
]

## End constants
## Start list functions

# Given a list of nodes with the same parent, delete those nodes using RemoveChild()
# use reverse() to avoid top-down errors
# params:
#	nodeList: any list of ResourceNodes which share a Parent
def removeChildNodes(nodeList):
	nodeList.reverse()
	parentNode = nodeList[0].Parent
	
	for node in nodeList:
		parentNode.RemoveChild(node)

def removeNode(node):
	node.Parent.RemoveChild(node)

# reverseResourceList()
# Basic impl of list.reverse() to accommodate ResourceNode lists
# params:
#	nodeList: any list of ResourceNodes
def reverseResourceList(nodeList):
	nodeListReverse = []
	for i in nodeList:
		nodeListReverse.append(i)
	
	nodeListReverse.reverse()
	return nodeListReverse

# getChildFromName()
# Given any node, return its child node whose name contains the given nameStr
# params:
#	node: Parent node to search within
#	nameStr: Name of child to search for
# 	EXACT_NEEDED: bool, whether or not name should match exactly
def getChildFromName(node, nameStr, EXACT_NEEDED=False):
	if node.Children:
		for child in node.Children:
			if EXACT_NEEDED and child.Name == str(nameStr):
				return child
			elif str(nameStr) in child.Name:
				return child
	return 0	# If not found, return 0
	
def getChildWrapperFromName(wrapper, nameStr, EXACT_NEEDED=False):
	if wrapper.Nodes:
		for child in wrapper.Nodes:
			if EXACT_NEEDED and child.Resource.Name == str(nameStr):
				return child
			elif str(nameStr) in child.Resource.Name:
				return child
	return 0	# If not found, return 0

def listToString(list):
	message = ""
	for item in list:
		message += item + "\n"
	
	return message

## End list functions
## Start node functions

# getParentArc()
# Return the "2" ARC of stage file, or 0 if not found
def getParentArc():
	if BrawlAPI.RootNode and BrawlAPI.RootNode.HasChildren:
		for i in BrawlAPI.RootNode.Children:
			if i.Name == "2" and isinstance(i, ARCNode):
				return i
	
	# If not found, show an error and return 0
	BrawlAPI.ShowError("2 ARC not found. Verify the open file is a stage .pac", "Error")
	return 0

# getChildNames()
# Return list containing group.Children node names
# params:
#	group: any node with children
def getChildNames(group):
	list = []
	for i in group.Children:
		list.append(i.Name)
	return list

def getChildNodes(node):
	if node.HasChildren:
		childrenList = []
		for i in node.Children:
			childrenList.append(i)
	
		return childrenList
	return 0
# Return true if given node is a brres, of exactly 640 bytes, and has exactly one mdl0 node
def isStaticBRRES(node):
	modelsGroup = getChildFromName(node,"3DModels")
	
	if node.UncompressedSize == 640 \
	and isinstance(node, BRRESNode) \
	and modelsGroup and modelsGroup.HasChildren and len(modelsGroup.Children) == 1:
		return True
	else:
		return False

## End node functions
## Start file operation functions

# getOpenFile()
# If a file is currently opened, return the file path, otherwise return 0

def getOpenFile():
	if BrawlAPI.RootNode:
		return str(BrawlAPI.RootNode.FilePath)
	return 0

## End file operation functions
## Start conversion functions

# Given an array of 3 numbers, return an array of 3 ints corresponding to the RGB values
# Hue in [0, 359], sat in [0,1], val in [0,1]
def HSV2RGB(colorList):
	[HUE, SAT, VAL] = colorList
	
	# Some formula calcs
	cValue = float(VAL * SAT)
	xValue = cValue * (1.0 - abs((HUE / 60.0) % 2 - 1.0))
	mValue = VAL - cValue
	
	# Keep hue value in [0, 359] range
	while HUE < 0:
		HUE = HUE + 360
	while HUE > 360:
		HUE = HUE - 360
	
	if HUE >= 0 and HUE < 60:
		[red, green, blue] = [cValue, xValue, 0]
	elif HUE >= 60 and HUE < 120:
		[red, green, blue] = [xValue, cValue, 0]
	elif HUE >= 120 and HUE < 180:
		[red, green, blue] = [0, cValue, xValue]
	elif HUE >= 180 and HUE < 240:
		[red, green, blue] = [0, xValue, cValue]
	elif HUE >= 240 and HUE < 300:
		[red, green, blue] = [xValue, 0, cValue]
	else:
		[red, green, blue] = [cValue, 0, xValue]
	
	red = int((red + mValue) * 255.0)
	green = int((green + mValue) * 255.0)
	blue = int((blue + mValue) * 255.0)
	
	return [red, green, blue]

# Given a color entry, return an array of 3 floats corresponding to the HSV values
def RGB2HSV(colorNode):
	RED = colorNode.R / 255.0
	BLUE = colorNode.B / 255.0
	GREEN = colorNode.G / 255.0
	colorMax = max(RED, BLUE, GREEN)
	colorMin = min(RED, BLUE, GREEN)
	colorDiff = colorMax - colorMin
	
	# If hue not 0, calculate hue as value 0..359
	if colorDiff == 0:
		hue = 0
	elif colorMax == RED:
		hue = ((GREEN - BLUE) / colorDiff) % 6
	elif colorMax == GREEN:
		hue = ((BLUE - RED) / colorDiff) + 2.0
	else:
		hue = ((RED - GREEN) / colorDiff) + 4.0

	hue = (hue * 60.0) % 360
	
	# Calculate saturation as [0,1]
	if colorMax > 0:
		sat = colorDiff / colorMax
	else:
		sat = 0
		
	# Calculate value (highest color) as [0,1]
	val = colorMax
	
	return [hue, sat, val]

# Given dec value, returns formatted hex value (17 -> 0x0011)
# Uses lowercase 0x prefix with uppercase hex digits
def formatHex(value, DIGIT_COUNT=4):

	# Convert to hex, and remove weird trailing L
	string = str(hex(value)).upper()[2:-1]
	
	while len(string) < DIGIT_COUNT:
		string = '0' + string
	
	return "0x" + string

## End conversion functions
## Start misc. / debug functions

# dmessage()
# Easy debug message
# params
#	msg: any string
def dmessage(msg):
	BrawlAPI.ShowMessage(str(msg), "DEBUG")

def dmsg(msg):
	dmessage(msg)
