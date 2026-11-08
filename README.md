
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

## Key Finding

On the primary test device (**POCO C31**, Android 10 / SDK 29, MIUI
12.0.10), unprivileged `adb shell input tap` against the lock screen fails
with:
