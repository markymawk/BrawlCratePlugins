version = "1.8"
# mawwwkLib
# Common functions for use with BrawlAPI scripts

# i don't like naming things after myself but eh

from BrawlCrate.API import *	# BrawlAPI
from BrawlCrate.API.BrawlAPI import AppPath
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib import * # Imaging
from BrawlLib.Imaging import * # Imaging, ARGBPixel
from BrawlLib.Internal import * # Vector2, Vector3 etc
from BrawlLib.SSBB.Types import * # BoneFlags
from BrawlLib.Wii.Animations import * # KeyframeCollection
from BrawlLib.SSBB.ResourceNodes.MatTextureMinFilter import * # Mipmaps
from BrawlLib.SSBB.ResourceNodes import GXColorSrc # Material colors
from System.IO import * # File, Directory
import math

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

## CHR keyframe ArrayIndex shortcuts
scaleX = 0
scaleY = 1
scaleZ = 2
rotX = 3
rotY = 4
rotZ = 5
transX = 6
transY = 7
transZ = 8

# BRRES group name shortcuts
MDL_GROUP = "3DModels(NW4R)"
CHR_GROUP = "AnmChr(NW4R)"
VIS_GROUP = "AnmVis(NW4R)"
CLR_GROUP = "AnmClr(NW4R)"
PAT_GROUP = "AnmTexPat(NW4R)"
SRT_GROUP = "AnmTexSrt(NW4R)"
TEX_GROUP = "Textures(NW4R)"
PLT_GROUP = "Palettes(NW4R)"
SHP_GROUP = "AnmShp(NW4R)"

BLACK = ARGBPixel(255, 0, 0, 0)
WHITE = ARGBPixel(255, 255, 255, 255)

LINEAR_MIPMAP = MatTextureMinFilter.Linear_Mipmap_Linear

## End constants
## Start list functions

# reverseResourceList()
# Basic implementation of list.reverse() to accommodate ResourceNode lists
# params:
#	nodeList: any list of ResourceNodes
def reverseResourceList(nodeList):
	nodeListReverse = []
	for i in nodeList:
		nodeListReverse.append(i)
	
	nodeListReverse.reverse()
	return nodeListReverse

# findChildByName()
# Given any node, search for a child node whose name contains the given nameStr
 
def findChildByName(node, nameStr, EXACT_NEEDED=False):
	if node.Children:
		for child in node.Children:
			if EXACT_NEEDED and child.Name == str(nameStr):
				return child
			elif not EXACT_NEEDED and str(nameStr) in child.Name:
				return child
	return 0	# If not found, return 0

# findChildWrapperByName()
# Given any nodeWrapper, return its child wrapper whose Resource.Name contains the given nameStr
def findChildWrapperByName(wrapper, nameStr, EXACT_NEEDED=False):
	if wrapper.Nodes:
		for child in wrapper.Nodes:
			if EXACT_NEEDED and child.Resource.Name == str(nameStr):
				return child
			elif str(nameStr) in child.Resource.Name:
				return child
	return 0	# If not found, return 0

# nodeListToString()
# Return a string containing the names of nodes inside the given list, one per line
def nodeListToString(nodeList, max=0):
	nodeNames = getNodeNames(nodeList)
	return listToString(nodeNames, max)

def listNoDuplicates(list):
	newList = []
	for item in list:
		if item not in newList:
			newList.append(item)
	return newList

def getNodeNames(nodeList):
	newList = []
	for node in nodeList:
		newList.append(node.Name)
	
	return newList

# listToString()
# Return a string containing the (str) items of the given list, one per line
def listToString(list, max=0):
	message = ""
	# If max is negative, throw error
	if max < 0:
		dmsg("listToString() maximum cannot be negative")
		return listToString(list)
	
	# If maximum set and list exceeds maximum, list only the max count of items
	elif max and len(list) > max:
		for i in range(max):
			message += list[i] + "\n"
		message += "...and " + str(len(list) - max) + " more." 
		
	# If no maximum set, list all items
	else:
		for item in list:
			message += item + "\n"
	
	return message

