import json
from pathlib import Path

DEFAULT_CONFIG = {
    "pipes": 1,
    "fps": 75,
    "steady": 13,
    "limit": 2000,
    "random_start": False,
    "bold": True,
    "color": True,
    "keep_style": False,
    "colors": [1, 2, 3, 4, 5, 6, 7, 0],
    "pipe_types": [0]
}

CONFIG_DIR = Path.home() / ".config" / "pipes-py"
CONFIG_FILE = CONFIG_DIR / "config.json"

def load_config():
    """Load configuration from file or return defaults."""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG

    try:
        with open(CONFIG_FILE, 'r') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    except (json.JSONDecodeError, OSError):
        return DEFAULT_CONFIG

def save_config(config):
    """Save configuration to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except OSError:
        pass
