import yaml
from typing import Dict, List, Any


class TemplateParser:
    def __init__(self, yaml_string: str):
        self.template = yaml.safe_load(yaml_string)
        self.validate_template()

    def validate_template(self):
        required_keys = ['version', 'rules', 'actions']
        for key in required_keys:
            if key not in self.template:
                raise ValueError(f"Missing required key in template: {key}")

    def parse_rules(self) -> List[Dict[str, Any]]:
        rules = self.template.get('rules', [])
        parsed_rules = []
        for rule in rules:
            parsed_rule = {
                'action': rule.get('action'),
                'priority': rule.get('priority'),
                'conditions': self.parse_conditions(rule.get('conditions', []))
            }
            parsed_rules.append(parsed_rule)
        return parsed_rules

    def parse_conditions(self, conditions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        parsed_conditions = []
        for condition in conditions:
            parsed_condition = {
                'attribute': condition['attribute'],
                'operator': condition['operator'],
                'values': condition.get('values', [condition.get('value')])
            }
            parsed_conditions.append(parsed_condition)
        return parsed_conditions

    def parse_actions(self) -> Dict[str, Dict[str, Any]]:
        actions = self.template.get('actions', {})
        parsed_actions = {}
        for action_name, action_details in actions.items():
            parsed_actions[action_name] = action_details
        return parsed_actions

    def parse(self) -> Dict[str, Any]:
        return {
            'version': self.template['version'],
            'rules': self.parse_rules(),
            'actions': self.parse_actions()
        }


# # Example usage
# yaml_string = '''
# version: 1
# rules:
#   - action: move_to_old_files_folder
#     priority: 1
#     condition:
#       attribute: file_group
#       operator: not_in
#       values:
#         - office
#         - media
#
# actions:
#   move_to_old_files_folder:
#     type: move
#     destination: old_files
# '''
#
# parser = TemplateParser(yaml_string)
# parsed_template = parser.parse()
#
# # Pretty print the parsed template
# import json
#
# print(json.dumps(parsed_template, indent=2))