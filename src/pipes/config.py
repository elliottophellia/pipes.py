"""Configuration management for pipes."""

import json
import sys
from pathlib import Path
from pipes.types import PipeConfig


def get_config_dir() -> Path:
    """Get platform-specific configuration directory."""
    if sys.platform == "win32":
        local_app_data = Path.home() / "AppData" / "Local"
        return local_app_data / "pipes-py"
    return Path.home() / ".config" / "pipes-py"


CONFIG_DIR = get_config_dir()
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = PipeConfig(
    pipes=1,
    fps=75,
    steady=13,
    limit=2000,
    random_start=False,
    bold=True,
    color=True,
    keep_style=False,
    colors=[1, 2, 3, 4, 5, 6, 7, 0],
    pipe_types=[0],
)


def load_config() -> PipeConfig:
    """Load configuration from file or return defaults."""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG

    try:
        with CONFIG_FILE.open("r") as f:
            data = json.load(f)
            return PipeConfig(
                pipes=data.get("pipes", DEFAULT_CONFIG.pipes),
                fps=data.get("fps", DEFAULT_CONFIG.fps),
                steady=data.get("steady", DEFAULT_CONFIG.steady),
                limit=data.get("limit", DEFAULT_CONFIG.limit),
                random_start=data.get("random_start", DEFAULT_CONFIG.random_start),
                bold=data.get("bold", DEFAULT_CONFIG.bold),
                color=data.get("color", DEFAULT_CONFIG.color),
                keep_style=data.get("keep_style", DEFAULT_CONFIG.keep_style),
                colors=data.get("colors", DEFAULT_CONFIG.colors),
                pipe_types=data.get("pipe_types", DEFAULT_CONFIG.pipe_types),
            )
    except (json.JSONDecodeError, OSError):
        return DEFAULT_CONFIG


def save_config(config: PipeConfig) -> None:
    """Save configuration to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        data = {
            "pipes": config.pipes,
            "fps": config.fps,
            "steady": config.steady,
            "limit": config.limit,
            "random_start": config.random_start,
            "bold": config.bold,
            "color": config.color,
            "keep_style": config.keep_style,
            "colors": config.colors,
            "pipe_types": config.pipe_types,
        }
        with CONFIG_FILE.open("w") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass
