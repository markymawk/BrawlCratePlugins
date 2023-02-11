__author__ = "mawwwk"
__version__ = "1.0"

from BrawlCrate.API import *
from mawwwkLib import *

if BrawlAPI.SelectedNode is not None:
	showMsg(BrawlAPI.SelectedNode.MD5Str()[:8],"MD5 Checksum")
else:
	showMsg("No node selected")