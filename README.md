# NAO Robot Teleoperation

## Requirements

**NAO Robot:** NAOqi 2.8.6.23 (compatible with Python 3.6–3.9), IP stored in `config.yaml`

**MacBook Pro:** 2.6 GHz 6-Core Intel Core i7

## Environment Setup

Install pyenv via Homebrew and set up a compatible Python version:
```bash
brew install pyenv
pyenv install 3.8.18
cd your-project-folder
pyenv local 3.8.18
python --version
```

Create and activate a virtual environment:
```bash
python -m venv nao_env
source nao_env/bin/activate
```
