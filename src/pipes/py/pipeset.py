import curses
import locale
import random
import time
from typing import Dict, List

# Ensure correct handling of Unicode characters
locale.setlocale(locale.LC_ALL, '')

PIPE_SETS = [
    "┃┏ ┓┛━┓  ┗┃┛┗ ┏━",
    "│╭ ╮╯─╮  ╰│╯╰ ╭─",
    "│┌ ┐┘─┐  └│┘└ ┌─",
    "║╔ ╗╝═╗  ╚║╝╚ ╔═",
    "|+ ++-+  +|++ +-",
    "|/ \\ /-\\  \\|/\\ /-",
    ".. ....  .... ..",
    ".o oo.o  o.oo o.",
    "-\\ /\\|/  /-\\/ \\|",
    "╿┍ ┑┚╼┒  ┕╽┙┖ ┎╾",
]

class PipesScreen:
    def __init__(self, screen, config: dict):
        self.screen = screen
        self.config = config
        self.pipes: List[Dict] = []
        self.color_pairs = {}
        self.sets = self._prepare_sets()

        # Screen setup
        curses.curs_set(0)
        screen.nodelay(True)
        screen.clear()

        self._init_colors()
        self._init_pipes()

        self.height, self.width = screen.getmaxyx()
        self.count = 0
        self.delay = 1.0 / self.config["fps"]

    def _prepare_sets(self) -> List[str]:
        sets = []
        for s in PIPE_SETS:
            sets.extend((s + " " * 16)[:16])
        return sets

    def _init_colors(self):
        if not self.config["color"] or not curses.has_colors():
            self.color_pairs = {c: curses.A_NORMAL for c in self.config["colors"]}
            return

        curses.start_color()
        curses.use_default_colors()
        max_colors = min(curses.COLORS, 8)

        for idx, color in enumerate(self.config["colors"]):
            curses_color = color % max_colors
            pair_number = idx + 1
            curses.init_pair(pair_number, curses_color, -1)
            attr = curses.color_pair(pair_number)
            if self.config["bold"]:
                attr |= curses.A_BOLD
            self.color_pairs[color] = attr

    def _init_pipes(self):
        h, w = self.screen.getmaxyx()
        for i in range(self.config["pipes"]):
            direction = random.randrange(4) if self.config["random_start"] else 0
            x = random.randrange(w) if self.config["random_start"] else w // 2
            y = random.randrange(h) if self.config["random_start"] else h // 2

            pipe_type = random.choice(self.config["pipe_types"])
            color = random.choice(self.config["colors"])

            self.pipes.append({
                "x": x,
                "y": y,
                "direction": direction,
                "type": pipe_type,
                "attr": self.color_pairs[color]
            })

    def update(self) -> bool:
        key = self.screen.getch()
        if key != -1 and not self._handle_key(key):
            return False

        new_h, new_w = self.screen.getmaxyx()
        if new_h != self.height or new_w != self.width:
            self.height, self.width = new_h, new_w
            self.screen.clear()

        self._update_pipes()
        self.screen.refresh()

        self.count += len(self.pipes)
        if self.config["limit"] > 0 and self.count >= self.config["limit"]:
            self.screen.clear()
            self.count = 0

        time.sleep(self.delay)
        return True

    def _update_pipes(self):
        for pipe in self.pipes:
            x, y = pipe["x"], pipe["y"]
            direction = pipe["direction"]

            # Update position
            if direction % 2:
                x += (-direction + 2)
            else:
                y += (direction - 1)

            # Handle wrapping
            if (x < 0 or x >= self.width or y < 0 or y >= self.height):
                if not self.config["keep_style"]:
                    pipe["type"] = random.choice(self.config["pipe_types"])
                    color = random.choice(self.config["colors"])
                    pipe["attr"] = self.color_pairs[color]
                x %= self.width
                y %= self.height

            # Calculate new direction
            new_direction = direction
            if random.randrange(self.config["steady"]) <= 1:
                new_direction = (direction + (2 * random.randrange(2) - 1)) % 4

            # Draw pipe
            base = pipe["type"] * 16
            index = base + direction * 4 + new_direction
            char = self.sets[index] if index < len(self.sets) else "?"

            try:
                self.screen.addstr(y, x, char, pipe["attr"])
            except curses.error:
                pass

            pipe.update({
                "x": x,
                "y": y,
                "direction": new_direction
            })

    def _handle_key(self, key: int) -> bool:
        key_char = chr(key).upper() if 0 <= key <= 255 else ''

        if key_char == 'P' and self.config["steady"] < 15:
            self.config["steady"] += 1
        elif key_char == 'O' and self.config["steady"] > 3:
            self.config["steady"] -= 1
        elif key_char == 'F' and self.config["fps"] < 100:
            self.config["fps"] += 1
            self.delay = 1.0 / self.config["fps"]
        elif key_char == 'D' and self.config["fps"] > 20:
            self.config["fps"] -= 1
            self.delay = 1.0 / self.config["fps"]
        elif key_char == 'B':
            self.config["bold"] = not self.config["bold"]
            self._init_colors()
        elif key_char == 'C':
            self.config["color"] = not self.config["color"]
            self._init_colors()
        elif key_char == 'K':
            self.config["keep_style"] = not self.config["keep_style"]
        elif key_char == '?' or key == 27:  # ESC
            return False
        return True
