import argparse
import os
import re


def process_mapping(mapping_path, filter_english, ban_file):
    with open(mapping_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    banned_phrases = []
    if ban_file and os.path.exists(ban_file):
        with open(ban_file, 'r', encoding='utf-8') as bf:
            banned_phrases = [line.strip() for line in bf.readlines()]

    clean_mapping = []

    for line in lines:
        filename, text = line.strip().split("|")

        if filter_english and re.search(r"[a-zA-Z]", text):
            print(f'drop non-kanji text : {text}')
            continue

        if any(ban_phrase in text for ban_phrase in banned_phrases):
            print(f'drop ban text : {text}')
            continue

        clean_mapping.append(line)

    with open(f'{mapping_path[:-12]}/clean_mapping.list', 'w', encoding='utf-8') as file:
        for line in clean_mapping:
            file.write(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and clean mapping.list based on criteria")
    parser.add_argument("--filter_english", action="store_true", default=False, help="Remove entries with English text")
    parser.add_argument("--ban_file", default="ban.txt", help="Path to file with banned phrases")
    args = parser.parse_args()

    for root, dirs, files in os.walk('output'):
        for folder in dirs:
            process_mapping(f"./output/{folder}/mapping.list", args.filter_english, args.ban_file)
