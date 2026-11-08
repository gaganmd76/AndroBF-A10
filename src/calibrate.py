import time
from adb_utils import device_connected, wake_screen, tap, screenshot
from config import DIGIT_COORDS


def main():
    if not device_connected():
        print("[!] No device detected. Run `adb devices` and check your connection.")
        return

    print("[*] Taking reference screenshot of current lock screen...")
    wake_screen()
    screenshot("../screenshots/lockscreen_reference.png")
    print("[*] Saved to screenshots/lockscreen_reference.png\n")

    input("Press Enter to start tapping each digit one by one...")

    for digit, (x, y) in sorted(DIGIT_COORDS.items()):
        print(f"[*] Tapping digit '{digit}' at ({x},{y}) — check the phone now.")
        tap(x, y)
        time.sleep(2)
        input("   Press Enter to continue to next digit...")

    print("\n[*] Calibration pass complete. Update config.py if any coordinates were off.")


if __name__ == "__main__":
    main()
