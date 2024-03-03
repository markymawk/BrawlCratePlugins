__author__ = "mawwwk"
__version__ = "1.1"

from BrawlCrate.API import *
from BrawlLib.SSBB import FileFilters
from BrawlLib.SSBB.ResourceNodes import *
from BrawlCrate.UI import MainForm
from BrawlLib.Internal import *
from BrawlLib.Internal.Windows.Forms import * #TextureConverterDialog
from BrawlLib.Internal.Windows.Controls import * #GoodColorControl2? DialogResult?
from BrawlLib.Wii.Textures import * #WiiPixelFormat, WiiPaletteFormat
from mawwwkLib import *

## Reference for using automatic dialog box:
## https://soopercool101.github.io/BrawlCrate/class_brawl_crate_1_1_external_interfacing_1_1_color_smash.html#aa4fadb82e34ae150d1e94ab101399a62

# INFFACE_DIGIT_COUNT: Can be changed to 3 for non-50CC builds
INFFACE_DIGIT_COUNT = 4


def main():
	initialOpenedFile = 0
	
	# Save currently opened file, if there is one
	# If currently opened file is a BP, assume user will want the new BPs open instead
	if BrawlAPI.RootNode and "InfFace" not in BrawlAPI.RootNode.Name:
		initialOpenedFile = str(BrawlAPI.RootNode.FilePath)

	# Prompt for PNG file paths
	images = BrawlAPI.OpenMultiFileDialog("Select battle portrait images", FileFilters.TEX0)
	if not images:
		return
	
	# Get output directory (same as png source directory)
	outputDir = images[0].rsplit("\\",1)[0]
	
	# Take user input to determine starting InfFace file name
	PROMPT_STR = "e.g. \"1\" for InfFace" + addLeadingZeros("1", INFFACE_DIGIT_COUNT) + ":"
	initial_BP_ID = BrawlAPI.UserIntegerInput("Enter starting portrait ID", PROMPT_STR)
	
	if initial_BP_ID < 0 or len(str(initial_BP_ID)) > INFFACE_DIGIT_COUNT:
		BrawlAPI.ShowError("Invalid value entered", "Error")
	elif not initial_BP_ID:
		return
	
	# Loop through each image opened and export a brres containing the texture in CI8
	exportedImageCount = 0
	for image in images:
	
		# Determine PNG output path by adding initial ID + exported image count
		endingDigits = addLeadingZeros(initial_BP_ID + exportedImageCount, INFFACE_DIGIT_COUNT)
		outputPath = outputDir + "\\InfFace" + endingDigits + ".brres"
		
		# Generate new dialog box with CI8 settings
		BrawlAPI.New[BRRESNode]()
		dlg = TextureConverterDialog()
		dlg.ImageSource = image
		dlg.Automatic = True
		dlg.StartingFormat = WiiPixelFormat.CI8
		
		if dlg.ShowDialog(MainForm.Instance, BrawlAPI.RootNode) == dlg.DialogResult.OK:
			BrawlAPI.SaveFileAs(outputPath)
			exportedImageCount += 1

	# After exporting, open previously opened file, if it exists
	if initialOpenedFile:
		BrawlAPI.OpenFile(initialOpenedFile)
	
	# Otherwise, leave the last-exported BP open
	else:
		BrawlAPI.OpenFile(outputPath)
	
	# Results
	BrawlAPI.ShowMessage(str(exportedImageCount) + " BRRES files successfully exported to\n" + outputDir, "Success!")

main()