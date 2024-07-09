import json


def load_suggestions():
    with open('config/suggestions.json', 'r', encoding='utf-8') as f:
        suggestions = json.load(f)['药品']
    return suggestions