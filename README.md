# LS Copy Tool

A Windows desktop app to:
- Copy selected file types from one folder to another
- Optionally delete files based on name patterns
- Remember last 10 used folders
- Supports drag-and-drop folders
- Preview deletions before confirming

## Features

- Copy multiple file extensions (e.g., `.ls`, `.tp`)
- Enable or disable deletion step
- Preview deletions without removing anything
- Drag and drop folders into the app
- Settings saved in `%APPDATA%/LSCopyTool`

## Setup

```bash
pip install -r requirements.txt
python src/copy_filter_gui.py
```

## Build Windows .exe

Install dependencies and build with:

```bash
pyinstaller --onefile --noconsole ^
  --icon=assets/app_icon.ico ^
  --add-data "tkinterdnd2;tkinterdnd2" ^
  src/copy_filter_gui.py
```

## License

MIT
