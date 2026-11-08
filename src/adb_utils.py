import subprocess
import time
from config import ADB, CLEAR_DELAY, DIGIT_COORDS


def device_connected() -> bool:
    result = subprocess.run([ADB, "devices"], capture_output=True, text=True)
    lines = [l for l in result.stdout.splitlines() if l.strip() and "List of devices" not in l]
    return any("device" in l for l in lines)


def wake_screen():
    subprocess.run([ADB, "shell", "input", "keyevent", "KEYEVENT_WAKEUP"])
    time.sleep(0.5)


def tap(x: int, y: int):
    subprocess.run([ADB, "shell", "input", "tap", str(x), str(y)])
    time.sleep(CLEAR_DELAY)


def enter_pin(pin: str):
    wake_screen()
    for digit in pin:
        x, y = DIGIT_COORDS[digit]
        tap(x, y)


def get_window_policy_dump() -> str:
    result = subprocess.run(
        [ADB, "shell", "dumpsys", "window", "policy"],
        capture_output=True, text=True
    )
    return result.stdout


def is_unlocked() -> bool:
    output = get_window_policy_dump()
    return "mShowingLockscreen=false" in output or "isStatusBarKeyguard=false" in output


def is_locked_out() -> bool:
    output = get_window_policy_dump().lower()
    return "lockout" in output or "wait" in output


def screenshot(path: str):
    subprocess.run([ADB, "shell", "screencap", "-p", "/sdcard/_tmp_screencap.png"])
    subprocess.run([ADB, "pull", "/sdcard/_tmp_screencap.png", path])
    subprocess.run([ADB, "shell", "rm", "/sdcard/_tmp_screencap.png"])
