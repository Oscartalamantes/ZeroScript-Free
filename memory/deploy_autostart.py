"""Bridge autostart launcher - run by the JunoZeroScriptBridge scheduled
task at every logon, under pythonw.exe (no console, nothing flashes on
Oscar's screens).

It starts bridge.py under python.exe with CREATE_NO_WINDOW and the
bridge's stdout/stderr captured to logs/bridge-autostart.log, then
exits - the bridge is a daemon, the launcher is not. This replaces the
old ritual of Oscar (or Juno) hand-running start.bat and babysitting
its terminal window.
"""

import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))  # ...\memory
ROOT = os.path.dirname(HERE)  # repo root (bridge.py lives there)
LOG = os.path.join(ROOT, "logs", "bridge-autostart.log")


def main() -> int:
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    bridge = os.path.join(ROOT, "bridge.py")
    # sys.executable is pythonw.exe here; bridge wants a real python.exe
    # (same install, sibling file) with a hidden console for its prints.
    py = os.path.join(os.path.dirname(sys.executable), "python.exe")
    if not os.path.exists(py):
        py = sys.executable
    with open(LOG, "a", encoding="utf-8") as f:
        f.write("\n=== autostart %s ===\n" % time.strftime("%Y-%m-%d %H:%M:%S"))
        f.flush()
        p = subprocess.Popen(
            [py, bridge],
            cwd=ROOT,
            stdout=f,
            stderr=subprocess.STDOUT,
            creationflags=0x08000000,  # CREATE_NO_WINDOW
        )
        f.write("bridge pid %d via %s\n" % (p.pid, py))
        f.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
