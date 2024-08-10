import os
import json
from typing import Dict, Any
from datetime import datetime
from tidydrawer.utils.logger import logger
from tidydrawer.core.file_info import get_file_info


class SnapshotManager:
    def __init__(self, root_folder: str, snapshot_file: str = 'tidydrawer_snapshot.json'):
        self.root_folder = root_folder
        self.snapshot_file = snapshot_file

    def create_snapshot(self) -> Dict[str, Any]:
        logger.info("Creating snapshot of the current folder state...")
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'files': {}
        }
        for root, _, files in os.walk(self.root_folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, self.root_folder)
                file_info = get_file_info(full_path)
                snapshot['files'][rel_path] = {
                    'hash': file_info['file_hash'],
                    'size': file_info['file_size'],
                    'last_modified': file_info['last_modified'].isoformat()
                }
        return snapshot

    def save_snapshot(self, snapshot: Dict[str, Any]):
        with open(self.snapshot_file, 'w') as f:
            json.dump(snapshot, f, indent=2)
        logger.info(f"Snapshot saved to {self.snapshot_file}")

    def load_snapshot(self) -> Dict[str, Any]:
        if os.path.exists(self.snapshot_file):
            with open(self.snapshot_file, 'r') as f:
                return json.load(f)
        return None

    def compare_with_current(self, snapshot: Dict[str, Any]) -> Dict[str, Any]:
        current_snapshot = self.create_snapshot()
        changes = {
            'added': [],
            'removed': [],
            'modified': [],
            'moved': []
        }

        current_files = set(current_snapshot['files'].keys())
        snapshot_files = set(snapshot['files'].keys())

        changes['added'] = list(current_files - snapshot_files)
        changes['removed'] = list(snapshot_files - current_files)

        for file in current_files.intersection(snapshot_files):
            if current_snapshot['files'][file]['hash'] != snapshot['files'][file]['hash']:
                changes['modified'].append(file)

        # Detect moved files (same hash, different path)
        current_hashes = {v['hash']: k for k, v in current_snapshot['files'].items()}
        for file, info in snapshot['files'].items():
            if file in changes['removed'] and info['hash'] in current_hashes:
                new_path = current_hashes[info['hash']]
                if new_path in changes['added']:
                    changes['moved'].append((file, new_path))
                    changes['added'].remove(new_path)
                    changes['removed'].remove(file)

        return changes