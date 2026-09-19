#!/usr/bin/env python3
"""Bundle the preserved foundation into the independently installable front door.

Run after editing skills/paper-figure-creation. The copied foundation is generated;
edit its original source, not both copies. --check detects an outdated bundle.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

REPO = Path(__file__).resolve().parents[1]


def source_files(root):
    return sorted(p for p in root.rglob('*') if p.is_file()
                  and '__pycache__' not in p.parts and p.suffix != '.pyc')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=Path, default=REPO / 'skills/paper-visual-design')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    source = REPO / 'skills/paper-figure-creation'
    target = args.target.resolve()
    if not (target / 'SKILL.md').is_file():
        parser.error('Initialize paper-visual-design before bundling its foundation.')
    # A standalone installation has one discoverable skill entry point. Preserve
    # the foundation's full instructions as a guide, not a nested second skill.
    paths = {("GUIDE.md" if p.name == "SKILL.md" and p.parent == source
              else str(p.relative_to(source))): p for p in source_files(source)}
    files = {name: digest(path) for name, path in paths.items()}
    manifest = {'source': 'skills/paper-figure-creation',
                'repository': 'https://github.com/Mishrakshitij/paper-figure-creation-skill',
                'policy': 'Generated bundle. Edit the source foundation and rerun the sync script.',
                'renamed_sources': {'GUIDE.md': 'SKILL.md'},
                'sha256': files}
    bundled = target / 'foundation'
    if args.check:
        actual = {str(p.relative_to(bundled)): digest(p) for p in source_files(bundled)}
        manifest_path = target / 'foundation-bundle.json'
        ok = actual == files and manifest_path.exists() and json.loads(manifest_path.read_text()) == manifest
        print('Foundation bundle matches source.' if ok else 'Foundation bundle is stale.')
        return 0 if ok else 1
    if bundled.exists():
        shutil.rmtree(bundled)
    shutil.copytree(source, bundled, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    (bundled / 'SKILL.md').rename(bundled / 'GUIDE.md')
    (target / 'foundation-bundle.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Bundled {len(files)} foundation files into {target.name}.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
