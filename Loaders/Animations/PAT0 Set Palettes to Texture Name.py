__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

## Start enable check functions
# Wrapper: PAT0TextureNode
def EnableCheckPAT0TextureNode(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None and node.HasChildren

# Wrapper: PAT0EntryNode
def EnableCheckPAT0EntryNode(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None and node.HasChildren

# Wrapper: PAT0Node
def EnableCheckPAT0Node(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = node is not None and node.HasChildren

## End enable check functions
## Start helper functions

def setFramePalettes(node):
	if not node.HasPalette:
		BrawlAPI.ShowError("HasPalette = False for animation: " + node.Parent.Name + "/" + node.Name + "\n\nSet HasPalette to True, then try again.", "Error")
		return
	for frame in node.Children:
		frame.Palette = frame.Texture
		
## End main functions
## Start loader functions

# Texture0
def match_palette_names_texturenode(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	setFramePalettes(selNode)

# Material (lambert117)
def match_palette_names_entrynode(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	if selNode.HasChildren:
		for texEntry in selNode.Children:
			setFramePalettes(texEntry)

# PAT0 root
def match_palette_names_pat0node(sender, event_args):
	selNode = BrawlAPI.SelectedNode
	if selNode.HasChildren:
		for mat in selNode.Children:
			if mat.HasChildren:
				for texEntry in mat.Children:
					setFramePalettes(texEntry)

## End loader functions
## Start context menu add

# From Texture0, etc.
BrawlAPI.AddContextMenuItem(PAT0TextureWrapper, "", "Set all frames' palettes to texture name", EnableCheckPAT0TextureNode, ToolStripMenuItem("Match all palette names", None, match_palette_names_texturenode))

# From material (lambert117) etc.
BrawlAPI.AddContextMenuItem(PAT0EntryWrapper, "", "Set all frames' palettes to texture name", EnableCheckPAT0EntryNode, ToolStripMenuItem("Match all palette names", None, match_palette_names_entrynode))

# From pat0 root
BrawlAPI.AddContextMenuItem(PAT0Wrapper, "", "Set all frames' palettes to texture name", EnableCheckPAT0Node, ToolStripMenuItem("Match all palette names", None, match_palette_names_pat0node))