__author__ = "mawwwk"
__version__ = "1.0.1"

from mawwwkLib import *

if BrawlAPI.SelectedNode is not None:
	BrawlAPI.ShowMessage(BrawlAPI.SelectedNode.MD5Str()[:8], "MD5 of Selected Node")
else:
	BrawlAPI.ShowMessage("No node selected")