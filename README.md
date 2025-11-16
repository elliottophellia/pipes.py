# pipes.py

A Python implementation of the classic [pipes.sh](https://github.com/pipeseroni/pipes.sh). Watch colorful pipes grow and spread across your terminal in mesmerizing patterns.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square) ![License](https://img.shields.io/badge/License-CC--BY--SA--4.0-green?style=flat-square) ![Version](https://img.shields.io/badge/Version-2.0.0-orange?style=flat-square)

[![Buy Me a Coffee](https://img.shields.io/badge/BUY%20ME%20A%20COFFEE-79B8CA?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/ReidhoSatria) [![Traktir Saya Kopi](https://img.shields.io/badge/TRAKTIR%20SAYA%20KOPI-FAC76C?style=for-the-badge&logo=BuyMeACoffee&logoColor=black)](https://saweria.co/elliottophellia)

## What's new in v2.0.0 ?!

Major rewrite. Here's what changed:

**Tooling:**
- Poetry → uv
- Added mypy (strict type checking)
- Added ruff (linter)
- Reorganized from `src/pipes/py/` to `src/pipes/`

**Code:**
- Split into modules instead of one big file
- Full type hints
- Better architecture

**Breaking:**
- Needs Python 3.10+
- Module path changed (but CLI is same)

All CLI arguments work the same. Config format is backwards compatible.

## Install

```bash
pip install pipes-py
```

Build from source:

```bash
git clone https://github.com/elliottophellia/pipes.py
cd pipes.py
uv build
pip install dist/pipes_py-2.0.0-py3-none-any.whl
```

## Usage

```bash
pipes-py                    # basic
pipes-py -p 5 -f 60         # 5 pipes at 60 fps
pipes-py -R -P 2            # random start with curved pipes
pipes-py -p 3 -C -B         # 3 pipes, no color, no bold
```

## Options

```
-p, --pipes N         number of pipes (default: 1)
-f, --fps N           frames per second, 20-100 (default: 75)
-s, --steady N        steadiness, 5-15 (default: 13)
-r, --limit N         character limit before screen reset
-R, --random          start pipes at random positions
-B, --no-bold         disable bold characters
-C, --no-color        disable colors
-P N                  pipe style 0-9 (default: 0)
-K, --keep-style      keep pipe style when wrapping around screen
-S, --save-config     save current settings as default
-v, --version         show version
```

Quit with `?` or `ESC`.

### Interactive keys

While running:
- `O` - decrease steadiness (more turns)
- `P` - increase steadiness (fewer turns)
- `D` - decrease FPS (slower)
- `F` - increase FPS (faster)
- `B` - toggle bold
- `C` - toggle color
- `K` - toggle keep style on wrap

## Pipe styles

10 styles available:

- `0` - heavy box-drawing (┃┏┓┛━)
- `1` - curved (│╭╮╯─)
- `2` - light box-drawing (│┌┐┘─)
- `3` - double box-drawing (║╔╗╝═)
- `4` - knobby (|+-+)
- `5` - angles (|/\-\)
- `6` - dots (.o...)
- `7` - dots with o (.ooo.)
- `8` - slashes (-\/|)
- `9` - mixed Unicode (╿┍┑┚╼)

Try them: `pipes-py -P 1 -p 3`

## Config

Config location:
- Linux/macOS: `~/.config/pipes-py/config.json`
- Windows: `%LOCALAPPDATA%\pipes-py\config.json`

```json
{
  "pipes": 1,
  "fps": 75,
  "steady": 13,
  "limit": 2000,
  "random_start": false,
  "bold": true,
  "color": true,
  "keep_style": false,
  "colors": [1, 2, 3, 4, 5, 6, 7, 0],
  "pipe_types": [0]
}
```

Use `-S` to save current settings or edit the file directly.

## Dev

```bash
git clone https://github.com/elliottophellia/pipes.py
cd pipes.py
uv sync
uv run python -m pipes

# checks
uv run ruff check src/pipes
uv run mypy src/pipes

# build
uv build
```

Code is in `src/pipes/`:
- `types.py` - enums/dataclasses
- `config.py` - file I/O
- `renderer.py` - drawing
- `pipes.py` - state
- `__main__.py` - CLI

## License

This project is licensed under the Creative Commons Attribution Share Alike 4.0 International (CC-BY-SA-4.0). For more information, please refer to the [LICENSE](LICENSE) file included in this repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Write your amazing code
4. Make sure pass `ruff check` and `mypy` first
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request
