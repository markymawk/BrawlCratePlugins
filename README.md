# Installation
*Python 3.9.x required to run. Set the Python install path inside Tools > Settings > BrawlAPI tab.*  
*BrawlCrate v0.37 or newer required for installation & auto-updates.*  

In BrawlCrate, navigate to Tools > Settings > Updater tab, and click the Manage Subscriptions button.  
Click add, then paste the link to this Github repo: https://github.com/markymawk/BrawlCratePlugins  
Then, these plug-ins will download and update automatically!  

Feedback welcome @ mawwwk#1068

# 1. Cosmetics plug-ins

## 1.1 Convert PNGs to Battle Portraits
**Usage:** Plugins menu

Bulk export PNG files as InfFace BRRES files, given a starting index value. Supports 3-digit (vBrawl) and 4-digit (50CC) indices.

## 1.2 Colorsmash-safe Texture Sort
**Usage:** Right-click any "Textures" group, or parent BRRES

Sort textures alphabetically, while keeping colorsmash groups in-tact. Includes auto-save functionality for backups during longer sorts.

## 1.3 Export MenuRule as selcharacter2
**Usage:** mu_menumain.pac > Right-click ARC MenuRule_en

Export the MenuRule_en ARC into the identical ARC inside sc_selcharacter2.pac within the same folder.

## 1.4 info.pac Stock Icon Exporter
**Usage:** info.pac > Right-click BRRES Misc Data 30 (or parent ARC)

Export stock textures and StockFace PAT0 animation data to the other files where stock icon data is used: `STGRESULT.pac`, `StockFaceTex.brres`, and `sc_selcharacter.pac`.

# 2. Build management plug-ins

## 2.1 Copy Tracklist Frequencies
**Usage:** Plugins menu

Transfer entire tracklist frequencies across build updates. Select a "source" tracklist folder (typically `Project+/pf/sound/tracklist`) and a "destination" tracklist folder. Song frequency values will be copied from the source to the destination tracklists, based on song name or filename.

## 2.2 Detect Unused BRSTMs (P+)
**Usage:** Plugins menu > File Checking (P+)

Scan a `strm` folder for any BRSTM files that aren't used by tracklist files inside `sound/tracklist/`. Unused files will be listed, with the option to delete them all at once.

## 2.3 Match All StgPosition Nodes 
**Usage:** Right-click any StgPosition model or its parent Model Data [100] BRRES inside a stage pac

Copy stageposition data (blastzones, respawn points) to all other stage .pac files that contain a given substring. For stage files with multiple StgPosition nodes, only the top-most one will be overwritten.  
This process is irreversible -- always save backups!

## 2.4 Verify ASL (stageslot) File Data
**Usage:** Plugins menu > File Checking (P+)

All .ASL files inside the given `stageslot` folder (or parent `pf` folder) will be checked for valid .param file locations. Optionally, the contents can be exported to a .txt file inside the stageslot folder, listing all stage entries in each ASL file along with the corresponding button combination for each.

## 2.5 Verify Param (stageinfo) File Data
**Usage:** Plugins menu > File Checking (P+)

All .param files inside the given `stageinfo` folder (or parent `pf` folder) will be checked for valid stage .pac, stage module, and tracklist file locations. Optionally, the contents can be exported to a .txt file inside the stageinfo folder, including SFX/GFX banks, stage flags, and character color overlay values.

## 2.6 Verify TLST (tracklist) File Data
**Usage:** Plugins menu > File Checking (P+)

All .TLST files inside the given `tracklist` folder (or parent `pf` folder) will be checked for valid BRSTM file paths and song IDs, including pinch mode (SongSwitch) tracks. Optionally, the contents can be exported to a .txt file inside the tracklist folder, including frequency, volume (for custom BRSTMs), and SongDelay values.

*Alternately, can be run per-tracklist as well, via any individual tracklist's right-click > plug-ins menu*

## 2.7 ASL + Param File Navigator
**Usage:** Right-click a param root node, ASL entry node, or any param substage entry.

Open a .param file from its ASL entry, or open the stage .pac or .tlst file associated with a given .param file. Specific substage .pac files can also be opened via right-clicking their child nodes.

## 2.8 TLST Add BRSTMs to Tracklist
**Usage:** Right-click tracklist root node

Generate new tracklist entries from selected BRSTM files automatically, based on their filepaths. If the BRSTM files exist outside of a strm folder, a custom prefix can be added to describe the relative path, such as `../../`

## 2.9 TLST Reset Track Frequencies
**Usage:** Right-click tracklist root node

Reset all frequency values of tracklist entries to their default value (40).

## 2.10 TLST Rename & Set Volume in All Tracklists
**Usage:** Right-click any track node that uses a custom BRSTM path

Rename or set volume of all instances of the selected track across every tracklist in the same directory. For quick repeat usage, leave the tracklist directory open in BrawlCrate.

# 3. Stage optimization plug-ins

