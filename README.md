# Windows network reset

Simple GUI tool to reset Windows network adapters.

Lazy man's way to reset network adapters.

Run as administrator...

## Build

```console

py -3.8 -m venv env
env\scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
pip list --outdated

pyinstaller --name NetworkReset --paths ".\env\Lib\site-packages\PyQt5\Qt\bin" --clean --onefile --windowed --icon=app.ico app.py

```
