import os
import hashlib
import deepdanbooru
from deepdanbooru.commands import evaluate_image
import traceback
from tensorflow.python.framework.errors_impl import InvalidArgumentError
from tqdm import tqdm
import argparse
import json
import sys

def resource_path(relative_path):
    # when pyinstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)

def get_image_tagscore(image_path):
    result = evaluate_image(image_path, MODEL, TAGS, 0.1)
    results = dict()
    for tag, score in result:
        results[tag] = float(score)
    return dict(sorted(results.items(), key=lambda item: item[1], reverse=True))


def get_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def process_images(files):
    completed_file_path = set()

    for file in tqdm(files):
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        file_path = file

        if VERBOSE: print(f'File, {file_path}')

        if file_path in completed_file_path:
            continue

        md5 = get_md5(file_path)

        try:
            tagscore = get_image_tagscore(file_path)
        except InvalidArgumentError:
            continue

        output_file = f"{md5}.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tagscore, f, ensure_ascii=False, indent=4)

        if VERBOSE: print(f"Saved tags to {output_file}")


if __name__ == "__main__":
    # os.chdir(os.path.dirname(__file__))

    parser = argparse.ArgumentParser(description="Process files and get tags")
    parser.add_argument('input_files', nargs='*', type=str, help="Input file list or one directory")
    parser.add_argument('--dry-run', action='store_true', help="Output empty success file")
    args = parser.parse_args()

    PROJECT_PATH = resource_path('model')
    MODEL = deepdanbooru.project.load_model_from_project(PROJECT_PATH, compile_model=False)
    TAGS = deepdanbooru.project.load_tags_from_project(PROJECT_PATH)

    VERBOSE = False

    target_files = args.input_files

    if (args.dry_run or len(target_files) < 1):
        with open('success', 'w', encoding='utf-8') as f:
            json.dump("success", f, ensure_ascii=False, indent=4)
        sys.exit()

    try:
        process_images(target_files)
    except Exception as e:
        print(f'{traceback.format_exception(e)}')