def listToStringNoDuplicates(list, max=0):
	newList = listNoDuplicates(list)	
	return listToString(newList, max)

def getParentFolderPath(filepath):
	path = filepath.rsplit("\\",1)[0] + "\\"
	return path

# Shortcut for System.IO Directory.GetFiles()
# If fileStr passed, return list[] of files in directory containing given string
def getFiles(dirPath, fileStr=0):
	if not fileStr:
		return Directory.GetFiles(dirPath)
	
	fileList = []
	for fileName in Directory.GetFiles(dirPath):
		if fileStr and fileStr in fileName:
			fileList.append(fileName)
	
	return fileList

## End list functions
## Start node functions

def clearTangents(chr0Entry):
	setAllTangents(chr0Entry, 0)

def setAllTangents(chr0Entry, newTangent=0):
	# If a CHR0 animation, run on all children
	if isinstance(chr0Entry, CHR0Node) and chr0Entry.HasChildren:
		for entry in chr0Entry.Children:
			setAllTangents(entry, newTangent)
		return
	for i in range(9):
		setSingleTangent(chr0Entry, i, newTangent)

# Given source entry, offset all keyframes in destEntry ahead by the amount frameDifference
# Still experimental
def shiftAnimation(sourceEntry, destEntry, frameDifference):
	frameCount = sourceEntry.Parent.FrameCount
	clearCHR(destEntry)
	# Set every value on every frame, then clean unused frames later
	for arrayIndex in range(9):
		currentTangent = 0
		
		for i in range(frameCount):
			# Get source keyframe
			sourceKf = sourceEntry.GetKeyframe(arrayIndex, i)
			# Update tangents if set on current frame
			if sourceKf:
				currentTangent = sourceKf._tangent
				
			# Get new value and set at new frame index
			frameValue = sourceEntry.GetFrameValue(arrayIndex, i)
			newFrameIndex = (i + frameDifference) % frameCount
			destKf = destEntry.SetKeyframe(arrayIndex, newFrameIndex, frameValue)
			
			destKf._tangent = currentTangent
	
	destEntry.Parent.FrameCount = frameCount
	cleanCHR(destEntry, 0.0015)

# animSharpTangents()
# Create keyframes in a chr0 entry with straight tangents, by adding keyframes at indices (startFrame+1) and (endFrame-1)
def animSharpTangents(chr0Entry, arrayIndex, startFrame, endFrame, startVal, endVal=None):
	if (endFrame - startFrame <= 1):
		dmsg("Lib animSharpTangents: No frame difference")
		return
	
	if endVal == None:
		endVal = startVal
	# If CHR0 node, run on all children
	if isinstance(chr0Entry, CHR0Node):
		for entry in chr0Entry.Children:
			animSharpTangents(entry, arrayIndex, startFrame, endFrame, startVal, endVal)
		return
	# Value change per frame
	tangent = (endVal - startVal) / (endFrame - startFrame)
	
	# Start and end keyframes
	kfStart = chr0Entry.SetKeyframe(arrayIndex, startFrame, startVal, True) # True forceNoGenTans
	kfEnd = chr0Entry.SetKeyframe(arrayIndex, endFrame, endVal, True)
	
	# Create keyframe at startFrame+1
	val = startVal + tangent
	kf1 = chr0Entry.SetKeyframe(arrayIndex, startFrame+1, val, True)
	
	# Create keyframe at endFrame-1
	val = endVal - tangent
	kf2 = chr0Entry.SetKeyframe(arrayIndex, endFrame-1, val, True)
	#kf2._tangent = tangent
	
	for kf in [kfStart, kfEnd, kf1, kf2]:
		kf._tangent = tangent
	