## 3.1 Delete Unused Animation Data
**Usage:** Plugins menu > PAC File Optimization

Check CHR0, VIS0, SRT0, CLR0, and PAT0 animations in the currently opened stage .pac file. Any unused entries will be listed and deleted from the animation. Only recommended for FD, BF, or Palutena-based stages. The result should always be tested in-game, with a backup .pac file saved.

*Alternately can be run per-animation as well, via any individual animation's right-click > plug-ins menu*

## 3.2 Delete Unused Stage Textures
**Usage:** Plugins menu > PAC File Optimization

Check materials and TEX0 nodes in the currently opened stage .pac file. Any materials that are unused by objects, PAT0 animations, or SRT0 animations, along with any textures unused by materials or PAT0 animations, will all be deleted. Any Cull_All materials, and unused Normals or Vertex nodes are also listed, but not deleted. **WILL break Hanenbow-based stages**, and may have untested, undesired effects on others (be wary of Star Fox or Shadow Moses-based stages). The result should always be tested in-game, with a backup .pac file saved.

## 3.3 Delete Unused Vertices and Normals
**Usage:** Plugins menu > PAC File Optimization

Delete any Normal or Vertex nodes unused by any objects within models. The result should always be tested in-game, with a backup .pac file saved.

## 3.4 Delete Unused Bones
**Usage:** Plugins menu > PAC File Optimization

Delete any bones unused by objects or collisions. Out of caution, this doesn't affect any models that use non-SingleBind objects (objects bound to multiple bones), and also avoids PokeTrainer and hyakunin_pos models.

## 3.5 Generate Static BRRES Redirects
**Usage:** Plugins menu > PAC File Optimization

Improve readability of stage .pac files by converting "Static" BRRES nodes (nodes where the only entry is a Static model) to Redirect nodes at the end of the file. The result should always be tested in-game, with a backup .pac file saved.

# 4. MDL0, TEX0, animation shortcuts

## 4.1 CLR0 Set and Rotate Hue, Adjust Saturation, Adjust Brightness
**Usage:** Right-click a MDL0 Color node, CLR0 animation node, CLR0 material, CLR0 material entry

Modify all color entries of the selected item at once. **Set Hue** changes all colors to the same hue (0 to 359 valid). **Rotate Hue** adds a given value to all colors' hue values, rotating them along the color wheel (-180 to 180 valid). **Adjust Saturation** and **Adjust Brightness** change the value of the color's respective saturation or brightness by the entered value (-100 to 100 valid).

## 4.2 MDL0 Copy Fighter Model
**Usage:** Right-click a MDL0 node inside a costume .pac file

Export the selected fighter MDL0 to all identically-named MDL0 nodes in the fighter's directory. Useful for optimizing or iterating on several recolors at once.

## 4.3 MDL0 Import Material Settings
**Usage:** Right-click any MDL0 node

Import materials and shaders from an external .MDL0 file, along with object DrawPass settings. Objects still must be re-assigned to materials manually.

## 4.4 MDL0 Set All FogIndex & LightSet
**Usage:** Right-click any MDL0 node with materials

Set all of the model's materials' FogIndex or LightSetIndex values to the given value (-1 to 20).

## 4.5 PAT0 Set Palettes to Texture Name
**Usage:** Right-click any PAT0, PAT0 texture entry, or PAT0 material entry  

Set each palette within a PAT0 frame to match the name of the texture.

## 4.6 Set All Game & Watch Colors
**Usage:** Right-click a CLR0 animation inside FitGameWatch00.pac, or the corresponding ColorRegister0 entry

Replace all matching ColorRegister0 entries with the selected color sequence inside the FitGamewatch00 file. Must be ran separately for fill and border entries.

## 4.7 Locate Texture Usage
**Usage:** Right-click a TEX0 node inside a stage .pac file

List all models, materials, objects, and PAT animations using the selected texture.

## 4.8 Rename TEX0 & Preserve References
**Usage:** Right-click a TEX0 node within any BRRES

Rename the selected texture and any material references and PAT0 entries where the texture is used. If the selected TEX0 is renamed over an already-existing TEX0, then the selected TEX0 will be deleted, and all references to the selected texture will instead direct to the new texture.
For TEX0s within a MiscData or ModelData, only that BRRES will be affected. For TEX0s within a TextureData, references within the whole file will be checked.

## 4.9 Locate SCN0 LightSet/Fog Usage
**Usage:** Right-click a LightSet or Fog node

List all materials to which the selected LightSet index or Fog index is assigned.

# 5. General node operations

## 5.1 Output Nodes to Text
**Usage:** Plugins menu

Output a .txt file containing info of the selected node and all child nodes, including name, MD5 checksum, node size, and specialized info for certain node types. Ideal for comparing files or as a form of version control.

## 5.2 MD5 of Selected Node
**Usage:** Plugins menu

Display a message with the MD5 checksum of the selected node, for quick checks or comparisons.
