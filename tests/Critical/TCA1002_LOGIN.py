import subprocess
import time
from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def verify_app_installed():
    result = subprocess.run(['adb', 'shell', 'pm', 'list', 'packages', 'com.photobook.android.staging'],
                          capture_output=True, text=True)
    return 'com.photobook.android.staging' in result.stdout

def launch_app_manually():
    # Force stop the app first
    subprocess.run(['adb', 'shell', 'am', 'force-stop', 'com.photobook.android.staging'])
    time.sleep(2)

    # Launch the app
    subprocess.run([
        'adb', 'shell', 'monkey', '-p',
        'com.photobook.android.staging', '-c',
        'android.intent.category.LAUNCHER', '1'
    ])

def wait_for_element(driver, locator, timeout=30):
    """Wait for an element to be present and visible"""
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.presence_of_element_located(locator))
        wait.until(EC.visibility_of(element))
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {locator}")
        return None

# Appium server URL
url = 'http://localhost:4723'

# Appium capabilities
cap:Dict[str, Any]={
    'platformName': "Android",
    'automationName': "UiAutomator2",
    'deviceName': "emulator-5554",
    'appPackage': "com.photobook.android.staging",
    'appActivity': "com.photobook.android.page.applaunch.AppLaunchActivity",
    'noReset': True,  # Changed to preserve settings
    'autoGrantPermissions': True,
    'uiautomator2ServerInstallTimeout': 120000,
    'adbExecTimeout': 120000,
    'systemPort': 8200,  # Add unique port
    'skipDeviceInitialization': False,
    'skipServerInstallation': False
}

try:
    # Verify app installation
    if not verify_app_installed():
        print("Error: App is not installed on the device")
        exit(1)

    # Launch app manually first
    print("Launching app manually...")
    launch_app_manually()
    
    # Initialize the driver
    print("Initializing Appium driver...")
    driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(cap))
    
    print("Waiting for app to fully load...")
    
    # Wait for the Photobook main page element to be present (indicates app is loaded)
    wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Account"), timeout=30)

    print("App is fully loaded!")

    #Login with Photobook credentials
    print("Begin TCA1001_LOGIN test execution...")
    account = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Account")
    account.click()

    time.sleep(3)

    navigate_login = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Button\").instance(0)")
    navigate_login.click()

    time.sleep(3)

    email = driver.find_element(by=AppiumBy.ID, value="com.photobook.android.staging:id/emailEditText")
    email.click()
    email.send_keys("autobots_ui_login@photobookworldwide.com")

    password = driver.find_element(by=AppiumBy.ID, value="com.photobook.android.staging:id/passwordEditText")
    password.click()
    password.send_keys("Testing@123")

    login_button = driver.find_element(by=AppiumBy.ID, value="com.photobook.android.staging:id/loginButton")
    login_button.click()

    print("Successfully logged in!")

    time.sleep(3)

    #Logout
    print("Logging out...")
    time.sleep(5)

    #Scroll down to the logout button
    for _ in range(2):  # Try scrolling up to 2 times
        driver.execute_script('mobile: scrollGesture', {
            'left': 100, 
            'top': 1000,  # Start from lower on the screen
            'width': 200, 
            'height': 1000,
            'direction': 'down',
            'percent': 1.0  # Maximum scroll percentage
        })
        time.sleep(1)  # Short wait between scrolls
    
    time.sleep(2) 

    logout_button = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Button\").instance(10)")
    logout_button.click()

    time.sleep(1)
    logout_okay_button = driver.find_element(by=AppiumBy.ID, value="com.photobook.android.staging:id/verticalDialogOkayButton")
    logout_okay_button.click()

    print("Successfully logged out!")

    time.sleep(2)
    print("TCA1001_LOGIN test execution completed successfully!")
    


except Exception as e:
    print(f"Test failed with error: {str(e)}")

finally:
    try:
        if 'driver' in locals():
            print("Cleaning up...")
            driver.quit()
            print("Cleanup completed successfully!")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")