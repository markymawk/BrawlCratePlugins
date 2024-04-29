__author__ = "mawwwk"
__version__ = "1.0.1"

from BrawlCrate.API import *
from BrawlCrate.NodeWrappers import *
from BrawlLib.SSBB.ResourceNodes import *
from System.Windows.Forms import ToolStripMenuItem
from mawwwkLib import *

# Check that group has Palettes in name
# Wrapper: BRESGroupWrapper
def EnableCheckGroupWrapper(sender, event_args):
	node = BrawlAPI.SelectedNode
	sender.Enabled = (node is not None and "Palettes(" in node.Name and node.HasChildren)

def import_plt0(sender, event_args):
	plt0Files = BrawlAPI.OpenMultiFileDialog("Select PLT0 files", "Palettes (*.plt0)|*.plt0")
	if not plt0Files:
		return
	
	basePalette = BrawlAPI.SelectedNodeWrapper.Nodes[0]
	
	# Loop through PLT0 files to add
	for file in plt0Files:
		# Get file name to rename palette
		fileName = file.split("\\")[-1][:-5]
		# Duplicate base palette, rename, and replace
		newPLT0 = basePalette.Duplicate()
		newPLT0.Name = fileName
		newPLT0.Replace(file)

## End loader function
## Start context menu add

BrawlAPI.AddContextMenuItem(BRESGroupWrapper, "", "Import palettes from external PLT0 files", EnableCheckGroupWrapper, ToolStripMenuItem("Import PLT0 files...", None, import_plt0))
