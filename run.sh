#!/bin/bash
# AndroBF - Android PIN Brute-Force Toolkit
# Menu-driven front end

cd "$(dirname "$0")/src" || exit 1

banner() {
    clear
    echo "=============================================="
    echo "        AndroBF - PIN Brute-Force Tool"
    echo "        (Personal test device only)"
    echo "=============================================="
    echo ""
}

# Returns: 0 = connected & authorized, 1 = not connected, 2 = unauthorized, 3 = adb not installed
check_adb_status() {
    if ! command -v adb &> /dev/null; then
        return 3
    fi

    local output
    output=$(adb devices | grep -v "List of devices" | grep -v "^$")

    if [ -z "$output" ]; then
        return 1
    elif echo "$output" | grep -q "unauthorized"; then
        return 2
    elif echo "$output" | grep -q "device$"; then
        return 0
    else
        return 1
    fi
}

check_device() {
    echo "[*] Checking device connection..."
    echo ""

    check_adb_status
    status=$?

    case $status in
        0)
            echo "[+] Device connected and authorized."
            adb devices
            ;;
        1)
            echo "[!] ERROR: No device detected."
            echo "    - Check the USB cable connection."
            echo "    - If using VMware, confirm USB passthrough is enabled for this device"
            echo "      (VM Settings > USB Controller > connect device to guest)."
            echo "    - Confirm USB debugging is enabled on the phone (Developer Options)."
            ;;
        2)
            echo "[!] ERROR: Device detected but UNAUTHORIZED."
            echo "    - Look at your phone screen right now."
            echo "    - Accept the 'Allow USB debugging?' popup."
            echo "    - Then re-run this check."
            ;;
        3)
            echo "[!] ERROR: adb is not installed."
            echo "    - Run: sudo apt install -y android-tools-adb"
            ;;
    esac

    echo ""
    read -p "Press Enter to return to menu..."
}

# Guard used before any action that needs the phone
require_device() {
    check_adb_status
    status=$?
    if [ $status -ne 0 ]; then
        echo ""
        echo "[!] Cannot proceed — device not ready (run option 1 to see why)."
        read -p "Press Enter to return to menu..."
        return 1
    fi
    return 0
}

run_calibrate() {
    require_device || return
    echo "[*] Launching calibration..."
    python3 calibrate.py
    read -p "Press Enter to return to menu..."
}

run_manual() {
    require_device || return
    read -p "Enter PIN to try (4 digits): " pin
    if [[ ! $pin =~ ^[0-9]{4}$ ]]; then
        echo "[!] ERROR: Invalid PIN format. Must be exactly 4 digits (e.g. 0007)."
    else
        python3 brute_force.py --manual "$pin"
    fi
    read -p "Press Enter to return to menu..."
}

run_common_only() {
    require_device || return
    echo "[*] Running common-PIN list only..."
    python3 brute_force.py --common-only
    read -p "Press Enter to return to menu..."
}

run_full() {
    require_device || return
    echo "[*] Running full brute-force (common PINs first, then full sweep)..."
    python3 brute_force.py --full
    read -p "Press Enter to return to menu..."
}

view_log() {
    if [ ! -f ../logs/attempt_log.txt ]; then
        echo "[!] No log file yet — nothing has been run."
    else
        echo "[*] Last 30 log entries:"
        echo ""
        tail -n 30 ../logs/attempt_log.txt
    fi
    echo ""
    read -p "Press Enter to return to menu..."
}

while true; do
    banner
    echo "1) Check phone connectivity"
    echo "2) Run calibration"
    echo "3) Try a manual PIN"
    echo "4) Try common PINs only"
    echo "5) Full brute-force (common + sequential)"
    echo "6) View attempt log"
    echo "7) Exit"
    echo ""
    read -p "Select an option [1-7]: " choice

    case $choice in
        1) check_device ;;
        2) run_calibrate ;;
        3) run_manual ;;
        4) run_common_only ;;
        5) run_full ;;
        6) view_log ;;
        7) echo "Exiting."; exit 0 ;;
        *) echo "[!] Invalid option — choose a number between 1 and 7."; sleep 1 ;;
    esac
done

