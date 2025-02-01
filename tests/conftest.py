# tests/conftest.py
import os
import pytest
import allure
from appium import webdriver
from appium.options.common import AppiumOptions
from typing import Dict, Any


def pytest_configure(config):
    """Configure Allure environment properties"""
    allure_env_dir = os.path.join(os.getcwd(), 'allure-results')
    os.makedirs(allure_env_dir, exist_ok=True)

    with open(os.path.join(allure_env_dir, 'environment.properties'), 'w') as f:
        f.write(f"APPIUM_VERSION={os.getenv('APPIUM_VERSION', '2.0')}\n")
        f.write(f"ANDROID_DEVICE={os.getenv('ANDROID_DEVICE', 'emulator-5554')}\n")
        f.write(f"APPIUM_HOST={os.getenv('APPIUM_HOST', 'localhost')}\n")
        f.write(f"TEST_PRIORITY=Critical,High,Medium\n")


@pytest.fixture(scope="session")
def driver():
    """Session-level fixture for Appium driver"""
    appium_host = os.getenv('APPIUM_HOST', 'host.docker.internal')
    appium_port = os.getenv('APPIUM_PORT', '4723')
    url = f'http://{appium_host}:{appium_port}'

    capabilities: Dict[str, Any] = {
        'platformName': 'Android',
        'automationName': 'UiAutomator2',
        'deviceName': os.getenv('ANDROID_DEVICE', 'emulator-5554'),
        'appPackage': 'com.photobook.android.staging',
        'appActivity': 'com.photobook.android.page.applaunch.AppLaunchActivity',
        'uiautomator2ServerLaunchTimeout': 120000,
        'adbExecTimeout': 120000,
        'noReset': False,
        'autoGrantPermissions': True
    }

    driver = webdriver.Remote(url, options=AppiumOptions().load_capabilities(capabilities))
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def restart_app(driver):
    """Restart app before each test"""
    try:
        driver.terminate_app('com.photobook.android.staging')
        driver.activate_app('com.photobook.android.staging')
    except Exception as e:
        pytest.fail(f"Failed to restart app: {str(e)}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot on test failure"""
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        driver = item.funcargs.get('driver')
        if driver:
            try:
                screenshot = driver.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {str(e)}")