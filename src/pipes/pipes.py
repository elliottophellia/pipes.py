"""Core pipe state management."""

import random
import time
from pipes.renderer import Renderer
from pipes.types import Direction, Pipe, PipeConfig
from typing import Any


class PipesScreen:
    """Manages the state and behavior of pipes on the screen."""

    def __init__(self, screen: Any, config: PipeConfig) -> None:
        """Initialize the pipes screen.

        Args:
            screen: Curses screen object
            config: Pipe configuration
        """
        self.screen = screen
        self.config = config
        self.renderer = Renderer(screen, config)
        self.pipes: list[Pipe] = []

        self.height, self.width = screen.getmaxyx()
        self.count = 0
        self.delay = 1.0 / self.config.fps

        self._init_pipes()

    def _init_pipes(self) -> None:
        """Initialize all pipes with random or centered positions."""
        h, w = self.screen.getmaxyx()
        for _ in range(self.config.pipes):
            direction = (
                Direction(random.randrange(4))
                if self.config.random_start
                else Direction.UP
            )
            x = random.randrange(w) if self.config.random_start else w // 2
            y = random.randrange(h) if self.config.random_start else h // 2

            pipe_type = random.choice(self.config.pipe_types)
            color = random.choice(self.config.colors)

            self.pipes.append(
                Pipe(
                    x=x,
                    y=y,
                    direction=direction,
                    pipe_type=pipe_type,
                    color=color,
                    attr=self.renderer.get_color_attr(color),
                )
            )

    def update(self) -> bool:
        """Update pipes state and render.

        Returns:
            False if the user wants to quit, True otherwise
        """
        key = self.screen.getch()
        if key != -1 and not self._handle_key(key):
            return False

        new_h, new_w = self.screen.getmaxyx()
        if new_h != self.height or new_w != self.width:
            self.height, self.width = new_h, new_w
            self.renderer.clear()

        self._update_pipes()
        self.renderer.refresh()

        self.count += len(self.pipes)
        if self.config.limit > 0 and self.count >= self.config.limit:
            self.renderer.clear()
            self.count = 0

        time.sleep(self.delay)
        return True

    def _update_pipes(self) -> None:
        """Update position and direction of all pipes."""
        for pipe in self.pipes:
            x, y = pipe.x, pipe.y
            old_direction = pipe.direction

            # Update position based on direction
            if old_direction % 2:  # RIGHT or LEFT
                x += -old_direction + 2
            else:  # UP or DOWN
                y += old_direction - 1

            # Handle wrapping
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                if not self.config.keep_style:
                    pipe.pipe_type = random.choice(self.config.pipe_types)
                    pipe.color = random.choice(self.config.colors)
                    pipe.attr = self.renderer.get_color_attr(pipe.color)
                x %= self.width
                y %= self.height

            # Calculate new direction
            new_direction = old_direction
            if random.randrange(self.config.steady) <= 1:
                turn = 2 * random.randrange(2) - 1  # -1 or 1
                new_direction = Direction((old_direction + turn) % 4)

            # Draw pipe segment
            self.renderer.draw_pipe(pipe, old_direction, new_direction)

            # Update pipe state
            pipe.x = x
            pipe.y = y
            pipe.direction = new_direction

    def _update_pipe_colors(self) -> None:
        """Update all pipe colors after color/bold changes."""
        for pipe in self.pipes:
            pipe.attr = self.renderer.get_color_attr(pipe.color)

    def _handle_key(self, key: int) -> bool:
        """Handle keyboard input.

        Args:
            key: Key code from curses

        Returns:
            False if the user wants to quit, True otherwise
        """
        key_char = chr(key).upper() if 0 <= key <= 255 else ""

        if key_char == "P" and self.config.steady < 15:
            self.config.steady += 1
        elif key_char == "O" and self.config.steady > 3:
            self.config.steady -= 1
        elif key_char == "F" and self.config.fps < 100:
            self.config.fps += 1
            self.delay = 1.0 / self.config.fps
        elif key_char == "D" and self.config.fps > 20:
            self.config.fps -= 1
            self.delay = 1.0 / self.config.fps
        elif key_char == "B":
            self.config.bold = not self.config.bold
            self.renderer.reinit_colors()
            self._update_pipe_colors()
        elif key_char == "C":
            self.config.color = not self.config.color
            self.renderer.reinit_colors()
            self._update_pipe_colors()
        elif key_char == "K":
            self.config.keep_style = not self.config.keep_style
        elif key_char == "?" or key == 27:  # ESC
            return False
        return True
