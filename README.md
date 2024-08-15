# Fenrir

## Overview

Fenrir is a screen recording tool built using Python. It allows users to select recording times, view GIFs, and perform basic editing operations.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Fenrir.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Fenrir
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Build the Executable

### Windows

Use the following command to build the executable for Windows:

```bash
pyinstaller --clean --onefile --add-data "images;images" --icon=icon.ico --noconsole --name=Fenrir windows/main.py
```

- `--clean`: Removes any temporary files before building.
- `--onefile`: Packages everything into a single executable.
- `--add-data "images;images"`: Includes the images folder in the build.
- `--icon=icon.ico`: Sets the application icon.
- `--noconsole`: Ensures no console window opens with the application.
- `--name=Fenrir`: Names the output executable as Fenrir.exe.

### macOS

Use the following command to build the executable for macOS:

```bash
pyinstaller --clean --onefile --add-data "images:images" --icon=icon.icns --noconsole --name=Fenrir macos/main.py
```

- `--clean`: Removes any temporary files before building.
- `--onefile`: Packages everything into a single executable.
- `--add-data "images:images"`: Includes the images folder in the build (note the colon `:` instead of a semicolon).
- `--icon=icon.icns`: Sets the application icon (macOS uses `.icns` files for icons).
- `--noconsole`: Ensures no console window opens with the application.
- `--name=Fenrir`: Names the output executable as Fenrir.app.

## Usage

Run the executable to launch the Fenrir application. The application will provide options to record your screen and edit GIFs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
