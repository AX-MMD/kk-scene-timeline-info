from typing import List
import toml


class Config:
    def __init__(
        self, 
        *, 
        display_only: bool = False,
        author: str = None, 
        replace_author: bool = None, 
        add_tags: List[str] = [], 
        replace_tags: bool = False, 
        no_subfolder: bool = True,
        **kwargs
    ):
        self.display_only = self._value_or_none(display_only)
        self.author = author  # author == "" is significant
        self.replace_author = self._value_or_none(replace_author)
        self.add_tags = set(add_tags)
        self.replace_tags = self._value_or_none(replace_tags)
        self.no_subfolder = self._value_or_none(no_subfolder)

    def _value_or_none(self, value):
        return None if (value == "" or value == "null") else value

    def to_dict(self) -> dict:
        return {
            "display_only": self.display_only,
            "author": self.author,
            "replace_author": self.replace_author,
            "add_tags": self.add_tags,
            "replace_tags": self.replace_tags,
            "no_subfolder": self.no_subfolder
        }    

    def __repr__(self):
        return f"Config(display_only={self.display_only}, author={self.author}, replace_author={self.replace_author}, add_tags={self.add_tags}, replace_tags={self.replace_tags}, no_subfolder={self.no_subfolder})"


def load_config_file(path: str) -> Config:
    with open(path, "r", encoding="UTF-8") as f:
        data = toml.load(f)

    return Config(**data.get("base"))