@echo off
pyinstaller --onefile --noconsole ^
  --icon=assets\app_icon.ico ^
  --add-data "tkinterdnd2;tkinterdnd2" ^
  src\copy_filter_gui.py

mkdir package
copy dist\copy_filter_gui.exe package\
copy README.md package\
copy assets\app_icon.ico package\
cd package
tar -a -c -f ../LSCopyTool_Windows.zip *
cd ..
echo Done.
