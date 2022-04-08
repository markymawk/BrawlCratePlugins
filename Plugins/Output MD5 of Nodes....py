__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.UI import MainForm
from BrawlLib.SSBB.ResourceNodes import *
from System.IO import *
from mawwwkLib import *

SCRIPT_NAME = "Output MD5 of Nodes"
# Directory path of files to open. Use AppPath for BrawlCrate install folder
FILE_DIR_PATH = "C:\\Users\\m\\Desktop\\"

def writeOutput(node, textFile, prefixStr=""):
	writeStr = prefixStr + node.Name + "\n" + str(type(node))[7:-2] + "\n" + node.MD5Str()[:16] + "\n"
	textFile.write(writeStr + "\n")
	
	# Recursively check child nodes
	if node.HasChildren:
		for child in node.Children:
			writeOutput(child, textFile, prefixStr + node.Name + "/")
	
	# Can add type checks in this function for more specialized info, i.e. bone flags, texture properties
	#if isinstance(node, type):
	#	...

def main():
	if BrawlAPI.SelectedNode is None:
		showMsg("No file opened", "Error")
		return
	
	# Show user prompt and get output directory
	msg = "Output MD5 checksum of the selected node and all child nodes to a text file.\n\nPress OK to choose a folder."
	prompt = showMsg(msg, SCRIPT_NAME, 1)
	if not prompt:
		return
	
	OUTPUT_DIR = BrawlAPI.OpenFolderDialog("Select output folder")
	if not OUTPUT_DIR:
		return
	
	selNode = BrawlAPI.SelectedNode
	
	# Filename stuff: Remove spaces and brackets
	outputTextFileName = selNode.Name.translate({ ord(c): None for c in " []" })
	# Use first 10 chars of filename + first 13 chars of selected node (Enough for ModelDataXXX and TextureDataXX)
	outputTextFileName = BrawlAPI.RootNode.FileName[:10] + "_" + outputTextFileName[:13] + "_md5.txt"
	FULL_TEXT_FILE_PATH = str(OUTPUT_DIR) + "\\" + outputTextFileName
	TEXT_FILE = open(FULL_TEXT_FILE_PATH,"w+")

	writeOutput(selNode, TEXT_FILE)
	
	TEXT_FILE.close()
	
	msg = "File hashes output to\n" + FULL_TEXT_FILE_PATH
	showMsg(msg, "Success!")

main()
