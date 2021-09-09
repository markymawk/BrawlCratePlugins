Plug-ins for BrawlCrate using BrawlAPI. Includes scripts for optimizing stage .pac files, maintaining custom builds, and some other helpful automated processes.

To install:  
In BrawlCrate, navigate to Tools > Settings > Updater tab, and click the Manage Subscriptions button.  
Click add, then paste the link to this Github repo: https://github.com/markymawk/BrawlCratePlugins  
Then, these plug-ins will download and update automatically!  
*BrawlCrate v0.37 or newer required for auto-updates.*

Feedback welcome @ mawwwk#1068

# Cosmetics plug-ins

## Convert PNGs to Battle Portraits
**Usage:** Plugins menu

Select one or more battle portrait PNG files, along with a starting index. Exports each PNG as an InfFaceXXXX.brres file. Supports 3-digit (vBrawl) and 4-digit (50CC) indices.

## Colorsmash-safe Texture Sort
**Usage:** Right-click any "Textures" group, or parent BRRES

Sorts textures in order based on name, while keeping colorsmash groups in-tact. Includes auto-save functionality for backups during longer sorts.

## Export MenuRule as selcharacter2
**Usage:** mu_menumain.pac > Right-click ARC MenuRule_en

Automatically exports the MenuRule_en ARC into the identical ARC inside sc_selcharacter2.pac within the same folder.

## info.pac Stock Icon Exporter
**Usage:** info.pac > Right-click BRRES Misc Data 30 (or parent ARC)

Exports stock textures and corresponding PAT0 animation to the other files where stock icon data is used: STGRESULT.pac, StockFaceTex.brres, and sc_selcharacter.pac.

# P+ build management plug-ins

## Copy Tracklist Frequencies (P+)
**Usage:** Plugins menu

Transfer entire tracklist frequencies across build updates. Select a "source" tracklist folder (typically Project+/pf/sound/tracklist) and a "destination" tracklist folder. Song frequency values will be copied from the source to the destination tracklists, based on song name or filename.

## Detect Unused BRSTMs (P+)
**Usage:** Plugins menu > File Checking (P+)

Select the build's pf (or sound, or strm) folder. Any BRSTM files inside sound/strm/ that aren't used by tracklists inside sound/tracklist/ will be listed.

## Verify ASL (stageslot) File Data (P+)
**Usage:** Plugins menu > File Checking (P+)

Select the build's pf, stage, or stageslot folder. All .ASL files will be checked for valid .param file locations. Optionally, the contents can be exported to a .txt file inside the stageslot folder, for record-keeping or version control.

## Verify Param (stageinfo) File Data (P+)
**Usage:** Plugins menu > File Checking (P+)

Select the build's pf, stage, or stageinfo folder. All .param files will be checked for valid stage .pac, stage module, and tracklist file locations. Optionally, the contents can be exported to a .txt file inside the stageinfo folder, including SFX/GFX banks, stage flags, and character color overlay values.

## Verify Tracklist (TLST) File Data (P+)
**Usage:** Plugins menu > File Checking (P+)

Select the build's pf, sound, or tracklist folder. All .TLST files will be checked for valid BRSTM file paths and song IDs, including pinch mode (SongSwitch) tracks. Optionally, the contents can be exported to a .txt file inside the tracklist folder, including frequency, volume (for custom BRSTMs), and SongDelay values.

## Param File Navigator
**Usage:** Right-click param node, or any substage entry

Easily open the stage .pac or .tlst file associated with the given .param file. Specific substage .pac files can also be opened via right-clicking them.

## TLST Add BRSTMs to Tracklist
**Usage:** Right-click tracklist node

Select one or more BRSTM files, and tracklist nodes will be automatically generated and renamed according to the BRSTM's filepath. If the BRSTM file exists outside of a strm folder, a custom prefix can be added to describe the relative path, such as ../../

## TLST Reset Track Frequencies
**Usage:** Right-click tracklist node

Resets all Frequency values of track entries to their default value (40).

# Stage optimization plug-ins

## Delete Unused Animation Data
**Usage:** Plugins menu > PAC File Optimization

Iterates through CHR0, VIS0, SRT0, CLR0, and PAT0 animations in the currently opened stage .pac file, detects any unused entries, and deletes them from the animation. The result should always be tested in-game, with a backup .pac file saved.

## Delete Unused Stage Textures
**Usage:** Plugins menu > PAC File Optimization

Iterates through material entries and TEX0 entries in the currently opened stage .pac file, and deletes any textures unused by materials or PAT0 animations. Lists any materials set to Cull_All, but leaves them to the user to manually delete. Also lists any models with unused Normals or Vertices nodes. **WILL break Hanenbow-based stages**, and may have untested, undesired effects on others (be wary of Star Fox or Shadow Moses-based stages). 

## Delete Unused Vertices and Normals
**Usage:** Plugins menu > PAC File Optimization

Iterates through models in the currently opened stage .pac file, and deletes any Normals or Vertices nodes unused by any objects. Lists any nodes named "Regenerated" as these may appear misleading to others (this is a common name for unused junk data). The result should always be tested in-game, with a backup .pac file saved.

## Generate Static BRRES Redirects
**Usage:** Plugins menu > PAC File Optimization

Improves readability of stage .pac files by converting "Static" BRRES nodes (nodes where the only entry is a Static model) to Redirect nodes at the end of the file. The result should always be tested in-game, with a backup .pac file saved.

## Clear Unused Animation Entries
**Usage:** Right-click a CHR0, VIS0, STR0, CLR0, or PAT0 animation node

A single-use version of "Delete Unused Animation Data" that checks a single animation entry for unused bones (CHR0, VIS0) or materials (SRT0, CLR0, PAT0). The result should always be tested in-game, with a backup .pac file saved.

# Model & animation shortcuts

## CLR0 Set and Rotate Hue
**Usage:** Right-click a CLR0 animation node

Modifies all frames of a CLR0 entry at once. **Set Hue** changes all color values to the same hue (0 to 359 valid). **Rotate Hue** adds a given value to all colors' hue values, rotating them along the color wheel (-180 to 180 valid).

## MDL0 Copy Fighter Model
**Usage:** Right-click a MDL0 node inside a costume .pac file

Exports the selected MDL0 node to the same location inside all other costume .pac files in the same folder with the same name. Useful for optimizing or iterating on several recolors at once.

## MDL0 Import Material Settings
**Usage:** Right-click any MDL0 node

Imports materials and shaders from an external .MDL0 file, replacing all settings at once. Objects still must be re-assigned to materials manually.

## Set All Game & Watch Colors
**Usage:** Right-click a CLR0 animation inside FitGameWatch00.pac, or the corresponding ColorRegister0 entry

Exports the selected color sequence to the other matching entries inside the FitGamewatch00 file. Must be ran separately for fill and border entries.

## Locate Texture Usage
**Usage:** Right-click a TEX0 node inside a stage .pac file

Lists all models, materials, objects, and PAT animations using the selected texture.
