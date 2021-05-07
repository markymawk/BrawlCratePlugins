__author__ = "mawwwk"
__version__ = "1.0.3"

from BrawlCrate.API import *
from BrawlLib.SSBB import FileFilters
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from BrawlLib.Internal.Windows.Forms import * #TextureConverterDialog
from BrawlLib.Internal.Windows.Controls import * #GoodColorControl2? DialogResult?
from BrawlLib.Wii.Textures import * #WiiPixelFormat, WiiPaletteFormat

# INFFACE_DIGIT_COUNT: Can be changed to 3 for non-50CC builds
INFFACE_DIGIT_COUNT = 4

## Begin helper methods

def addLeadingZeros(value):
	while len(str(value)) < INFFACE_DIGIT_COUNT:
		value = "0" + str(value)
	
	return str(value)

def getStartingPortraitID():
	PROMPT_STR = "e.g. \"1\" for InfFace" + addLeadingZeros("1") + ":"
	initialID = BrawlAPI.UserIntegerInput("Enter starting portrait ID", PROMPT_STR)
	
	if initialID and initialID > 0 and len(str(initialID)) <= INFFACE_DIGIT_COUNT:
		return initialID
	else:
		if initialID:
			BrawlAPI.ShowError("Invalid value entered", "Error")
		return 0
	
## End helper methods
## Start of main script

# Save currently opened file, if there is one
# If currently opened file is a BP, assume user will want the new BPs open instead
if BrawlAPI.RootNode and "InfFace" not in BrawlAPI.RootNode.Name:
	CURRENT_OPEN_FILE = str(BrawlAPI.RootNode.FilePath)
else:
	CURRENT_OPEN_FILE = 0

# Prompt for PNG file paths
images = BrawlAPI.OpenMultiFileDialog("Select battle portrait images", FileFilters.TEX0)

if images:
	OUTPUT_DIR = images[0].rsplit("\\",1)[0]

	# Take user input to determine starting InfFace file name
	INITIAL_BP_ID = getStartingPortraitID()
	
	# Reference https://soopercool101.github.io/BrawlCrate/class_brawl_crate_1_1_external_interfacing_1_1_color_smash.html#aa4fadb82e34ae150d1e94ab101399a62
	# Iterate through each image opened and export a brres containing the texture in CI8
	if INITIAL_BP_ID:
		exportedImageCount = 0
		for image in images:
			outputPath = OUTPUT_DIR + "\\InfFace" + addLeadingZeros(INITIAL_BP_ID + exportedImageCount) + ".brres"
			
			BrawlAPI.New[BRRESNode]()
			
			dlg = TextureConverterDialog()
			dlg.ImageSource = image
			dlg.Automatic = True
			dlg.StartingFormat = WiiPixelFormat.CI8
			
			if (dlg.ShowDialog(MainForm.Instance, BrawlAPI.RootNode) == dlg.DialogResult.OK):
				BrawlAPI.SaveFileAs(outputPath)
				exportedImageCount += 1

		# After exporting, open previously opened file, if it exists
		if CURRENT_OPEN_FILE:
			BrawlAPI.OpenFile(CURRENT_OPEN_FILE)
		# Otherwise, leave the last-exported BP open
		else:
			BrawlAPI.OpenFile(outputPath)

		BrawlAPI.ShowMessage(str(exportedImageCount) + " BRRES files successfully exported to\n" + OUTPUT_DIR, "Success!")