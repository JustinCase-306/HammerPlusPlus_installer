import os
import shutil
from pathlib import Path
import zipfile
from colorama import init, Fore

init(autoreset=True)

bin_delete = ["hammerplusplus.exe", "hlmvplusplus.dll", "hlmvplusplus.exe"]
bin_folder = Path(input(Fore.LIGHTYELLOW_EX + "Please paste your game's bin folder path here: ").strip('"'))

print(Fore.LIGHTYELLOW_EX + "\nCleaning up old files...")

for file in bin_delete:
    full_path = bin_folder / file
    if full_path.exists():
        full_path.unlink()
        print(Fore.LIGHTYELLOW_EX + "File deleted: " + file)

print(Fore.LIGHTGREEN_EX + "Successfully cleaned up old files. Continue...")

zip_file = Path(
    input(Fore.LIGHTYELLOW_EX + "\nPlease paste your hammerplusplus_[game]_build[...] .zip path here: ").strip('"'))

temp_extract_folder = bin_folder / "hplusplus_temp_extract"

print(Fore.LIGHTYELLOW_EX + "\nExtracting zip file...")
with zipfile.ZipFile(zip_file, "r") as zip_archive:
    zip_archive.extractall(temp_extract_folder)

extracted_root = next(temp_extract_folder.iterdir())
hammer_bin_folder = extracted_root / "bin"

if not hammer_bin_folder.exists():
    hammer_bin_folder = extracted_root

print(Fore.LIGHTYELLOW_EX + "Moving files to your game's bin folder...")

for item in hammer_bin_folder.iterdir():
    dest_path = bin_folder / item.name

    if item.is_file():
        shutil.move(str(item), str(dest_path))
    elif item.is_dir():
        if dest_path.exists():
            for sub_item in item.iterdir():
                sub_dest = dest_path / sub_item.name
                if sub_item.is_file():
                    shutil.move(str(sub_item), str(sub_dest))
                elif sub_item.is_dir():
                    shutil.copytree(str(sub_item), str(sub_dest), dirs_exist_ok=True)
        else:
            shutil.move(str(item), str(dest_path))

shutil.rmtree(temp_extract_folder)

print(Fore.LIGHTGREEN_EX + "\nSuccessfully moved files and cleaned up!")