# NAO Robot Teleoperation

## Requirements

**NAO Robot (the grey one):** NAOqi 2.8.6.23 (⚠️ Python 2.7 only), IP stored in `config.toml`

**MacBook Pro:** 2.6 GHz 6-Core Intel Core i7

## Environment Setup

Download and install Python 2.7.18 from [python.org](https://www.python.org/downloads/release/python-2718/) — required by the NAOqi Python SDK as it expects Python at `/Library/Frameworks/Python.framework/Versions/2.7/`.

Install `virtualenv` and create the virtual environment using the official Python 2.7:
```bash
mkdir nao_teleoperation
cd nao_teleoperation
/Library/Frameworks/Python.framework/Versions/2.7/bin/python -m pip install virtualenv
/Library/Frameworks/Python.framework/Versions/2.7/bin/python -m virtualenv nao_env
source nao_env/bin/activate
```

## NAOqi Python SDK Installation

Clone the community SDK repository for Mac:
```bash
cd ~
git clone https://github.com/cristianrubioa/pynaoqi-installation-for-mac
```

Set the environment variables and make them permanent:
```bash
echo 'export PYTHONPATH=${PYTHONPATH}:/Users/ada/pynaoqi-installation-for-mac/pynaoqi/lib/python2.7/site-packages' >> ~/.zshrc
echo 'export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/Users/ada/pynaoqi-installation-for-mac/pynaoqi/lib' >> ~/.zshrc
echo 'export QI_SDK_PREFIX=/Users/ada/pynaoqi-installation-for-mac/pynaoqi' >> ~/.zshrc
source ~/.zshrc
```

Verify the installation:
```bash
python test_naoqi.py
```

No error means the SDK is installed successfully.

## VS Code Setup

1. Install the **Python extension** by Microsoft (**⌘ + Shift + X** → search `Python`)
2. Open the project folder: **File → Open Folder** → select `nao_teleoperation`
3. Activate the virtual environment in the VS Code terminal:
```bash
source nao_env/bin/activate
```

4. Select the correct Python interpreter: **⌘ + Shift + P** → `Python: Select Interpreter` → `Enter interpreter path...` → `Find...` → navigate to `/Users/ada/nao_teleoperation/nao_env/bin/` and select `python`
5. Confirm the bottom left corner of VS Code shows `Python 2.7.18 ('nao_env')`

## References

[NAOqi 2.8 Python SDK official documentation](http://doc.aldebaran.com/2-8/dev/python/index.html)

[Community pynaoqi installation guide for Mac](https://github.com/cristianrubioa/pynaoqi-installation-for-mac)

[Python 2.7.18 download](https://www.python.org/downloads/release/python-2718/)
