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

Select one or more battle portrait PNG files, along with a starting index value. Each selected image will be exported as an InfFaceXXXX.brres file. Supports 3-digit (vBrawl) and 4-digit (50CC) indices.

## Colorsmash-safe Texture Sort
**Usage:** Right-click any "Textures" group, or parent BRRES

Sorts textures in order based on name, while keeping colorsmash groups in-tact. Includes auto-save functionality for backups during longer sorts.

## Export MenuRule as selcharacter2
**Usage:** mu_menumain.pac > Right-click ARC MenuRule_en

Automatically exports the MenuRule_en ARC into the identical ARC inside sc_selcharacter2.pac within the same folder.

## info.pac Stock Icon Exporter
**Usage:** info.pac > Right-click BRRES Misc Data 30 (or parent ARC)

Exports stock textures and StockFace PAT0 animation data to the other files where stock icon data is used: STGRESULT.pac, StockFaceTex.brres, and sc_selcharacter.pac.

# P+ build management plug-ins

## Copy Tracklist Frequencies (P+)
**Usage:** Plugins menu

Transfer entire tracklist frequencies across build updates. Select a "source" tracklist folder (typically Project+/pf/sound/tracklist) and a "destination" tracklist folder. Song frequency values will be copied from the source to the destination tracklists, based on song name or filename.

## Detect Unused BRSTMs (P+)
**Usage:** Plugins menu > File Checking (P+)

Select the build's pf (or sound, or strm) folder. Any BRSTM files inside sound/strm/ that aren't used by tracklists inside sound/tracklist/ will be listed.

## Verify ASL (stageslot) File Data (P+)
**Usage:** Plugins menu > File Checking (P+)

Select the build's pf, stage, or stageslot folder. All .ASL files will be checked for valid .param file locations. Optionally, the contents can be exported to a .txt file inside the stageslot folder, listing all stage entries in each ASL file along with the corresponding button combination for each.

## Verify Param (stageinfo) File Data (P+)
**Usage:** Plugins menu > File Checking (P+)

Select the build's pf, stage, or stageinfo folder. All .param files will be checked for valid stage .pac, stage module, and tracklist file locations. Optionally, the contents can be exported to a .txt file inside the stageinfo folder, including SFX/GFX banks, stage flags, and character color overlay values.

## Verify TLST (tracklist) File Data (P+)
**Usage:** Plugins menu > File Checking (P+)

Select the build's pf, sound, or tracklist folder. All .TLST files will be checked for valid BRSTM file paths and song IDs, including pinch mode (SongSwitch) tracks. Optionally, the contents can be exported to a .txt file inside the tracklist folder, including frequency, volume (for custom BRSTMs), and SongDelay values.

## Param + ASL File Navigator
**Usage:** Right-click a param parent node, ASL entry node, or any param substage entry.

Easily open a .param file from its ASL entry, or open the stage .pac or .tlst file associated with a given .param file. Specific substage .pac files can also be opened via right-clicking their child nodes.

## TLST Add BRSTMs to Tracklist
**Usage:** Right-click tracklist parent node

Select one or more BRSTM files. New tracklist entries will be automatically generated and configured according to each BRSTM's filepath. If the BRSTM files exist outside of a strm folder, a custom prefix can be added to describe the relative path, such as `../../`

## TLST Reset Track Frequencies
**Usage:** Right-click tracklist parent node

Resets all Frequency values of track entries to their default value (40).

## TLST Check Missing Tracks
**Usage:** Right-click tracklist parent node

Checks all tracklist entries for missing BRSTM file paths (and SongSwitch paths, when applicable).
# Stage optimization plug-ins

## Delete Unused Animation Data
**Usage:** Plugins menu > PAC File Optimization

Checks CHR0, VIS0, SRT0, CLR0, and PAT0 animations in the currently opened stage .pac file, then detects any unused entries and deletes them from the animation. Only recommended for FD, BF, or Palutena-based stages. The result should always be tested in-game, with a backup .pac file saved.

*Alternate: can be run per-animation as well, via any individual animation's right-click > plug-ins menu*

## Delete Unused Stage Textures
**Usage:** Plugins menu > PAC File Optimization

Checks materials and TEX0 nodes in the currently opened stage .pac file. Deletes any materials that are unused by objects, PAT0 animations, or SRT0 animations, then deletes any textures unused by materials or PAT0 animations. Lists any materials set to Cull_All, but leaves them to the user to manually delete. Also lists any models with unused Normals or Vertices nodes. **WILL break Hanenbow-based stages**, and may have untested, undesired effects on others (be wary of Star Fox or Shadow Moses-based stages). The result should always be tested in-game, with a backup .pac file saved.

## Delete Unused Vertices and Normals
**Usage:** Plugins menu > PAC File Optimization

Checks all models in the currently opened stage .pac file, and deletes any Normal or Vertex nodes unused by any objects. Any nodes named "Regenerated" are listed, as this is a common name for unused junk data and may appear misleading. The result should always be tested in-game, with a backup .pac file saved.

## Generate Static BRRES Redirects
**Usage:** Plugins menu > PAC File Optimization

Improves readability of stage .pac files by converting "Static" BRRES nodes (nodes where the only entry is a Static model) to Redirect nodes at the end of the file. The result should always be tested in-game, with a backup .pac file saved.

# Model & animation shortcuts

## CLR0 Set and Rotate Hue
**Usage:** Right-click a CLR0 animation node, CLR0 material, or CLR0 material entry

Modifies all color frames of the animation at once. **Set Hue** changes all color values to the same hue (0 to 359 valid). **Rotate Hue** adds a given value to all colors' hue values, rotating them along the color wheel (-180 to 180 valid). Can be run on the full CLR0 animation, any individual CLR0Material, or CLR0 material entry

## MDL0 Copy Fighter Model
**Usage:** Right-click a MDL0 node inside a costume .pac file

Replaces all identically-named MDL0 nodes in the fighter's directory with the selected MDL0. Useful for optimizing or iterating on several recolors at once.

## MDL0 Import Material Settings
**Usage:** Right-click any MDL0 node

Imports materials and shaders from an external .MDL0 file, replacing all settings at once. Objects still must be re-assigned to materials manually.

## Set All Game & Watch Colors
**Usage:** Right-click a CLR0 animation inside FitGameWatch00.pac, or the corresponding ColorRegister0 entry

Replaces all fill/border entries with the selected color sequence inside the FitGamewatch00 file. Must be ran separately for fill and border entries.

## Locate Texture Usage
**Usage:** Right-click a TEX0 node inside a stage .pac file

Lists all models, materials, objects, and PAT animations using the selected texture.

## Locate SCN0 LightSet/Fog Usage
**Usage:** Right-click a LightSet or Fog node

Lists all materials to which the selected LightSet or Fog is assigned
