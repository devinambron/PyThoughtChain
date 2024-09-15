import json
import os

DEFAULT_CONFIG = {
    "iterations_before_feedback": 1,
    "max_iterations": 5,
    "confidence_threshold": 0.8
}

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return DEFAULT_CONFIG

def save_config(config):
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

CONFIG = load_config()