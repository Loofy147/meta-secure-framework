import yaml
from typing import Dict, Any

def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """
    Loads and parses the YAML configuration file.

    Args:
        config_path: The path to the configuration file.

    Returns:
        A dictionary containing the configuration settings.
    """
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Warning: Configuration file not found at '{config_path}'. Using default settings.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return {}
