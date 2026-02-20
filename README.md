# NAO Robot Teleoperation

## Requirements

**NAO Robot:** NAOqi 2.8.6.23 (compatible with Python 2.7 ONLY), IP stored in `config.toml`

**MacBook Pro:** 2.6 GHz 6-Core Intel Core i7

## Environment Setup

```bash
# Install pyenv via Homebrew
brew install pyenv

# Install a compatible Python version
pyenv install 2.7.18

# Set Python version locally for this project
mkdir nao_teleoperation
cd nao_teleoperation
pyenv local 2.7.18

# Verify
python --version

# Create and activate a virtual environment
python -m venv nao_env
source nao_env/bin/activate
```

## References
[NAOqi 2.8 Python SDK official documentation](http://doc.aldebaran.com/2-8/dev/python/index.html)
