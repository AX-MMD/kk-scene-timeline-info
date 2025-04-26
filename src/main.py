import os
import sys
import traceback

from kk_scene_timeline_info import (
    Config,
    SceneTimelineInfoManager,
    load_config_file,
    settings,
)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        path = input("Please enter the path to the folder or scene file:\n> ")
        if not path:
            input("No path provided.")
            sys.exit(1)
        elif path[0] == '&':
            path = path[3:-1]
    elif len(sys.argv) != 2:
        print("Usages: " +\
             "\nSet the author of the files in the folder to the folder's name" +
             "\n> python script.py <folder_path>" +
             "\nSet the file's author to its parent folder name" +
             "\n> python script.py <file_path>")
        input()
        sys.exit(1)
    else:
        path = sys.argv[1]

    path = path.replace("\\", "/").replace("'", "").replace('"', "").strip()

    try:
        config: Config = load_config_file(settings.CONFIG_PATH)

        if config.display_only:
            print("### DISPLAY ONLY MODE IS ENABLED ###")

        if os.path.isdir(path):
            SceneTimelineInfoManager(config=config).add_info_to_dir_files(path)
        else:
            SceneTimelineInfoManager(config=config).add_info_to_file(path)

        if config.display_only:
            print("### DISPLAY ONLY MODE, NO FILES CHANGED ###")
    except Exception:
        traceback.print_exc()
    finally:
        input("Press Enter to exit...")
