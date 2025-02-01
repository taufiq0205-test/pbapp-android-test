import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import time
from selenium.webdriver.support.wait import WebDriverWait
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

class GoogleProject:
    def test_TCA2004_GOOGLE_PROJECT(self, driver):

        with allure.step("Navigate to Account page"):
            account = wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Account"))
            account.click()

            time.sleep(3)

            navigate_login = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR,"new UiSelector().className(\"android.widget.Button\").instance(0)"))
            navigate_login.click()

            time.sleep(3)

        with allure.step("Login using Google account"):
            continue_with_google = wait_for_element(driver, (AppiumBy.ID,
                                                       "com.photobook.android.staging:id/googleButton"))
            continue_with_google.click()

            select_gmail_account = wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().className(\"android.widget.LinearLayout\").instance(3)"))
            select_gmail_account.click()

            time.sleep(20)
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(764, 1596)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            time.sleep(7)
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(758, 2100)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            print("Successfully logged in!")
            time.sleep(3)

        with allure.step("Navigate to Home"):
            home = wait_for_element(driver, (AppiumBy.ACCESSIBILITY_ID, "Home"))
            home.click()

        with allure.step("Navigate to Simplebook"):
            view_more = wait_for_element(driver,
                                         (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"View More\").instance(0)"))
            view_more.click()

        with allure.step("Select Simplebook"):
            print("Buying Simplebook...")
            wait_for_element(driver, (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Simple Books\")"))
            simple_book = wait_for_element(driver,
                                           (AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Simple Books\")"))
            simple_book.click()

            next_button = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/action_product_next"))
            next_button.click()

            print("Adding pictures...")
            wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/albumConstraintLayout"))
            open_gallery = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/albumConstraintLayout"))
            open_gallery.click()

            select_all_pictures = wait_for_element(driver, (
            AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().className(\"android.widget.FrameLayout\").instance(22)"))
            select_all_pictures.click()

            continue_button = wait_for_element(driver, (
            AppiumBy.ID, "com.photobook.android.staging:id/continueWithPhotoCountButton"))
            continue_button.click()

            always_use_this_feature = wait_for_element(driver, (
            AppiumBy.ID, "com.photobook.android.staging:id/verticalDialogOkayButton"))
            always_use_this_feature.click()

        with allure.step("Add Simplebook to Cart"):
            add_to_cart_button_small = wait_for_element(driver, (
            AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Add to cart\")"))
            add_to_cart_button_small.click()

            # Perform touch actions with waiting period
            time.sleep(2)
            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(1003, 1448)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(0.1)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            no_thanks_button = wait_for_element(driver,
                                                (AppiumBy.ID, "com.photobook.android.staging:id/upsellDialogCancelButton"))
            no_thanks_button.click()

            all_good_button = wait_for_element(driver,
                                               (AppiumBy.ID, "com.photobook.android.staging:id/verticalDialogCancelButton"))
            all_good_button.click()

        with allure.step("Proceed to Checkout"):
            print("Add project to cart...")
            add_to_cart_button = wait_for_element(driver, (
            AppiumBy.ID, "com.photobook.android.staging:id/removePageLayoutBookEditor"))
            add_to_cart_button.click()

            print("Begin checkout process...")
            checkout = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/checkoutButton"))
            checkout.click()

            select_payment_method_button = wait_for_element(driver, (
                AppiumBy.ID, "com.photobook.android.staging:id/selectPaymentMethodButton"))
            select_payment_method_button.click()

            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(502, 2033)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(534, 326)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            choose_payment_method = wait_for_element(driver, (
            AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"Offline Payment\")"))
            choose_payment_method.click()

            select_payment_button = wait_for_element(driver,
                                                     (AppiumBy.ID, "com.photobook.android.staging:id/selectPaymentButton"))
            select_payment_button.click()

            actions = ActionChains(driver)
            actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(515, 1735)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.move_to_location(518, 473)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

            order_now_button = wait_for_element(driver, (AppiumBy.ID, "com.photobook.android.staging:id/orderNowButton"))
            order_now_button.click()

        with allure.step("Order Complete and View Order"):
            print("Order completed!")
            view_my_order = wait_for_element(driver, (
            AppiumBy.ANDROID_UIAUTOMATOR, "new UiSelector().resourceId(\"view_my_orders\")"))
            view_my_order.click()

        with allure.step("Navigate to Account Page"):
            print("Navigate to Account page...")
            back_button = wait_for_element(driver, (AppiumBy.CLASS_NAME, "android.widget.Button"))
            back_button.click()

