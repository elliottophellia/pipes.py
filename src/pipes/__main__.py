"""Command-line interface for pipes."""

import argparse
import curses
import sys
from pipes import __version__
from pipes.config import load_config, save_config
from pipes.pipes import PipesScreen
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Basically pipes.sh but rewritten in Python",
        formatter_class=argparse.HelpFormatter,
    )

    parser.add_argument("-p", "--pipes", type=int, help="number of pipes")
    parser.add_argument("-f", "--fps", type=int, help="frames per second (20-100)")
    parser.add_argument("-s", "--steady", type=int, help="steadiness (5-15)")
    parser.add_argument("-r", "--limit", type=int, help="character limit before reset")
    parser.add_argument("-R", "--random", action="store_true", help="random start")
    parser.add_argument("-B", "--no-bold", action="store_true", help="disable bold")
    parser.add_argument("-C", "--no-color", action="store_true", help="disable color")
    parser.add_argument(
        "-P",
        "--pipe-style",
        type=int,
        choices=range(10),
        help="change pipe style (0-9)",
    )
    parser.add_argument(
        "-K", "--keep-style", action="store_true", help="keep style on wrap"
    )
    parser.add_argument(
        "-S",
        "--save-config",
        action="store_true",
        help="save current settings as default",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"pipes-py v{__version__}"
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point for the application."""
    args = parse_args()
    config = load_config()

    # Update config with command line arguments
    if args.pipes is not None:
        config.pipes = max(1, args.pipes)
    if args.fps is not None:
        config.fps = max(20, min(100, args.fps))
    if args.steady is not None:
        config.steady = max(5, min(15, args.steady))
    if args.limit is not None:
        config.limit = max(0, args.limit)
    if args.random:
        config.random_start = True
    if args.no_bold:
        config.bold = False
    if args.no_color:
        config.color = False
    if args.keep_style:
        config.keep_style = True
    if args.pipe_style is not None:
        config.pipe_types = [args.pipe_style]

    if args.save_config:
        save_config(config)

    try:
        curses.wrapper(lambda screen: run_pipes(screen, config))
    except KeyboardInterrupt:
        sys.exit(0)


def run_pipes(screen: Any, config: Any) -> None:
    """Run the pipes animation.

    Args:
        screen: Curses screen object
        config: Pipe configuration
    """
    pipes = PipesScreen(screen, config)
    while pipes.update():
        pass


if __name__ == "__main__":
    main()
