import argparse
import os
from pydub import AudioSegment
from tqdm import tqdm
import shutil

def merge_segments(mapping_path, folder_name, max_length):
    merge_path = f"merge/{folder_name}"
    if not os.path.exists(merge_path):
        os.makedirs(merge_path)
    else:
        print(f'检测到{merge_path}已存在，执行删除')
        shutil.rmtree(merge_path)
        os.makedirs(merge_path)

    with open(mapping_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    segments_to_merge = []
    current_text_length = 0
    new_mapping = []

    for line in tqdm(lines, desc=f"Processing {folder_name}", unit="line"):
        filename, text = line.strip().split("|")
        current_text_length += len(text)

        segments_to_merge.append((filename, text))

        if current_text_length > max_length:
            merged_audio = AudioSegment.empty()
            merged_text = []

            for seg_file, seg_text in segments_to_merge:
                audio_path = os.path.join(os.path.dirname(mapping_path), seg_file)
                segment_audio = AudioSegment.from_wav(audio_path)
                merged_audio += segment_audio
                merged_text.append(seg_text)

            merged_filename = f"{segments_to_merge[0][0]}_to_{segments_to_merge[-1][0]}"
            merged_audio.export(os.path.join(merge_path, merged_filename), format="wav")
            new_mapping.append(f"{merged_filename}|{','.join(merged_text)}")

            segments_to_merge = []
            current_text_length = 0

    if segments_to_merge:
        merged_audio = AudioSegment.empty()
        merged_text = []

        for seg_file, seg_text in segments_to_merge:
            audio_path = os.path.join(os.path.dirname(mapping_path), seg_file)
            segment_audio = AudioSegment.from_wav(audio_path)
            merged_audio += segment_audio
            merged_text.append(seg_text)

        merged_filename = f"{segments_to_merge[0][0]}_to_{segments_to_merge[-1][0]}"
        merged_audio.export(os.path.join(merge_path, merged_filename), format="wav")
        new_mapping.append(f"{merged_filename}|{' '.join(merged_text)}")

    with open(os.path.join(merge_path, "new_mapping.list"), 'w', encoding='utf-8') as file:
        for line in new_mapping:
            file.write(line + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge short segments from mapping.list")
    parser.add_argument("--max", type=int, default=20, help="Maximum text length for a segment")
    args = parser.parse_args()

    for root, dirs, files in os.walk('output'):
        for folder in tqdm(dirs, desc="Merging folders", unit="folder"):
            merge_segments(f"./output/{folder}/clean_mapping.list", folder, args.max)
