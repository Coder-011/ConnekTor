# ConnekTor CI Hardening & Smoke Tests

## Overview

This directory contains scripts and documentation for running smoke tests and verifying the ConnekTor Android build pipeline.

## Smoke Test Script

### `ci_smoke_test.sh` - APK Installation & Launch Test

Validates that:
- The APK file is properly built and signed
- APK installs successfully on target device/emulator
- App process starts without immediate crashes
- Basic device connectivity works

### Local Usage

**Prerequisites:**
- Android SDK with `adb` command available
- Android emulator running or device connected via USB
- Built APK in `bin/connektor-debug.apk`

**Run against default emulator:**
```bash
bash scripts/ci_smoke_test.sh
```

**Run against specific device:**
```bash
bash scripts/ci_smoke_test.sh bin/connektor-debug.apk emulator-5554
```

**Run against physical device:**
```bash
# List connected devices
adb devices

# Run test on specific device
bash scripts/ci_smoke_test.sh bin/connektor-debug.apk <device-serial>
```

### Example Output

```
[INFO] APK found: bin/connektor-debug.apk (45.2M)
[INFO] adb version: Android Debug Bridge version 1.0.41
[INFO] Target device: emulator-5554
[INFO] Clearing previous installation of org.citpc.connektor...
[INFO] Installing APK...
[INFO] ✓ APK installed successfully
[INFO] Launching app...
[INFO] ✓ App launch command sent
[INFO] Waiting for app to start (up to 30s)...
[INFO] ✓ App process running (PID: 12345)
[INFO] Checking app logs...
[INFO] ✓ Network accessible from device
[INFO] ✓ No obvious crashes detected in logs

============================================
Smoke test completed successfully!
✓ APK installed and app launched
✓ App process verified
============================================
```

## CI Integration

The GitHub Actions workflow (`.github/workflows/build.yml`) includes:

### Python & Dependency Pinning
- **Python 3.10.13**: Pinned for compatibility with Kivy 2.3.0 and NDK
- **Cython 0.29.32**: Matched to Kivy 2.3.0 C extension build
- **python-for-android 2024.1214**: Stable release for Android build toolchain

### Debug Information Collected
- Python version confirmation
- Installed dependency versions (p4a, Cython, buildozer)
- Buildozer cache state and Python header paths

### Build Log Collection
On build failure, the workflow automatically:
- Collects build logs from `.buildozer` directory
- Captures compiler output and error details
- Uploads logs as CI artifact for debugging

### Artifact Caching
- **Buildozer global cache**: Keyed on `buildozer.spec` and workflow changes
- **Buildozer build cache**: Keyed on spec, date, and requirements to balance freshness and speed

## Troubleshooting Build Failures

### Check Python Header Paths

If compilation fails with `_Py*` symbol errors:

```bash
# Locally, in CI debug logs, look for:
# "=== .buildozer/.../python3.10/include"

# The include directory should match the pinned Python version (3.10.13)
# If it shows 3.9, 3.11, etc., adjust buildozer.spec and retry
```

### Verify Cython/p4a Versions

```bash
# Check CI logs for:
pip show python-for-android Cython buildozer

# Locally:
pip install python-for-android==2024.1214 Cython==0.29.32
buildozer android debug --verbose
```

### Rebuild with Fresh Cache

If you suspect stale cache corruption:

```bash
# Delete local caches
rm -rf .buildozer .buildozer_global

# Rebuild
buildozer android debug
```

In CI, restart the workflow to evict cache.

## Future Enhancements

- [ ] Add emulator smoke test to CI workflow (requires cloud emulator setup)
- [ ] Integrate with Android Test Lab for device matrix testing
- [ ] Add UI automation tests (Appium/Espresso)
- [ ] Implement performance profiling (APK size, startup time)
- [ ] Add code signing and release APK builds
