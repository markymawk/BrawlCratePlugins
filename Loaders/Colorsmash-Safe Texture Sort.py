__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import * 
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from BrawlLib.Internal.Windows.Forms import ProgressWindow
from mawwwkLib import *

SCRIPT_NAME = "Color Smash-safe Texture Sort"
moveCount = 0

TEXTURE_GROUP_ERROR_TEXT = "Error: expand the Textures(NW4R) group within the BRRES so that the green texture nodes are visible, then try the plug-in again."

## Start enable check functions

# Check to ensure that the BRESGroup is a Texture group that contains more than 1 TEX0
# Wrapper: BRESGroupWrapper
def EnableCheckBRESGroup(sender, event_args):
	group = BrawlAPI.SelectedNode
	sender.Enabled = (group is not None and group.HasChildren and len(group.Children) > 1)

# Check to ensure that the BRES contains a Texture group that contains more than 1 TEX0
# Wrapper: BRESWrapper
def EnableCheckBRES(sender, event_args):
	group = BrawlAPI.SelectedNode
	
	if group is not None:
		textureGroup = getChildFromName(group, "Texture")
	else:
		textureGroup = 0
		
	sender.Enabled = (group is not None and textureGroup and textureGroup.HasChildren and len(textureGroup.Children) > 1)
	
## End enable check functions
## Start helper functions

# Given a parent list and wrapper child, return the ResourceNode within the wrapper at the previous index in the list
def wrapperPrevSiblingNode(list, wrapper):
	thisIndex = list.IndexOf(wrapper)
	if thisIndex > 0:
		return list[thisIndex-1].Resource
	else:
		return 0

# Given a wrapper, increment moveCount and MoveUp() the wrapper
def moveUpWrapper(wrapper):
	global moveCount
	moveCount += 1
	wrapper.MoveUp(False)

# Helper function to sort textures given the list of wrappers
def sortTextures(textureWrappers, AUTO_SAVE):
	sharesDataMoveUpCount = 0
	tex0MovedCount = 1
	inSharesDataGroup = False
	progressBar = ProgressWindow()
	progressBar.Begin(0, len(textureWrappers), 0)
	
	# Iterate through textures
	for i in range(1, len(textureWrappers), 1):
	
		# Auto-save if enabled, and only if not amid a colorsmash group
		if AUTO_SAVE and not inSharesDataGroup and tex0MovedCount >= 13:
			BrawlAPI.SaveFile()
			tex0MovedCount = tex0MovedCount % 13
		
		doLoop = True
		currentWrapper = textureWrappers[i]
		
		# Update progress bar
		progressBar.Update(i)
		progressBar.Caption = currentWrapper.Resource.Name
		
		# Sort behavior #1: If current tex0 SharesData is False, and not in a colorsmash group, use MoveUp() freely as needed
		if not currentWrapper.Resource.SharesData and not inSharesDataGroup:
			while doLoop:
			
				# Compare current tex0 name with prevSibling tex0 name
				prevWrapperNode = wrapperPrevSiblingNode(textureWrappers, currentWrapper)
				if prevWrapperNode and currentWrapper.Resource.Name.lower() < prevWrapperNode.Name.lower():
					moveUpWrapper(currentWrapper)
					tex0MovedCount += 1
					
					# If the current tex0 was moved into the middle of a colorsmash group (previous.SharesData == True), push it back to preserve the CS order
					previous = wrapperPrevSiblingNode(textureWrappers, currentWrapper)
					
					while previous and previous.SharesData:
						moveUpWrapper(currentWrapper)
						previous = wrapperPrevSiblingNode(textureWrappers, currentWrapper)
				
				# Once the current node is sorted correctly, exit the loop for this texture
				else:
					doLoop = False
		
		# Sort behavior #2: If the current texture is inside a colorsmash group (i.e. previous node was SharesData == True),
		# then MoveUp() the exact amount as the previously sorted tex0
		elif inSharesDataGroup:
			if sharesDataMoveUpCount:
				tex0MovedCount += 1
				
			# Preserve the colorsmash group. Move up x times, per sharesDataMoveUpCount
			for j in range (0, sharesDataMoveUpCount, 1):
				progressBar.Update((float(j)/sharesDataMoveUpCount) * len(textureWrappers)) # Update progress bar with current tex0 sort
				moveUpWrapper(currentWrapper)
				
			# If this node is the end of a colorsmash group (SharesData == False), revert back to the default move count afterward
			if not currentWrapper.Resource.SharesData:
				inSharesDataGroup = False
				sharesDataMoveUpCount = 0
		
		# Sort behavior #3: If at the beginning of a colorsmash group (SharesData == True), count the MoveUp() use and store in sharesDataMoveUpCount
		else:
			inSharesDataGroup = True
			while doLoop:
			
				# Compare current tex0 name with prevSibling tex0 name
				prevWrapperNode = wrapperPrevSiblingNode(textureWrappers, currentWrapper)
				if prevWrapperNode and currentWrapper.Resource.Name.lower() < prevWrapperNode.Name.lower():
					tex0MovedCount += 1
					moveUpWrapper(currentWrapper)
					sharesDataMoveUpCount += 1	# Store how many MoveUp() runs to do for the rest of the group
					
					# If the current tex0 was moved into the middle of a separate colorsmash group, push it back to preserve the other group's order
					previous = wrapperPrevSiblingNode(textureWrappers, currentWrapper)
					
					while previous and previous.SharesData:
						moveUpWrapper(currentWrapper)
						previous = wrapperPrevSiblingNode(textureWrappers, currentWrapper)
						sharesDataMoveUpCount += 1
				
				# Once the current current node is sorted correctly, exit the loop for this texture
				else:
					doLoop = False
	
	progressBar.Finish()

