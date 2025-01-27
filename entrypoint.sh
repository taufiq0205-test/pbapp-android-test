#!/bin/bash

# Start Appium with increased timeout
appium --relaxed-security --allow-insecure=adb_shell --session-override --log appium.log &
APPIUM_PID=$!
sleep 20  # Increased wait time

# Connect and prepare device
adb connect host.docker.internal:5555

# Clean existing Appium Settings
adb -s host.docker.internal:5555 uninstall io.appium.settings || true

# Install fresh Appium Settings
adb -s host.docker.internal:5555 install \
  /root/.appium/node_modules/appium-uiautomator2-driver/node_modules/io.appium.settings/apks/settings_apk-debug.apk

# Grant permissions
adb -s host.docker.internal:5555 shell pm grant io.appium.settings android.permission.WRITE_SECURE_SETTINGS
adb -s host.docker.internal:5555 shell pm grant io.appium.settings android.permission.CHANGE_CONFIGURATION

# Start settings app
adb -s host.docker.internal:5555 shell am start -n io.appium.settings/.Settings

# Add verification
echo "Checking Appium Settings status:"
adb -s host.docker.internal:5555 shell "ps | grep io.appium.settings"

# Run tests
pytest tests/critical_suite.py \
  -v \
  --alluredir=./allure-results \
  -k "TestPhotobook and test_TCA1002_LOGIN"

# Generate report
allure generate allure-results -o allure-report --clean

# Cleanup
kill $APPIUM_PID