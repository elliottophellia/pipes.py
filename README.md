# Pipes.py
A Python implementation of the classic pipes.sh. Watch colorful pipes grow and spread across your terminal in mesmerizing patterns.


![Python](https://img.shields.io/badge/PYTHON-3.X-bf616a?style=flat-square) ![License](https://img.shields.io/badge/LICENCE-CC%20BY%20SA%204.0-ebcb8b?style=flat-square) ![Version](https://img.shields.io/badge/VERSION-1.0.0-a3be8c?style=flat-square)

[![Buy Me a Coffee](https://img.shields.io/badge/BUY%20ME%20A%20COFFEE-79B8CA?style=for-the-badge&logo=paypal&logoColor=white)](https://paypal.me/ReidhoSatria) [![Traktir Saya Kopi](https://img.shields.io/badge/TRAKTIR%20SAYA%20KOPI-FAC76C?style=for-the-badge&logo=BuyMeACoffee&logoColor=black)](https://saweria.co/elliottophellia)


## Features

- Multiple pipe styles (10 different types)
- Customizable colors and animations
- Adjustable speed and steadiness
- Configuration saving
- Bold and color options
- Random start positions

## Installation

### Release
```bash
# Install using pipx
pipx install pipes-py
```

### Build from Source
```bash
# Clone the repository
git clone https://github.com/elliottophellia/pipes.py

# Change directory
cd pipes.py

# Build the package
poetry build

# Install the package
pipx install dist/pipes_py-1.0.0.tar.gz
```

## Usage

```bash
pipes-py
```

### Command Line Options

- `-p, --pipes N`: Set number of pipes (default: 1)
- `-f, --fps N`: Set frames per second (20-100, default: 75)
- `-s, --steady N`: Set steadiness (5-15, default: 13)
- `-r, --limit N`: Set character limit before reset
- `-R, --random`: Enable random start positions
- `-B, --no-bold`: Disable bold characters
- `-C, --no-color`: Disable colors
- `-P N, --pipe-style N`: Set pipe style (0-9)
- `-K, --keep-style`: Keep pipe style when wrapping
- `-S, --save-config`: Save current settings as default
- `-v, --version`: Show version information

## Configuration

The program stores its configuration in `~/.config/pipes-py/config.json`. You can modify this file directly or use the `-S` option to save your current settings.

Default configuration:
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

## License

This project is licensed under the Creative Commons Attribution Share Alike 4.0 International (CC-BY-SA-4.0). For more information, please refer to the [LICENSE](LICENSE) file included in this repository.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
