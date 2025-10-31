import os
import zipfile

import toml

SRC_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SRC_PATH)
RELEASE_DIR = os.path.join(PROJECT_DIR, 'releases')

def join_path(*args):
    return os.path.join(SRC_PATH, *args)

def to_pascal_case(s: str) -> str:
    return ''.join(word.capitalize() for word in s.replace('-', '_').split('_'))

def get_app_info(pyproject_file='pyproject.toml') -> tuple[str, str]:
    """Yields the app name in PascalCase and version from pyproject.toml."""
    with open(pyproject_file, 'r') as file:
        pyproject_data = toml.load(file)

    return to_pascal_case(pyproject_data['project']['name']), pyproject_data['project']['version']

def zip_directory(zipf, path, base_path, added_files):
    """Recursively adds a directory to the zip file, preserving subfolders."""
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            # Compute the relative path from the base 'path'
            rel_path = os.path.relpath(file_path, path)
            arcname = os.path.join(base_path, rel_path)
            if arcname not in added_files:
                zipf.write(file_path, arcname)
                added_files.add(arcname)

def create_release_zip(zip_filename: str):
    zip_path = os.path.join(RELEASE_DIR, zip_filename)
    os.makedirs(RELEASE_DIR, exist_ok=True)
    if os.path.exists(zip_path):
        os.remove(zip_path)

    added_files = set()

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add config
        config_path = join_path(SRC_PATH, 'config.toml')
        config_arcname = 'config.toml'
        if config_arcname not in added_files:
            zipf.write(config_path, config_arcname)
            added_files.add(config_arcname)

        # Add BAT file
        exe_path = join_path(SRC_PATH, 'KKSceneTimelineInfo.bat')
        exe_arcname = 'KKSceneTimelineInfo.bat'
        if exe_arcname not in added_files:
            zipf.write(exe_path, exe_arcname)
            added_files.add(exe_arcname)

        # Add EXE dependencies from _dist
        zip_directory(zipf, join_path(PROJECT_DIR, '_dist', 'bin'), 'bin', added_files)

        # Add LICENSE
        license_path = join_path(PROJECT_DIR, 'LICENSE')
        license_arcname = 'LICENSE'
        if license_arcname not in added_files:
            zipf.write(license_path, license_arcname)
            added_files.add(license_arcname)

        # Add README.md
        readme_path = join_path(PROJECT_DIR, 'README.md')
        readme_arcname = 'README.md'
        if readme_arcname not in added_files:
            zipf.write(readme_path, readme_arcname)
            added_files.add(readme_arcname)

    print(f'Created {zip_filename}')

if __name__ == '__main__':
    app_name, app_version = get_app_info()
    create_release_zip(f'{app_name}.v{app_version}.zip')
