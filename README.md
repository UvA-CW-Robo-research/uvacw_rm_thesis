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

Verify the installation by running the test script found in [test_naoqi.py](https://github.com/adashiyj/uvacw_rm_thesis/blob/main/code/test_naoqi.py):
```bash
python code/test_naoqi.py
```

Seeing "NAOqi imported successfully!" means the SDK is installed successfully.

## VS Code Setup

1. Install the **Python extension** by Microsoft (**⌘ + Shift + X** → search `Python`)
2. Open the project folder: **File → Open Folder** → select `nao_teleoperation`
3. Activate the virtual environment in the VS Code terminal:
```bash
source nao_env/bin/activate
```

4. Select the correct Python interpreter: **⌘ + Shift + P** → `Python: Select Interpreter` → `Enter interpreter path...` → `Find...` → navigate to `/Users/ada/nao_teleoperation/nao_env/bin/` and select `python`
5. Confirm the bottom right corner of VS Code shows `Python 2.7.18 ('nao_env')`

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

NAO will stand up, enable face tracking, and wait for your input. Use the following keyboard controls during the session:

| Key | Action |
|-----|--------|
| `Enter` | Advance to next step |
| `N` | Nod (listening gesture) |
| `F` | Trigger failure sequence |
| `W` | Wave (hello or goodbye) |
| `Esc` | Safe shutdown |

## Experiment Script Architecture

The experiment script is organized across four files in the `code/` folder:

`script.py` contains all 24 steps of the session organized by condition. Each step is a tuple of a type and content, for example `("speech", "Hello!")` or `("wait", "Wait for response.")`. The four step types are `speech` (NAO speaks the line), `wait` (experimenter action required), `failure` (triggers the freeze sequence), and `gesture` (triggers a physical gesture).

`gestures.py` handles all physical behaviors — the hello and goodbye wave, the nodding listening gesture, the 5-second failure sequence with red LED eyes, and natural blinking during speech. It also manages the robot connection and returns all NAOqi proxies.

`controller.py` listens for keyboard input and controls the flow of the session. It advances through the script step by step, triggering the appropriate speech or gesture for each step type.

`main.py` is the entry point. It loads `config.toml`, prompts for the condition, connects to the robot, stands it up, enables face tracking and breathing animation, and hands control to the controller. On exit it safely shuts the robot down.

## References

[NAOqi 2.8 Python SDK official documentation](http://doc.aldebaran.com/2-8/dev/python/index.html)

[Python 2.7.18 download](https://www.python.org/downloads/release/python-2718/)

[Community pynaoqi installation guide for Mac](https://github.com/cristianrubioa/pynaoqi-installation-for-mac)


