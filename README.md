# KK Scene Timeline Info

**KK Scene Timeline Info** is a console executable designed to add timeline information to a scene's file name. It provides configurable options to customize how file names are updated, including adding author names, replacing tags, and handling subfolders.

## Features
- Add timeline information to file names.
- Add `SFX` tag to file name of scenes that includes sounds (experimental).
- Add custom tags to file name.
- Optional, prepend the file name with `[author name]`.
- Optional, Handle subfolders as scene collections with aggregated information.

## Configuration
The script behavior can be customized using the `config.toml` file. Below are the available options:

- **`display_only`**:  
  If `true`, the script will only display the changes without applying them.  
  Default: `false`

- **`author`**:  
  Specify the author name to add to file names. 
  If left empty, will not add author name.
  If removed completely or commented out, will use the parent folder's name.

- **`replace_author`**:  
  If `false`, the script will not update the author in file names.  
  Default: `true`

- **`replace_tags`**:  
  If `true`, all tags (except `SFX`) will be replaced (instead of updated) with the content of `add_tags`. To force remove the `SFX` tag, add `NoSFX` to `add_tags`.  
  Default: `false`

- **`add_tags`**:  
  A list of tags to add or replace. Example: `add_tags=["animation", "creampie"]`.  
  Default: `[]`

- **`no_subfolder`**:  
  If `false`, subfolders will be treated as scene collections, and each subfolder will be assigned the author name and the total playtime of its scenes. Individual scenes will still have their own information.  
  Default: `true`

## Installation
