from typing import Dict, List, Any


def match_rule(file_data: Dict[str, Any], rule: Dict[str, Any]) -> float:
    conditions = rule['conditions']
    match_scores = [match_condition(file_data, condition) for condition in conditions]

    # All conditions must be met for the rule to match
    if all(match_scores):
        return sum(match_scores) / len(match_scores)  # Average match score
    return 0


def match_condition(file_data: Dict[str, Any], condition: Dict[str, Any]) -> float:
    attribute = condition['attribute']
    operator = condition['operator']
    values = condition['values']

    if attribute not in file_data:
        return 0

    file_value = file_data[attribute]

    if operator == '=':
        return 1 if file_value in values else 0
    elif operator == '!=':
        return 1 if file_value not in values else 0
    elif operator == 'in':
        return 1 if file_value in values else 0
    elif operator == 'not_in':
        return 1 if file_value not in values else 0
    elif operator == '<':
        return 1 if file_value < values[0] else 0
    elif operator == '<=':
        return 1 if file_value <= values[0] else 0
    elif operator == '>':
        return 1 if file_value > values[0] else 0
    elif operator == '>=':
        return 1 if file_value >= values[0] else 0

    return 0