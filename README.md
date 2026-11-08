
# AndroBF — Android PIN Brute-Force (Learning Project)

A personal, educational project exploring how 4-digit PIN brute-forcing works
against Android lock screens, how Android defends against it, and the
practical limits of unprivileged automation (`adb`) versus rooted access.

> ⚠️ **For use only on a personal, wiped, no-data test device with USB
> debugging enabled by the owner.** This project is not intended for use
> against any device you do not own or have explicit permission to test.

---

## Project Goal

Build a brute-force tool that:
1. Connects to an Android device via `adb`
2. Simulates PIN entry on the lock screen (0000–9999)
3. Prioritizes statistically common PINs before a full sequential sweep
4. Detects lockouts and backs off appropriately
5. Logs progress and resumes if interrupted

Along the way, the project became a practical lesson in **why this doesn't
just work out of the box** on modern Android.

---


This confirms that modern Android blocks synthetic input injection into
secure system windows (like the keyguard) unless the shell has elevated
(root) privileges. This is a deliberate OS-level defense — not a bug in
this project's code.

**Workarounds explored:**
- Rooting the physical device via Magisk (requires bootloader unlock, full
  data wipe, and a wait period via Xiaomi's official Mi Unlock process)
- Testing against a rooted virtual device (Genymotion) instead, which
  bypasses the permission wall without touching the physical phone

---

## Project Structure
AndroBF/
├── README.md
├── requirements.txt
├── .gitignore
├── run.sh # menu-driven bash front end
├── data/
│ └── common_pins.txt # prioritized list of common PINs
├── src/
│ ├── config.py # device-specific tunables (coordinates, delays)
│ ├── adb_utils.py # shared adb wrapper functions
│ ├── calibrate.py # taps each digit once, for coordinate calibration
│ └── brute_force.py # main brute-force logic (common PINs → full sweep)
├── logs/ # gitignored — runtime attempt logs
└── screenshots/ # gitignored — calibration reference images

---

## Setup

### 1. Requirements
```bash
sudo apt update
sudo apt install -y android-tools-adb python3
```

### 2. Connect your test device
- Enable Developer Options and USB debugging on the device
- Connect via USB (or configure USB passthrough if running Kali in a VM)
- Accept the "Allow USB debugging?" prompt on the device screen
- Verify:
```bash
adb devices
```

### 3. Calibrate tap coordinates
Lock screen layouts vary by device/resolution. Run calibration first:
```bash
cd src
python3 calibrate.py
```
Update `DIGIT_COORDS` in `config.py` if any tap misses its intended digit.

---

## Usage

Run the menu-driven interface from the project root:
```bash
./run.sh
```

Menu options:
1. **Check phone connectivity** — verifies adb connection/authorization
2. **Run calibration** — confirms tap coordinates
3. **Try a manual PIN** — test a single 4-digit PIN
4. **Try common PINs only** — runs the prioritized common-PIN list
5. **Full brute-force** — common PINs first, then full 0000–9999 sweep
6. **View attempt log** — shows recent attempt history

Progress is logged to `logs/attempt_log.txt` and automatically resumed on
restart (already-tried PINs are skipped).

---

## How It Works (Summary)

1. **Wake** the screen via `adb shell input keyevent`
2. **Enter PIN** by tapping calibrated digit coordinates in sequence
3. **Check result** via `adb shell dumpsys window policy` (lock state)
4. **Detect lockout** and back off if Android's attempt-delay kicks in
5. **Prioritize** common PINs (`1234`, `0000`, `1111`, keypad patterns like
   `2580`/`1470`, etc.) before falling back to a full sequential sweep

---

## Known Limitations

- Unprivileged `adb` cannot inject input into the lock screen on Android
  10+ without root (`INJECT_EVENTS` permission required)
- Tap coordinates are device/resolution-specific and must be recalibrated
  per device
- Lockout-detection strings in `dumpsys` output vary by Android
  version/OEM skin and should be verified per device before relying on them

---

## Device(s) Tested

| Device | Android Version | Root Status | Result |
|---|---|---|---|
| POCO C31 | 10 (SDK 29) | Not rooted | Blocked by `INJECT_EVENTS` permission |
| _(fill in: Genymotion / rooted device)_ | | | |

---

## Disclaimer

This project is for personal educational use on devices the author owns
and controls. It is not intended to facilitate unauthorized access to any
device. Understanding offensive techniques is a legitimate and common part
of learning defensive security — use responsibly.
EOF
