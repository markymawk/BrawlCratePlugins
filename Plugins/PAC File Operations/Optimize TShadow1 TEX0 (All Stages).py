__author__ = "mawwwk"
__version__ = "1.2"

from BrawlCrate.API import BrawlAPI
from BrawlLib.SSBB import FileFilters
from BrawlLib.SSBB.ResourceNodes import *
from BrawlLib.Internal import *
from BrawlLib.Internal.Windows.Forms import *
from BrawlCrate.UI import * # MainForm CompabibilityMode
from System.IO import *
from mawwwkLib import *

SCRIPT_NAME = "Replace TShadow1"
#TEX0_FILTER = "TEX0 file (*.tex0)|*.tex0"
SHADOW_TEX0_PATH = AppPath + "\\BrawlAPI\\Resources\\TShadow1.tex0"

def main():
	
	# Get stage/melee folder
	if not BrawlAPI.ShowOKCancelPrompt("Select stage/melee folder.", SCRIPT_NAME):
		return
	meleeDir = BrawlAPI.OpenFolderDialog("Select stage/melee folder.")
	if not meleeDir:
		return
	
	# Enable compatibility mode to avoid corrupting older imports
	MainForm.Instance.CompatibilityMode = True
	
	# Initialize file list and progress bar
	files = Directory.GetFiles(meleeDir)
	changedPacsCount = 0
	progressBar = ProgressWindow(MainForm.Instance, "Updating", "Replace TShadow1 texture", False)
	progressCounter = 0
	progressBar.Begin(0, len(files), progressCounter)
	
	tex0Hash = ""
	filesSkippedCount = 0
	# Loop through pac files
	for file in files:
		
		# Check whether file should be opened
		if not Path.GetFileName(file).lower().endswith(".pac"):
			continue
		
		# Attempt to open file, but skip if unable to
		if not BrawlAPI.OpenFile(file):
			continue
		
		progressBar.Caption = Path.GetFileName(file)
		parentArc = BrawlAPI.RootNode.FindChild("2")
		isShadowFound = False # Set to False for each pac
		isFileModified = False
		duplicateNodes = [] # List of duplicate TShadow TEX0 to delete in pac
		
		if not parentArc:
			BrawlAPI.ShowMessage("No 2 ARC found.","")
			continue
		
		# Loop through Texture Data brres nodes
		for brres in parentArc.Children:
			if not isinstance(brres, BRRESNode):
				continue
			if "Texture Data" not in brres.Name:
				continue
			if not brres.HasChildren:
				continue
			texturesGroup = brres.FindChild(TEX_GROUP)
			
			if not texturesGroup:
				continue
			for tex0 in texturesGroup.Children:
				if tex0.Name == "TShadow1":
					# If no TShadow1 found yet, determine whether to replace
					if not isShadowFound:
						isShadowFound = True
						
						# For first file of the run, replace and save the MD5 for future comparisons
						if tex0Hash == "":
							tex0.Replace(SHADOW_TEX0_PATH)
							tex0Hash = tex0.MD5Str()
							isFileModified = True
						# If tex0 already matches, skip it
						elif tex0.MD5Str() == tex0Hash:
							continue
						tex0.Replace(SHADOW_TEX0_PATH)
						isFileModified = True
						changedPacsCount += 1
					
					# If TShadow already found earlier, report a duplicate
					elif BrawlAPI.ShowYesNoWarning("More than 1 TShadow TEX0 found. Remove duplicate texture?", SCRIPT_NAME):
						duplicateNodes.append(tex0)
						isFileModified = True
			
			if isFileModified:
				for i in duplicateNodes:
					i.Remove(True)
				BrawlAPI.SaveFile()
			else:
				filesSkippedCount += 1
		
		# Update progress bar
		progressCounter += 1
		progressBar.Update(progressCounter)
	
	# Restore compatibility mode setting
	MainForm.Instance.CompatibilityMode = False
	
	# Results
	BrawlAPI.CloseFile()
	progressBar.Finish()
	msg = "Complete.\n"
	msg += str(changedPacsCount) + " file(s) updated"
	if filesSkippedCount:
		msg += "\n" + str(filesSkippedCount) + " files skipped (already use selected TEX0, or no TShadow found)"
	BrawlAPI.ShowMessage(msg, SCRIPT_NAME)

main()