# NAO Robot Teleoperation

## Requirements

**NAO Robot (the grey one):** NAOqi 2.8.6.23 (⚠️ Python 2.7 only), IP stored in `config.toml`

**MacBook Pro:** 2.6 GHz 6-Core Intel Core i7

---

## First Time Setup

### 1. Python 2.7.18
Download and install from [python.org](https://www.python.org/downloads/release/python-2718/) — required by the NAOqi SDK at `/Library/Frameworks/Python.framework/Versions/2.7/`.

### 2. Virtual Environment
```bash
mkdir nao_teleoperation
cd nao_teleoperation
/Library/Frameworks/Python.framework/Versions/2.7/bin/python -m pip install virtualenv
/Library/Frameworks/Python.framework/Versions/2.7/bin/python -m virtualenv nao_env
source nao_env/bin/activate
```

### 3. NAOqi Python SDK

> ⚠️ The [Aldebaran Community](https://community.aldebaran.com/en/resources/software) website is expired and the SDK can no longer be downloaded through the official channel. Also note that the official SDK only supports Python 2.7 — see [NAOqi 2.8 Python install guide](http://doc.aldebaran.com/2-8/dev/python/install_guide.html) for reference.

As an alternative, clone the community SDK repository for Mac:
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

Verify by running `python code/connection_test.py` to check if NAO's connection is successful.

### 4. VS Code
1. Install the **Python extension** by Microsoft (**⌘ + Shift + X** → search `Python`)
2. Open the project folder: **File → Open Folder** → select `nao_teleoperation`
3. Select the correct Python interpreter: **⌘ + Shift + P** → `Python: Select Interpreter` → `Enter interpreter path...` → `Find...` → navigate to `.../nao_teleoperation/nao_env/bin/` and select `python`
4. Confirm the bottom right corner of VS Code shows `Python 2.7.18 ('nao_env')`

---

## Every Session

Activate the virtual environment in the terminal:
```bash
cd ~/nao_teleoperation
source nao_env/bin/activate
```

---

## Running the Experiment

Make sure the robot is on and connected to the same network, then run:
```bash
python code/main.py
```

Enter the condition number when prompted:
```
1: Team Identity + Humor
2: Team Identity + No Humor
3: No Team Identity + Humor
4: No Team Identity + No Humor
```

NAO will sit down, enable face tracking, and wait for your input:

| Key | Action |
|-----|--------|
| `Enter` | Advance to next step |
| `N` | Nod (listening gesture) |
| `F` | Trigger failure sequence |
| `W` | Wave (hello or goodbye) |
| `Esc` | Safe shutdown |

---

## Code Architecture
```
nao_teleoperation/
├── code/
│   ├── __init__.py           # Makes code/ a Python package
│   ├── main.py               # Entry point — connects to robot, loads condition, starts session
│   ├── script.py             # All 24 dialogue steps organized by condition (1–4)
│   ├── gestures.py           # Physical behaviors — wave, nod, blink, failure sequence
│   ├── controller.py         # Keyboard input — controls session flow step by step
│   └── connection_test.py    # Tests robot connection
└── config.toml               # Robot IP, port, motion and logging settings
```

Each step in the script is a tuple of `(type, content)`:

| Type | Triggered by | Description |
|------|-------------|-------------|
| `speech` | `Enter` | NAO speaks the line with natural blinking |
| `wait` | `Enter` | Pause shown in terminal for experimenter action |
| `failure` | `F` | 5-second natural freeze — speech and blinking stop abruptly |
| `gesture` | `W` | Wave hello or goodbye |

## NAO Voice Settings

| Parameter | Value |
|-----------|-------|
| Voice | `naoenu` |
| Speed | `75` |
| Pitch | `0.9` |
| Volume | `100` |

---

## References

[NAOqi 2.8 Python SDK official documentation](http://doc.aldebaran.com/2-8/dev/python/index.html)

[Python 2.7.18 download](https://www.python.org/downloads/release/python-2718/)

[Community pynaoqi installation guide for Mac](https://github.com/cristianrubioa/pynaoqi-installation-for-mac)
