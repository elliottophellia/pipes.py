"""Terminal rendering logic for pipes."""

import contextlib
import curses
import locale
from pipes.types import Direction, Pipe, PipeConfig
from typing import Any

# Ensure correct handling of Unicode characters
locale.setlocale(locale.LC_ALL, "")

PIPE_SETS = [
    "┃┏ ┓┛━┓  ┗┃┛┗ ┏━",
    "│╭ ╮╯─╮  ╰│╯╰ ╭─",
    "│┌ ┐┘─┐  └│┘└ ┌─",
    "║╔ ╗╝═╗  ╚║╝╚ ╔═",
    "|+ ++-+  +|++ +-",
    "|/ \\ /-\\  \\|/\\ /-",
    ".o ....  .... .o",
    ".o oo.o  o.oo o.",
    "-\\ /\\|/  /-\\/ \\|",
    "╿┍ ┑┚╼┒  ┕╽┙┖ ┎╾",
]


class Renderer:
    """Handles terminal rendering for pipes."""

    def __init__(self, screen: Any, config: PipeConfig) -> None:
        """Initialize the renderer.

        Args:
            screen: Curses screen object
            config: Pipe configuration
        """
        self.screen = screen
        self.config = config
        self.color_pairs: dict[int, int] = {}
        self.sets = self._prepare_sets()

        # Screen setup
        curses.curs_set(0)
        screen.nodelay(True)
        screen.clear()

        self._init_colors()

    def _prepare_sets(self) -> list[str]:
        """Prepare pipe character sets.

        Returns:
            List of pipe characters
        """
        sets: list[str] = []
        for pipe_set in PIPE_SETS:
            sets.extend((pipe_set + " " * 16)[:16])
        return sets

    def _init_colors(self) -> None:
        """Initialize color pairs for rendering."""
        if not self.config.color or not curses.has_colors():
            self.color_pairs = dict.fromkeys(self.config.colors, curses.A_NORMAL)
            return

        curses.start_color()
        curses.use_default_colors()
        max_colors = min(curses.COLORS, 8)

        for idx, color in enumerate(self.config.colors):
            curses_color = color % max_colors
            pair_number = idx + 1
            curses.init_pair(pair_number, curses_color, -1)
            attr = curses.color_pair(pair_number)
            if self.config.bold:
                attr |= curses.A_BOLD
            self.color_pairs[color] = attr

    def get_color_attr(self, color: int) -> int:
        """Get the color attribute for a given color.

        Args:
            color: Color index

        Returns:
            Curses attribute value
        """
        return self.color_pairs[color]

    def draw_pipe(
        self, pipe: Pipe, old_direction: Direction, new_direction: Direction
    ) -> None:
        """Draw a pipe segment at the current position.

        Args:
            pipe: Pipe to draw
            old_direction: Previous direction
            new_direction: New direction
        """
        base = pipe.pipe_type * 16
        index = base + old_direction * 4 + new_direction
        char = self.sets[index] if index < len(self.sets) else "?"

        with contextlib.suppress(curses.error):
            self.screen.addstr(pipe.y, pipe.x, char, pipe.attr)

    def clear(self) -> None:
        """Clear the screen."""
        self.screen.clear()

    def refresh(self) -> None:
        """Refresh the screen."""
        self.screen.refresh()

    def reinit_colors(self) -> None:
        """Reinitialize colors (used when toggling color/bold)."""
        self._init_colors()