# setSingleTangent()
# Applies given value to all frames, only for a given index (translation X, rot Y, etc.)
def setSingleTangent(chr0Entry, tangentIndex, newTangent=0):
	
	# If a CHR0 animation, run on all children
	if isinstance(chr0Entry, CHR0Node) and chr0Entry.HasChildren:
		for entry in chr0Entry.Children:
			setSingleTangent(entry, tangentIndex, newTangent)
		return
	
	chr0 = chr0Entry.Parent
	frameCount = chr0.FrameCount
	if chr0.Loop:
		frameCount = frameCount + 1
	
	# Don't change tangents for 1-frame animations
	isMultipleFrames = False
	for k in range(frameCount):
		
		frame = chr0Entry.GetKeyframe(tangentIndex, k)
		
		if "None" in str(type(frame)):
			continue
		
		# Store tangent of first frame
		if k == 0:
			frame0Tangent = frame._tangent
		isMultipleFrames = (k > 0)
		frame._tangent = newTangent
		
	# If only 1 frame in the animation, restore its original tangent
	firstFrame = chr0Entry.GetKeyframe(tangentIndex, 0)
	
	if isMultipleFrames:
		chr0Entry.IsDirty = True
	elif firstFrame:
		firstFrame._tangent = frame0Tangent

# clearCHR()
# Remove all keyframes from a CHR0 or CHR0Entry node
def clearCHR(chr0Entry):
	# If a CHR0 animation, run on all children
	if isinstance(chr0Entry, CHR0Node) and chr0Entry.HasChildren:
		for entry in chr0Entry.Children:
			clearCHR(entry)
		return
	
	# Clear keyframes from entry nodes
	
	frameCount = chr0Entry.Parent.FrameCount
	if chr0Entry.Parent.Loop:
		frameCount += 1
	for i in range(frameCount):
		chr0Entry.RemoveKeyframe(i)

# cleanCHR()
# Remove redundant keyframes within a given interval
def cleanCHR(entry, interval=0.001):
	
	keyframesRemovedCount = 0
	
	# If parameter is CHR0 node, run on all child entries
	if isinstance (entry, CHR0Node):
		for chr0Entry in entry.Children:
			keyframesRemovedCount += cleanCHR(chr0Entry, interval)
		return keyframesRemovedCount
	
	frameCount = entry.Parent.FrameCount
	entry._generateTangents = False
	entry.IsDirty = True
	
	# Loop through CHR array indices (scale, rot, trans)
	for i in range(9):
		
		# Loop through frames
		for frameIndex in range(1, frameCount+1):
			keyframe = entry.GetKeyframe(i, frameIndex)
			
			# Ignore blank keyframes
			if keyframe == None:
				continue
			
			# Save value then remove it
			tangent = keyframe._tangent
			value = keyframe._value
			entry.RemoveKeyframe(i, frameIndex)
			
			blankValue = entry.GetFrameValue(i, frameIndex)
			minVal = blankValue - interval
			maxVal = blankValue + interval
			
			inRemovableRange = value >= minVal and value <= maxVal
			
			if inRemovableRange:
				keyframesRemovedCount += 1
			# If value differs too greatly, restore the keyframe value
			else:
				# Last true = don't regenerate tangents
				restoredKeyframe = entry.SetKeyframe(i, frameIndex, value, True)
				restoredKeyframe._tangent = tangent
	
	return keyframesRemovedCount

def setMips(mdl0):
	if mdl0.FindChild("Materials"):
		for mat in mdl0.FindChild("Materials").Children:
			for matEntry in mat.Children:
				matEntry.MinFilter = LINEAR_MIPMAP

# Return the first brres with a FileIndex matching the given id
def getBRRES(parentNode, id):
	for child in parentNode.Children:
		if child.FileIndex == id:
			return child
	else:
		dmsg("Lib getBRRES() index error")
		return 0

# Return the CHR at index chrID of the given brres ID
def getCHR(parentNode, brresID, chrID=0):
	brres = getBRRES(parentNode, brresID)
	if brres and brres.FindChild(CHR_GROUP):
		return brres.FindChild(CHR_GROUP).Children[chrID]
	else:
		dmsg("Lib getCHR() index error")
		return 0

# Return the Children[chrID] entry of the given getCHR()
def getCHREntry(parentNode, brresID, childID=0, chrID=0):
	chr = getCHR(parentNode, brresID)
	if chr and chr.HasChildren:
		return chr.Children[childID]
	else:
		dmsg("Lib getCHREntry() index error")
		return 0
	
# Return the CLR at index clrID of the given brres ID
def getCLR(parentNode, brresID, clrID=0):
	brres = getBRRES(parentNode, brresID)
	if brres and brres.FindChild(CLR_GROUP):
		return brres.FindChild(CLR_GROUP).Children[clrID]
	else:
		dmsg("Lib getCLR() index error")
		return 0

# Create a new CHR with the new frame count, then replace the source CHR with that new one
def resizeCHR(chr0Node, newFrameCount=-1):
	
	# If no frame count entered, prompt for one
	if newFrameCount == -1:
		newFrameCount = BrawlAPI.UserIntegerInput("Resize CHR0", "New frame count:")
		if newFrameCount == 0:
			return
	
	# If run on a brres, run on the topmost CHR0 node
	if isinstance(chr0Node, BRRESNode):
		wrapper = getWrapperFromNode(chr0Node)
		wrapper.Expand()
		chr0Node = chr0Node.FindChild(CHR_GROUP).Children[0]
	
	# If run on CHR0 entry node, change to parent
	elif isinstance(chr0Node, CHR0EntryNode):
		chr0Node = chr0Node.Parent
	
	# Expand wrappers
	wrapper = getWrapperFromNode(chr0Node.Parent)
	wrapper.Expand()
	# Set frame count, but quit if no resize is done
	oldFrameCount = chr0Node.FrameCount
	if newFrameCount == oldFrameCount:
		return
	
	# Duplicate CHR0 node
	chr0Wrapper = getWrapperFromNode(chr0Node)
	newCHR0 = chr0Wrapper.Duplicate()
	newCHR0.Name = chr0Node.Name
	newCHR0.FrameCount = newFrameCount
	
	# Add loop frame
	if chr0Node.Loop:
		oldFrameCount += 1
		newFrameCount += 1
	
	ratio = newFrameCount / oldFrameCount
	
	# Loop through entries in source CHR0
	for sourceEntry in chr0Node.Children:
		
		# Get destination entry in new CHR0 and clear keyframes
		destEntry = newCHR0.FindChild(sourceEntry.Name)
		for i in range(newFrameCount):
			destEntry.RemoveKeyframe(i)
		
		# Loop through source frames
		for frameIndex in range(oldFrameCount):
			newFrame = round(frameIndex * ratio)
			
			# Loop through array indices
			for i in range(9):
				keyframe = sourceEntry.GetKeyframe(i, frameIndex)
				
				if keyframe:
					destEntry.SetKeyframe(i, newFrame, keyframe._value)
	
	chr0Node.Replace(newCHR0)
	removeNode(newCHR0)

# removeChildNodes()
# Given a list of nodes with the same parent, delete those nodes using RemoveChild()
# use reverse() to avoid top-down errors
# params:
#	nodeList: any list of ResourceNodes which share a Parent
def removeChildNodes(nodeList):
	nodeList.reverse()
	parentNode = nodeList[0].Parent
	
	for node in nodeList:
		parentNode.RemoveChild(node)

# removeNode()
# Use Parent.RemoveChild() to remove the given node
def removeNode(node):
	node.Parent.RemoveChild(node)

def clearBoneFlags(node):
	# If bone, clear bone flags
	if isinstance(node, MDL0BoneNode):
		node._boneFlags = node._boneFlags and BoneFlags.Visible
		node.IsDirty = True
	# If MDL0, clear all child bone flags
	elif isinstance(node, MDL0Node):
		boneGroup = node.FindChild("Bones")
		for bone in boneGroup.GetChildrenRecursive():
			clearBoneFlags(bone)
# getParentArc()
# Return the parent ARCNode of the given node, or the RootNode if reached
def getParentArc(node):
	if node == BrawlAPI.RootNode:
		return node
	if isinstance(node.Parent, ARCNode):
		return node.Parent
	else:
		return getParentArc(node.Parent)

# getChildNames()
# Return list containing group.Children node names
def getChildNames(group):
	list = []
	for i in group.Children:
		list.append(i.Name)
	return list

# getChildNodes()
# Return python list of child nodes, to avoid BrawlCrate ordering conflicts
def getChildNodes(node):
	if node.HasChildren:
		childrenList = []
		for i in node.Children:
			childrenList.append(i)
	
		return childrenList
	return 0

# getModelFromBone()
# Given a bone node, return its parent MDL0 node
def getMDL0FromBone(bone):
	if isinstance(bone.Parent, MDL0Node):
		return bone.Parent
	else:
		return getMDL0FromBone(bone.Parent)

# getWrapperFromNode()
# Given a node, return its corresponding wrapper by navigating index values from the RootNode
def getWrapperFromNode(node):
	indexList = []

	# Append node index to list
	while node.Parent and node.Index > -1:
		indexList.append(node.Index)
		node = node.Parent
	
	# Reverse list so it goes in order of parent to child
	indexList.reverse()
	
	wrapper = BrawlAPI.RootNodeWrapper
	for i in range(len(indexList)):
		childIndex = indexList[i]
		wrapper = wrapper.Nodes[childIndex]
	return wrapper

## End node functions
## Start file operation functions

# getOpenFile()
# If a file is currently opened, return the file path, otherwise return 0
def getOpenFile():
	if BrawlAPI.RootNode:
		return str(BrawlAPI.RootNode.FilePath)
	return 0

## End file operation functions
## Start math/conversion functions

def mathDist(p, q):
	distance = math.sqrt( ((p[0] - q[0]) ** 2.0) + ((p[1] - q[1]) ** 2.0) )
	return abs(distance)

def addLeadingZeros(value, count):
	while len(str(value)) < count:
		value = "0" + str(value)
	
	return str(value)

# listToARGBPixel()
# Given a list[] of numbers as HSV, return an ARGBPixel object
def listToARGBPixel(hsvList, alpha=255):
	hue = hsvList[0]
	sat = hsvList[1]
	val = hsvList[2]
	return HSVtoARGBPixel(hue, sat, val, alpha)

# HSVtoARGBPixel()
# Given a list of 3 numbers as HSV, return an ARGBPixel object
def HSVtoARGBPixel(h, s, v, alpha=255):
	RGBColors = HSV2RGB([h, s, v])
	return ARGBPixel(alpha, RGBColors[0], RGBColors[1], RGBColors[2])

# HSV2RGB()
# Given a list of 3 numbers as HSV, return a list of 3 ints corresponding to the RGB values
# Hue in [0, 359], sat in [0, 100], val in [0, 100]
def HSV2RGB(colorList):
	[hue, sat, val] = colorList
	
	# Keep brightness and sat values in [0, 100 range]
	sat = min(max(sat, 0), 100)
	val = min(max(val, 0), 100)
	
	# Keep hue value in [0, 359] range
	while hue < 0:
		hue = hue + 360
	hue = hue % 360
	
	# RGB formula calculations
	cValue = float(val * sat) / 10000.0
	xValue = cValue * (1.0 - abs((hue / 60.0) % 2 - 1.0))
	mValue = val/100.0 - cValue
	
	if hue >= 0 and hue < 60:
		[red, green, blue] = [cValue, xValue, 0]
	elif hue >= 60 and hue < 120:
		[red, green, blue] = [xValue, cValue, 0]
	elif hue >= 120 and hue < 180:
		[red, green, blue] = [0, cValue, xValue]
	elif hue >= 180 and hue < 240:
		[red, green, blue] = [0, xValue, cValue]
	elif hue >= 240 and hue < 300:
		[red, green, blue] = [xValue, 0, cValue]
	else:
		[red, green, blue] = [cValue, 0, xValue]
	
	red = round((red + mValue) * 255.0)
	green = round((green + mValue) * 255.0)
	blue = round((blue + mValue) * 255.0)
	
	return [red, green, blue]

