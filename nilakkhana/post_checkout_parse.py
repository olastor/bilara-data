import argparse
import json
from pathlib import Path
from typing import Dict

from parser import parse

# Set up argparse to get the files passed by git diff-tree
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-f', '--files', required=True, type=Path, nargs='*')
args = arg_parser.parse_args()

def update_file_content(file_content: Dict[str, str]) -> Dict[str, str]:
    for key, value in file_content.items():
        if type(value) != str:
            continue
        file_content[key] = parse(value).replace('"', '\'')
    return file_content


if __name__ == '__main__':
    unfiltered_files = args.files
    changed_files = [f for f in unfiltered_files if f.suffix == '.json']
    print(f"Received changed files in Nilakkhana: {changed_files}")
    for file in changed_files:
        print(f'{file} file in progress')
        with open(file, 'r+', encoding='utf-8') as target_file:
            data = json.load(target_file)
            data = update_file_content(data)
            target_file.seek(0)
            target_file.truncate()
            json.dump(data, target_file, indent=2, ensure_ascii=False)
        print(f'{file} done!')

    print('\nNilakkhana done!')
