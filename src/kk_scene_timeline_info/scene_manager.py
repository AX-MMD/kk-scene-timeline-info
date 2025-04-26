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

        if self.config.replace_author is not False:
            if self.config.author is None:
                author = folder_name or author
            else:
                author = self.config.author

        if not author:
            new_folder_name = f"{name} ({duration_str})"
        else:
            new_folder_name = f"[{author}] {name} ({duration_str})"

        new_folder_path = os.path.join(parent_path, new_folder_name)

        # Rename the folder
        if not self.config.display_only:
            os.rename(folder_path, new_folder_path)
        print(f"'{name}' -> '{new_folder_name}'")
        return new_folder_name

    def _rename_file(self, folder_path: str, folder_name: str, filename: str):
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

    def add_info_to_dir_files(self, folder_path, author_name=None):
        # Get the folder name
        folder_name = author_name if author_name else os.path.basename(folder_path)
        if folder_name[0] == "[" and folder_name[-1] == "]":
            folder_name = folder_name[1:-1]

        # Iterate over all files in the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    self._rename_file(folder_path, folder_name, filename)
                except SceneData.ContentError as e:
                    print(f"Skipping' {filename}': {e}")
                except SceneData.MemoryError as e:
                    print(f"Skipping '{filename}': {e}")
            elif os.path.isdir(file_path) and not self.config.no_subfolder:
                tot_duration = 0
                for sub_filename in os.listdir(file_path):
                    sub_file_path = os.path.join(file_path, sub_filename)
                    if os.path.isfile(sub_file_path):
                        try:
                            _, img_type, duration = self._rename_file(
                                file_path, folder_name, sub_filename
                            )
                            if img_type != "dynamic" and duration:
                                tot_duration += duration
                        except SceneData.MemoryError as e:
                            print(f"Skipping '{sub_filename}': {e}")
                        except SceneData.ContentError as e:
                            print(f"Skipping' {sub_filename}': {e}")
                if tot_duration:
                    duration_str = (
                        f"{int(tot_duration // 60)}m{int(tot_duration % 60):02}"
                    )
                    self._rename_folder(file_path, folder_name, duration_str)
            else:
                print(f"Skipping subfolder'{filename}', 'no_subfolder' flag is set")
