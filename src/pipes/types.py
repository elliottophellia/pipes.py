"""Type definitions for the pipes application."""

from dataclasses import dataclass
from enum import IntEnum


class Direction(IntEnum):
    """Pipe direction enumeration."""

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class PipeStyle(IntEnum):
    """Available pipe styles."""

    HEAVY = 0
    CURVED = 1
    LIGHT = 2
    DOUBLE = 3
    KNOBBY = 4
    ANGLES = 5
    DOTS = 6
    DOTS_O = 7
    SLASHES = 8
    MIXED = 9


@dataclass
class PipeConfig:
    """Configuration for the pipes application."""

    pipes: int
    fps: int
    steady: int
    limit: int
    random_start: bool
    bold: bool
    color: bool
    keep_style: bool
    colors: list[int]
    pipe_types: list[int]


@dataclass
class Pipe:
    """Represents a single pipe with its state."""

    x: int
    y: int
    direction: Direction
    pipe_type: int
    color: int
    attr: int