# RGB2HSV()
# Given a color node (frame), return a list of 3 floats corresponding to the HSV values
def RGB2HSV(colorNode):
	red = colorNode.R / 255.0
	blue = colorNode.B / 255.0
	green = colorNode.G / 255.0
	colorMax = max(red, blue, green)
	colorMin = min(red, blue, green)
	colorDiff = colorMax - colorMin
	
	# Calculate hue as value [0, 360)
	if colorDiff == 0:
		hue = 0
	elif colorMax == red:
		hue = ((green - blue) / colorDiff) % 6
	elif colorMax == green:
		hue = ((blue - red) / colorDiff) + 2.0
	else:
		hue = ((red - green) / colorDiff) + 4.0

	hue = (hue * 60.0) % 360
	
	# Calculate saturation as [0, 100]
	if colorMax > 0:
		sat = colorDiff / colorMax * 100
	else:
		sat = 0
		
	# Calculate value (highest color) as [0,100]
	val = colorMax * 100
	
	return [hue, sat, val]

# setColorGradient()
# Set a gradient color blend in a given color node, using frame start/end indices, and start/end ARGBPixel colors
def setColorGradient(node, startFrame, endFrame, startColor, endColor=-1):
	# If given a CLR0Node, run on all children
	if isinstance(node, CLR0Node):
		for clr0Material in node.Children:
			for clr0MatEntry in clr0Material.Children:
				setColorGradient(clr0MatEntry, startFrame, endFrame, startColor, endColor)
		return
	
	# If endColor not set, match startColor
	if endColor == -1:
		endColor = startColor
	
	# If endFrame is -1, set to last frame
	if endFrame == -1:
		endFrame = node.Parent.Parent.FrameCount - 1
	count = endFrame - startFrame
	
	# Calculate color change per frame
	if (count == 0):
		[stepA, stepR, stepG, stepB] = [0, 0, 0, 0]
	else:
		stepA = (endColor.A - startColor.A) / ((float) (count))
		stepR = (endColor.R - startColor.R) / ((float) (count))
		stepG = (endColor.G - startColor.G) / ((float) (count))
		stepB = (endColor.B - startColor.B) / ((float) (count))
	
	# Set frames in range
	for i in range(0, count+1):
		frame = i + startFrame
		newA = round(startColor.A + i * stepA)
		newR = round(startColor.R + i * stepR)
		newG = round(startColor.G + i * stepG)
		newB = round(startColor.B + i * stepB)
		
		p = ARGBPixel(newA, newR, newG, newB)
		node.SetColor(frame, frame, p)
	
	# Force last frame to ignore calculations and match endColor exactly
	node.SetColor(endFrame, endFrame, endColor)

# setMirrorGradient()
# Set a gradient color blend that goes Color A > Color B > Color A
def setMirrorGradient(node, startColor, endColor):
	# If given a CLR0Node, run on all children
	if isinstance(node, CLR0Node):
		for clr0Material in node.Children:
			for clr0MatEntry in clr0Material.Children:
				setMirrorGradient(clr0MatEntry, startColor, endColor)
		return
	
	
	# Determine middle and ending points
	midPoint = round((node.Parent.Parent.FrameCount - 1)/2)
	
	setColorGradient(node, 0, midPoint, startColor, endColor)
	
	# Get new start color from frames[1]
	newStartColor = node.GetColor(1, 0)
	setColorGradient(node, midPoint, -1, endColor, newStartColor)

# formatHex()
# Given dec value, returns formatted hex value (17 -> 0x0011)
# Uses lowercase 0x prefix with uppercase hex digits
def formatHex(value, MIN_DIGIT_COUNT=4):

	# Convert to hex, and remove Python formatted "0X"
	hexString = str(hex(value)).upper()[2:]
	hexString.replace("L","") # Only needed for certain python versions
	while len(hexString) < MIN_DIGIT_COUNT:
		hexString = '0' + hexString
	
	return "0x" + hexString

## End conversion functions
## Start misc. / debug functions

def savePreviewSettings():
	return [MainForm.Instance.ShowBRRESPreviews, MainForm.Instance.ShowARCPreviews]

def restorePreviewSettings(settings):
	MainForm.Instance.ShowBRRESPreviews = settings[0]
	MainForm.Instance.ShowARCPreviews = settings[1]
	
# dmsg()
# Easy message

def dmsg(msg, title=""):
	BrawlAPI.ShowMessage(str(msg), title)
