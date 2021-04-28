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
    print(f"Received changed files in Nilakkhana: {args.files}")
    for file in args.files:
        print(f'{file} file in progress')
        with open(file, 'r+', encoding='utf-8') as target_file:
            data = json.load(target_file)
            data = update_file_content(data)
            if file == 'root/pli/ms/sutta/an/an1/an1.628-637_root-pli-ms_test_1.json' or file == 'root/pli/ms/sutta/an/an1/an1.638-647_root-pli-ms_test_2.json':
                print(f'data={data}')
            target_file.seek(0)
            target_file.truncate()
            json.dump(data, target_file, indent=2, ensure_ascii=False)
        print(f'{file} done!')

    print('\nNilakkhana done!')