## End helper functions
## Start loader functions

def colorsmash_safe_sort_bresgroup(sender, event_args):
	main(BrawlAPI.SelectedNodeWrapper)

def colorsmash_safe_sort_bres(sender, event_args):

	if str(BrawlAPI.SelectedNodeWrapper.Nodes[0]) == "TreeNode: ":
		BrawlAPI.ShowError(TEXTURE_GROUP_ERROR_TEXT, "Error")
		return
	else:	
		main(getChildWrapperFromName(BrawlAPI.SelectedNodeWrapper, "Textures"))
	
## End loader functions
## Start main function

def main(parentGroupWrapper):
	TEXTURE_WRAPPERS = parentGroupWrapper.Nodes
	
	# If type is null, don't run the script
	if str(TEXTURE_WRAPPERS[0]) == "TreeNode: ":
		BrawlAPI.ShowError(TEXTURE_GROUP_ERROR_TEXT, "Error")
		return
	
	# User prompt to run
	message = "Sort textures while preserving Color Smash groups.\n\n"
	message += "This process may take 15-30 minutes OR LONGER depending on the amount of sorting needed.\n\n"
	message += "BrawlCrate may appear unresponsive in the meantime.\n\nPress OK to continue."
	if not BrawlAPI.ShowOKCancelPrompt(message, SCRIPT_NAME):
		return
	
	# User prompt to auto-save
	message = "The script can automatically save the file after every 12 sorts.\n\nEnable auto-saving? (Recommended for first run.)"
	AUTO_SAVE = BrawlAPI.ShowYesNoPrompt(message, SCRIPT_NAME)
	
	# If 2 or more textures, start the sort. (This is in EnableCheck already, but verify the wrapper count to be double-sure)
	if len(TEXTURE_WRAPPERS) >= 2:
		sortTextures(TEXTURE_WRAPPERS, AUTO_SAVE)
		
		if moveCount == 0:
			BrawlAPI.ShowMessage("Sort complete: no resorting done.", SCRIPT_NAME)
		else:
			BrawlAPI.ShowMessage("Sort complete! (" + str(moveCount) + " total moves performed)", "Success!")

## End main function
## Start context menu add

# From Textures group
BrawlAPI.AddContextMenuItem(BRESGroupWrapper, "", "Sort textures in order while preserving color smash sets", EnableCheckBRESGroup, ToolStripMenuItem("Sort Textures (Color Smash-safe)", None, colorsmash_safe_sort_bresgroup))

# From parent BRRES
BrawlAPI.AddContextMenuItem(BRESWrapper, "", "Sort textures in order while preserving color smash sets", EnableCheckBRES, ToolStripMenuItem("Sort Textures (Color Smash-safe)", None, colorsmash_safe_sort_bres))
