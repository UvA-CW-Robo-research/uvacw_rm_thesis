# NAO Robot Teleoperation

## Requirements

### NAO Robot
- NAOqi version: 2.8.6.23 (compatible with Python 3.6–3.9)
- IP: `192.168.0.102`

### MacBook Pro
- Processor: 2.6 GHz 6-Core Intel Core i7

---

## Environment Setup

### 1. Install pyenv via Homebrew
```bash
brew install pyenv
```

### 2. Install a compatible Python version
```bash
pyenv install 3.8.18
```

### 3. Set Python version locally for this project
```bash
cd your-project-folder
pyenv local 3.8.18
```

### 4. Verify
```bash
python --version
```

### 5. Create and activate a virtual environment
```bash
python -m venv nao_env
source nao_env/bin/activate
```
