import time
import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def wait_for_element(driver, locator, timeout=60):
    """Wait for an element to be present and visible"""
    wait = WebDriverWait(driver, timeout)
    try:
        element = wait.until(EC.presence_of_element_located(locator))
        wait.until(EC.visibility_of(element))
        return element
    except TimeoutException:
        print(f"Timeout waiting for element: {locator}")
        return None

class AddAddress:
    def test_TCA3002_ADD_ADDRESS(self, driver):

        with allure.step("Navigate to Address Book"):
            address_book = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Address Book\")"))
            address_book.click()

        with allure.step("Add New Address"):
            add_address = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/addAddressButton"))
            add_address.click()

        with allure.step("Fill New Address Details"):
            # Address form
            first_name = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/firstNameEditText"))
            first_name.send_keys("Autobots")

            last_name = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/lastNameEditText"))
            last_name.send_keys("Add Address")

            address_line = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/street1EditText"))
            address_line.send_keys("Testing Road 123")

            time.sleep(3)
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(532, 2273)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(537, 246)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            select_state = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/stateTextView"))
            select_state.click()

            state_name = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Melaka\")"))
            state_name.click()

            city_name = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/cityEditText"))
            city_name.send_keys("Alor Gajah")

            postcode = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/postcodeEditText"))
            postcode.send_keys("70000")

            phone_number = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/phoneNumberEditText"))
            phone_number.send_keys("0123456789")

        with allure.step("Save New Address"):
            save_button = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/saveButton"))
            save_button.click()

        with allure.step("Navigate to Account Page"):
            time.sleep(2)
            back_to_account = wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Navigate up"))
            back_to_account.click()
