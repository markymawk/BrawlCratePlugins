# -*- coding: utf-8 -*- 
# Fixes redirect arrow character
__author__ = "mawwwk"
__version__ = "1.1"

from BrawlCrate.API import *
from BrawlCrate.UI import MainForm
from BrawlLib.SSBB.ResourceNodes import *
from System.IO import *
from mawwwkLib import *

SCRIPT_NAME = "Output Nodes to Text"
 
# getNodeProperties():
# Get specific node properties depending on the node's type, and return as string
def getNodeProperties(node, doIncludeMD5):
	nodeStr = ""
	nodeType = node.NodeType.split(".")[-1]
	nodeHash = node.MD5Str()
	uncompressedSize = node.UncompressedSize
	
	# Show MD5 if exists
	if doIncludeMD5 and len(nodeHash):
		nodeStr += "\nMD5: " + nodeHash[:8]
	
	# TEX0Node info
	if nodeType == "TEX0Node":
		nodeStr += "\n"
		if node.SharesData:
			nodeStr += "SharesData | "
		nodeStr += str(node.Width) + "x" + str(node.Height) + " | " + str(node.Format)
		if node.LevelOfDetail > 1:
			nodeStr += " | LevelOfDetail: " + str(node.LevelOfDetail)
	
	# ARCNode info
	elif nodeType == "ARCNode":
		compression = str(node.Compression)
		if compression != "None":
			nodeStr += "\nCompression: " + compression
	
	# MDL0Node info
	elif nodeType == "MDL0Node":
		nodeStr += "\nFacepoints: " + str(node.NumFacepoints) \
		+ " | Verts: " + str(node.NumVertices) \
		+ " | Tris: " + str(node.NumTriangles) \
		+ " | Nodes: " + str(node.NumNodes)
	
	# MDL0BoneNode info
	elif nodeType == "MDL0BoneNode":
		nodeStr += "\nScale: " + str(node.Scale) \
		+ " | Rotation: " + str(node.Rotation) \
		+ " | Translation: " + str(node.Translation) \
		+ "\nFlags: " + str(node.Flags)
	
	# MDL0Material info
	elif nodeType == "MDL0MaterialNode":
		nodeStr += "\n" + str(node.CullMode) + ", " + str(node.Shader) + ", LightSet " + str(node.LightSetIndex) + ", Fog " + str(node.FogIndex)
	
	# Animation info (or SCN0Node)
	elif nodeType in ["CHR0Node", "CLR0Node", "SRT0Node", "VIS0Node", "PAT0Node", "SCN0Node"]:
		nodeStr += "\nFrameCount: " + str(node.FrameCount) + " | Loop: " + str(node.Loop)
	
	# STPMEntryNode info
	elif nodeType == "STPMEntryNode":
		nodeStr += "\nShadowPitch: " + str(node.ShadowPitch) + " | ShadowYaw: " + str(node.ShadowYaw)
	
	# SCN0LightSetNode info
	elif nodeType == "SCN0LightSetNode":
		lightSetString = "\n"
		lightSetUsed = False
		for i in ["Ambience", "Light0", "Light1", "Light2", "Light3", "Light4", "Light5", "Light6", "Light7"]:
			lightName = str(getattr(node, i))
			if lightName != "None":
				lightSetUsed = True
				lightSetString += i + ": " + lightName + " | "
		
		if lightSetUsed:
			nodeStr += lightSetString[:-2]
	
	# CollisionObject info
	# Show uncompressedSize if size > 0
	if uncompressedSize:
		nodeStr += "\nUncompressedSize: " + str(uncompressedSize)
	return nodeStr + "\n"

# writeOutput():
# Recursive method to write node info to text file, then call for each child node
def writeOutput(node, textFile, doIncludeMD5, prefixStr=""):
	writeStr = prefixStr + node.Name + "\n" + node.NodeType.split(".")[-1]
	writeStr += getNodeProperties(node, doIncludeMD5)
	# Replace redirect arrow, has ascii issues
	textFile.write(writeStr.replace("→",">") + "\n")
	# Recursively check child nodes
	if node.HasChildren:
		for child in node.Children:
			writeOutput(child, textFile, doIncludeMD5, prefixStr + node.Name + "/")

def main():
	if BrawlAPI.SelectedNode is None:
		showMsg("No file opened", "Error")
		return
	
	# Show user prompt and get output directory
	msg = "Write properties of the selected node and all child nodes to a text file.\n\nPress OK to choose a folder."
	prompt = showMsg(msg, SCRIPT_NAME, 1)
	if not prompt:
		return
	
	OUTPUT_DIR = BrawlAPI.OpenFolderDialog("Select output folder")
	if not OUTPUT_DIR:
		return
	
	selNode = BrawlAPI.SelectedNode
	
	# Filename stuff: Remove spaces, brackets, parentheses
	defaultName = selNode.Name.translate({ ord(c): None for c in " []()→" })
	
	# Use first 10 chars of filename + first 13 chars of selected node (Enough for ModelDataXXX and TextureDataXX)
	suggestedFileName = BrawlAPI.RootNode.FileName[:10] + "_" + defaultName[:13] + "_md5.txt"
	outputTextFileName = BrawlAPI.UserStringInput("Enter output .txt file name", suggestedFileName)
	
	if not outputTextFileName.endswith(".txt"):
		outputTextFileName += ".txt"
	
	msg = "Include MD5 checksums in output?"
	doIncludeMD5 = BrawlAPI.ShowYesNoPrompt(msg, SCRIPT_NAME)
	
	FULL_TEXT_FILE_PATH = str(OUTPUT_DIR) + "\\" + outputTextFileName
	TEXT_FILE = open(FULL_TEXT_FILE_PATH,"w+", encoding="utf-8")

	writeOutput(selNode, TEXT_FILE, doIncludeMD5)
	
	TEXT_FILE.close()
	
	msg = "Node data written to\n" + FULL_TEXT_FILE_PATH
	showMsg(msg, "Success!")

main()
