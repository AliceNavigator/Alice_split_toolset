import os
import argparse
import shutil
from shutil import copyfile
from tqdm import tqdm


def process_and_rename(character_name):
    dataset_path = f"./dataset/{character_name}"
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)
    else:
        print(f'检测到"{dataset_path}" 已存在，执行删除')
        shutil.rmtree(dataset_path)
        os.makedirs(dataset_path)

    counter = 1

    all_folders = [folder for r, d, f in os.walk('./merge') for folder in d]
    for folder in tqdm(all_folders, desc="Processing folders", unit="folder"):
        mapping_path = os.path.join('./merge', folder, "new_mapping.list")
        if os.path.exists(mapping_path):
            with open(mapping_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            for line in tqdm(lines, desc=f"Processing files in {folder}", unit="file", leave=False):
                old_filename, text = line.strip().split("|")
                old_filepath = os.path.join('./merge', folder, old_filename)

                new_filename = f"{character_name}_{counter}.wav"
                new_filepath = os.path.join(dataset_path, new_filename)
                new_mapping_entry = f"./dataset/{character_name}/{new_filename}|{character_name}|ZH|{text}"

                # Copy and rename the file
                copyfile(old_filepath, new_filepath)

                with open(os.path.join(dataset_path, "dataset_mapping.list"), 'a', encoding='utf-8') as dataset_file:
                    dataset_file.write(new_mapping_entry + "\n")

                counter += 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rename and restructure files based on character_name")
    parser.add_argument("character_name", type=str, help="Name of the character for restructuring")
    args = parser.parse_args()

    process_and_rename(args.character_name)
