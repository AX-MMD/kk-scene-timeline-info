import os
import re
import typing

from kk_scene_wrapper import SceneData

if typing.TYPE_CHECKING:
    from kk_scene_timeline_info.utils import Config


class SceneTimelineInfoManager:
    def __init__(self, *, config: "Config"):
        self.config = config
        self.file_info_pattern = r"^(?:\[(?P<author>[^\]]+)\]) (?P<filename>.+?) (?:\((?P<duration>\d+m\d{1,2})\))?.*$"

    def _extract_name_info(
        self, filename: str
    ) -> typing.Tuple[str, typing.Optional[str], typing.Optional[str], typing.Set[str]]:
        match = re.match(r"^(?:\[(?P<author>[^\]]+)\]) (?P<rest>.+)", filename)
        author = match.group("author") if match else None
        rest = match.group("rest") if match else filename
        match = re.match(
            r"^(?P<filename>.+) (?:\((?P<duration>static|dynamic|dynamic;\d+m\d{2}|\d+m\d{1,2})\))(?:(?P<rest>.*))",
            rest,
        )
        duration = match.group("duration") if match else None
        filename = match.group("filename") if match else rest
        rest = match.group("rest") if match else None
        tags = re.findall(r"\[([^\]]+)\]", rest) if rest else []

        return filename, author, duration, set(tags)

    def _rename_folder(self, folder_path: str, folder_name: str, duration_str: str):
        # Split the folder path and its name
        parent_path, name = os.path.split(folder_path)
        name, author, old_duration_str, tags = self._extract_name_info(name)

        if old_duration_str == duration_str:
            return folder_name  # No change needed

        new_folder_name = f"{name} ({duration_str})"
        new_folder_path = os.path.join(parent_path, new_folder_name)

        # Rename the folder
        if not self.config.display_only:
            os.rename(folder_path, new_folder_path)
        print(f"'{name}' -> '{new_folder_name}'")
        return new_folder_name

    def _rename_file(self, folder_path: str, folder_name: str, filename: str) -> typing.Tuple[str, str, float]:
        file_path = os.path.join(folder_path, filename)
        scene_data = SceneData(file_path)
        image_type, sfx_status, duration = scene_data.get_timeline_info()

        # Get info from the filename
        name, ext = os.path.splitext(filename)
        name, author, duration_str, tags = self._extract_name_info(name)

        # Refresh the duration
        if duration:
            duration_str = f"{int(duration // 60)}m{int(duration % 60):02}"
            if image_type == "dynamic":
                duration_str = "dynamic;" + duration_str
        else:
            duration_str = "static"

        if self.config.replace_tags:
            tags = set(self.config.add_tags)
        else:
            tags.update(self.config.add_tags)

        if sfx_status:
            tags.add("SFX")
        elif "SFX" not in self.config.add_tags:
            tags.discard("SFX")

        if "NoSFX" in self.config.add_tags:
            tags.discard("SFX")
            tags.discard("NoSFX")

        if tags:
            tag_str = " " + "".join(
                f"[{t}]" for t in sorted(tags, key=lambda x: x != "SFX")
            )
        else:
            tag_str = ""

        if self.config.replace_author is not False:
            if self.config.author is None:
                author = folder_name or author
            else:
                author = self.config.author

        if not author:
            new_filename = f"{name} ({duration_str}){tag_str}{ext}"
        else:
            new_filename = f"[{author}] {name} ({duration_str}){tag_str}{ext}"

        # Rename the file
        if not self.config.display_only:
            try:
                os.rename(file_path, os.path.join(folder_path, new_filename))
            except FileExistsError:
                # Handle file name conflict
                u_input = input(f"File '{new_filename}' already exists:\n- [c] copy: Add '_Copy' suffix\n- [s] skip: Skip this file\n- [r] replace: Replace existing file\n- [q] quit: Abort the operation\nYour choice (c/s/r/q): ").strip().lower()
                while u_input not in ("copy", "skip", "replace", "quit", "c", "s", "r", "q"):
                    u_input = input("Invalid choice. Please enter copy/skip/replace/quit or their shortcut: ").strip().lower()

                if u_input in ("copy", "c"):
                    new_filename = f"{os.path.splitext(new_filename)[0]}_Copy{ext}"
                elif u_input in ("replace", "r"):
                    os.remove(os.path.join(folder_path, new_filename))
                elif u_input in ("quit", "q"):
                    raise KeyboardInterrupt("Operation aborted by user.")
                else:
                    print(f"Skipping '{filename}'")
                    return filename, image_type, 0.0

                os.rename(file_path, os.path.join(folder_path, new_filename))

        print(f"'{filename}' -> '{new_filename}'")
        return new_filename, image_type, duration

    def add_info_to_file(self, file_path, author_name=None):
        folder_path = os.path.dirname(file_path)
        folder_name = author_name if author_name else os.path.basename(folder_path)
        if folder_name[0] == "[" and folder_name[-1] == "]":
            folder_name = folder_name[1:-1]

        filename = os.path.basename(file_path)
        self._rename_file(folder_path, folder_name, filename)

    def add_info_to_dir_files(self, folder_path, author_name=None) -> float:
        # Get the folder name
        folder_name = author_name if author_name else os.path.basename(folder_path)
        if folder_name[0] == "[" and folder_name[-1] == "]":
            folder_name = folder_name[1:-1]

        # Total duration of content in the folder
        tot_duration: float = 0.0

        # Iterate over all files and folders in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    _, _, duration = self._rename_file(folder_path, folder_name, filename)
                    if duration:
                        tot_duration += duration
                except SceneData.ContentError as e:
                    print(f"Skipping' {filename}': {e}")
                except SceneData.MemoryError as e:
                    print(f"Skipping '{filename}': {e}")
            elif os.path.isdir(file_path) and not self.config.no_subfolder:
                # Recursively process subfolders and accumulate their durations
                subfolder_duration: float = 0.0

                for sub_filename in os.listdir(file_path):
                    sub_file_path = os.path.join(file_path, sub_filename)
                    if os.path.isfile(sub_file_path):
                        try:
                            _, img_type, duration = self._rename_file(
                                file_path, folder_name, sub_filename
                            )
                            if img_type != "dynamic" and duration:
                                subfolder_duration += duration
                        except SceneData.MemoryError as e:
                            print(f"Skipping '{sub_filename}': {e}")
                        except SceneData.ContentError as e:
                            print(f"Skipping' {sub_filename}': {e}")
                    elif os.path.isdir(sub_file_path):
                        # Recursively process and add duration from subfolders
                        subfolder_duration += self.add_info_to_dir_files(
                            sub_file_path, folder_name
                        )

                if subfolder_duration:
                    duration_str = f"{int(subfolder_duration // 60)}m{int(subfolder_duration % 60):02}"
                    tot_duration += subfolder_duration
                else:
                    duration_str = "static"

                self._rename_folder(file_path, folder_name, duration_str)
            else:
                print(f"Skipping subfolder'{filename}', 'no_subfolder' flag is set")

        return tot_duration
