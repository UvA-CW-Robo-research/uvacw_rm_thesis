# NAO Robot Teleoperation

## Requirements

**NAO Robot:** NAOqi 2.8.6.23 (Python 2.7 only), IP stored in `config.toml`

**MacBook Pro:** 2.6 GHz 6-Core Intel Core i7

## Environment Setup

Install pyenv via Homebrew and set up a compatible Python version:
```bash
brew install pyenv
pyenv install 2.7.18
```

Create the project folder and set the Python version locally:
```bash
mkdir nao_teleoperation
cd nao_teleoperation
pyenv local 2.7.18
python --version
```

Install virtualenv and create the virtual environment:
```bash
pip install virtualenv
python -m virtualenv nao_env
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
python
>>> import naoqi
```

No error means the SDK is installed successfully.

## References

[NAOqi 2.8 Python SDK official documentation](http://doc.aldebaran.com/2-8/dev/python/index.html)

[Community pynaoqi installation guide for Mac](https://github.com/cristianrubioa/pynaoqi-installation-for-mac)
