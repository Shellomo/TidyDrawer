from typing import Dict, List, Any
import os

from tidydrawer.core.file_info import get_file_info, get_file_group
from tidydrawer.core.snapshot_manager import SnapshotManager
from tidydrawer.parsers.template_parser import TemplateParser
from tidydrawer.parsers.rule_parser import match_rule
from tidydrawer.actions.move_action import MoveAction
from tidydrawer.utils.logger import logger


class TidyDrawerEngine:
    def __init__(self, root_folder: str = '.'):
        self.template: Dict[str, Any] = {}
        self.rules: List[Dict[str, Any]] = []
        self.actions: Dict[str, Dict[str, Any]] = {}
        self.snapshot_manager = SnapshotManager(root_folder)
        self.initial_snapshot = None

    def load_template(self, template_path: str) -> None:
        """Load and parse the template file."""
        try:
            with open(template_path, 'r') as f:
                template_content = f.read()

            parser = TemplateParser(template_content)
            parsed_template = parser.parse()

            self.template = parsed_template
            self.rules = parsed_template['rules']
            self.actions = parsed_template['actions']
            self.initial_snapshot = self.snapshot_manager.create_snapshot()
            self.snapshot_manager.save_snapshot(self.initial_snapshot)

            logger.info(f"Template loaded successfully from {template_path}")
        except Exception as e:
            logger.error(f"Error loading template: {str(e)}")
            raise

    def process_folder(self, folder_path: str) -> List[Dict[str, Any]]:
        """Process all files in the given folder according to the loaded rules."""
        processed_files = []
        try:
            for i, filename in enumerate(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    result = self.process_file(file_path)
                    processed_files.append(result)

            logger.info(f"Processed {len(processed_files)} files in {folder_path}")
        except Exception as e:
            logger.error(f"Error processing folder {folder_path}: {str(e)}")
            raise

        return processed_files

    def process_file(self, file_path: str) -> Dict[str, Any]:
        """Process a single file according to the loaded rules."""
        try:
            file_data = get_file_info(file_path)
            matched_rule = self.match_rule_for_file(file_data)

            result = {
                "file": file_data['file_name'] + file_data['file_extension'],
                "matched_rule": matched_rule['action'] if matched_rule else None,
                "action_performed": None
            }

            if matched_rule:
                action_result = self.perform_action(file_data, matched_rule)
                result["action_performed"] = action_result

            logger.info(f"Processed file: {file_data['file_name']}")
            return result
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            raise

    def match_rule_for_file(self, file_data: Dict[str, Any]) -> Dict[str, Any] or None:
        """Find the highest priority rule that matches the file."""
        matched_rule = None
        highest_score = 0

        for rule in self.rules:
            match_score = match_rule(file_data, rule)
            if match_score > highest_score:
                highest_score = match_score
                matched_rule = rule

        return matched_rule

    def perform_action(self, file_data: Dict[str, Any], rule: Dict[str, Any]) -> str:
        """Perform the action specified by the matched rule."""
        action_name = rule['action']
        if action_name not in self.actions:
            logger.warning(f"Action '{action_name}' not found in actions list.")
            return "Action not found"

        action_config = self.actions[action_name]
        action_type = action_config['type']

        if action_type == 'move':
            move_action = MoveAction(action_config['destination'])
            return move_action.execute(file_data)
        else:
            logger.warning(f"Unknown action type '{action_type}'")
            return f"Unknown action type: {action_type}"

    def undo_all_actions(self) -> Dict[str, Any]:
        if not self.initial_snapshot:
            return {"error": "No initial snapshot available"}

        current_changes = self.snapshot_manager.compare_with_current(self.initial_snapshot)

        for src, dest in current_changes['moved']:
            os.rename(os.path.join(self.snapshot_manager.root_folder, dest),
                      os.path.join(self.snapshot_manager.root_folder, src))

        for file in current_changes['added']:
            os.remove(os.path.join(self.snapshot_manager.root_folder, file))

        for file in current_changes['removed']:
            # Here you might want to have a backup of removed files to restore them
            logger.warning(f"Cannot restore removed file: {file}")

        return current_changes


# Example usage
if __name__ == "__main__":
    engine = TidyDrawerEngine()
    engine.load_template("../templates/basic.yaml")
    results = engine.process_folder("../test_folder")
    # print(results)