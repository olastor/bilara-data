import argparse
from pathlib import Dict, Path
from typing import List

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-c', '--changed', required=True, type=Path, nargs='*')
arg_parser.add_argument('-d', '--deleted', required=True, type=Path, nargs='*')
args = arg_parser.parse_args()


def filter_overlapping_files(changed: List[Path], deleted: List[Path]) -> Dict[str, List[Path]]:
    overlapping = []
    for p in deleted:
        if p in changed:
            overlapping.append(p)

    filtered_changed = [c for c in changed if c not in overlapping]
    filtered_deleted = [d for d in deleted if d not in overlapping]

    return {'overlapping': overlapping, 'filtered_changed': filtered_changed, 'filtered_deleted': filtered_deleted}


if __name__ == '__main__':
    filter_overlapping_files(changed=args.changed, deleted=args.deleted)
