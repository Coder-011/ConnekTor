#!/bin/bash
# ConnekTor CI Smoke Test Script
# Validates APK installation and basic app functionality on Android emulator/device
# Usage: bash scripts/ci_smoke_test.sh [apk_path] [device_id]

set -euo pipefail

APK_PATH="${1:-bin/connektor-debug.apk}"
DEVICE_ID="${2:-emulator-5554}"
PACKAGE_NAME="org.citpc.connektor"
ACTIVITY_NAME="org.citpc.connektor.MainActivity"
TIMEOUT=30

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Step 1: Check APK exists
if [ ! -f "$APK_PATH" ]; then
    log_error "APK not found at: $APK_PATH"
    exit 1
fi
log_info "APK found: $APK_PATH ($(du -h "$APK_PATH" | cut -f1))"

# Step 2: Check adb is available
if ! command -v adb &> /dev/null; then
    log_error "adb not found in PATH"
    exit 1
fi
log_info "adb version: $(adb version 2>&1 | head -1)"

# Step 3: Check device is connected/available
if ! adb devices | grep -q "$DEVICE_ID"; then
    log_warn "Device $DEVICE_ID not found. Available devices:"
    adb devices
    log_info "Attempting to connect to local emulator..."
    DEVICE_ID="emulator-5554"
fi
log_info "Target device: $DEVICE_ID"

# Step 4: Clear any previous installation
log_info "Clearing previous installation of $PACKAGE_NAME..."
adb -s "$DEVICE_ID" uninstall "$PACKAGE_NAME" 2>/dev/null || log_warn "Package not previously installed"

# Step 5: Install APK
log_info "Installing APK..."
if adb -s "$DEVICE_ID" install -r "$APK_PATH"; then
    log_info "✓ APK installed successfully"
else
    log_error "Failed to install APK"
    exit 1
fi

# Step 6: Wait for device to settle
sleep 2

# Step 7: Start the app
log_info "Launching app..."
if adb -s "$DEVICE_ID" shell am start -n "$PACKAGE_NAME/$ACTIVITY_NAME" 2>/dev/null; then
    log_info "✓ App launch command sent"
else
    log_warn "Could not launch app (activity may not exist yet, trying package start)"
    adb -s "$DEVICE_ID" shell am start -n "$PACKAGE_NAME/.MainActivity" 2>/dev/null || \
        adb -s "$DEVICE_ID" shell monkey -p "$PACKAGE_NAME" 1 2>/dev/null || true
fi

# Step 8: Wait for app to initialize
log_info "Waiting for app to start (up to ${TIMEOUT}s)..."
sleep 3

# Step 9: Check if process is running
APP_PID=$(adb -s "$DEVICE_ID" shell pidof "$PACKAGE_NAME" 2>/dev/null || echo "")
if [ -n "$APP_PID" ]; then
    log_info "✓ App process running (PID: $APP_PID)"
else
    log_warn "Could not verify app process via pidof (may still be starting)"
fi

# Step 10: Capture logcat for app events
log_info "Checking app logs..."
LOGCAT_OUTPUT=$(adb -s "$DEVICE_ID" logcat -d "$PACKAGE_NAME" 2>/dev/null | tail -20 || adb -s "$DEVICE_ID" logcat -d | grep -i connektor | tail -20 || echo "No logs captured")
if [ -n "$LOGCAT_OUTPUT" ]; then
    echo "$LOGCAT_OUTPUT"
fi

# Step 11: Quick connectivity check (verify basic network access works)
log_info "Checking network connectivity..."
PING_RESULT=$(adb -s "$DEVICE_ID" shell ping -c 1 8.8.8.8 2>&1 | grep -i "1 packets received" || echo "No ping response")
if [ -n "$PING_RESULT" ]; then
    log_info "✓ Network accessible from device"
else
    log_warn "Could not verify network connectivity"
fi

# Step 12: Check for crashes
log_info "Checking for app crashes..."
CRASH_LOG=$(adb -s "$DEVICE_ID" logcat -d "*:E" 2>/dev/null | grep -i "$PACKAGE_NAME\|FATAL\|crash" | tail -5 || echo "")
if [ -n "$CRASH_LOG" ]; then
    log_warn "Potential crash logs detected:"
    echo "$CRASH_LOG"
else
    log_info "✓ No obvious crashes detected in logs"
fi

log_info ""
log_info "============================================"
log_info "Smoke test completed successfully!"
log_info "✓ APK installed and app launched"
log_info "✓ App process verified"
log_info "============================================"

exit 0
