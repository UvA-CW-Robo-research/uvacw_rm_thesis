# NAO Robot Teleoperation

## Requirements

**NAO Robot:** NAOqi 2.8.6.23 (compatible with Python 3.6–3.9), IP stored in `config.toml`

**MacBook Pro:** 2.6 GHz 6-Core Intel Core i7

## Environment Setup

```bash
# Install pyenv via Homebrew
brew install pyenv

# Install a compatible Python version
pyenv install 3.8.18

# Set Python version locally for this project
mkdir nao_teleoperation
cd nao_teleoperation
pyenv local 3.8.18

# Verify
python --version

# Create and activate a virtual environment
python -m venv nao_env
source nao_env/bin/activate
```
