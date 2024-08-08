from typing import Dict, List, Any
import os


def perform_action(file_data: Dict[str, Any], rule: Dict[str, Any], actions: Dict[str, Dict[str, Any]]):
    action_name = rule['action']
    if action_name not in actions:
        print(f"Warning: Action '{action_name}' not found in actions list.")
        return

    action = actions[action_name]
    action_type = action['type']

    if action_type == 'move':
        destination = os.path.join(os.path.dirname(file_data['folder_full_path']), action['destination'])
        if not os.path.exists(destination):
            os.makedirs(destination)
        new_path = os.path.join(destination, file_data['file_name'])
        os.rename(file_data['file_full_path'], new_path)
        print(f"Moved {file_data['file_name']} to {destination}")
    else:
        print(f"Warning: Unknown action type '{action_type}'")


def action_move_file(file_data: Dict[str, Any], destination: str):
    if not os.path.exists(destination):
        os.makedirs(destination)
    new_path = os.path.join(destination, file_data['file_name'])
    os.rename(file_data['file_full_path'], new_path)
    print(f"Moved {file_data['file_name']} to {destination}")