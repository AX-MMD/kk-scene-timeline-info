import os
import sys
import traceback
from kk_scene_timeline_info import SceneTimelineInfoManager, Config, load_config_file, settings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usages: " +\
             "\nSet the author of the files in the folder to the folder's name" +
             "\n> python script.py <folder_path>" +
             "\nSet the file's author to its parent folder name" +
             "\n> python script.py <file_path>")
        input()
        sys.exit(1)
    
    path = sys.argv[1]
    config: Config = load_config_file(settings.CONFIG_PATH)

    if config.display_only:
        print("### DISPLAY ONLY MODE IS ENABLED ###")
    
    try:
        if os.path.isdir(path):
            SceneTimelineInfoManager(config=config).add_info_to_dir_files(path)
        else:
            SceneTimelineInfoManager(config=config).add_info_to_file(path)
    except Exception as e:
        traceback.print_exc()
    finally:
        input("Press Enter to exit...")