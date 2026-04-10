from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from modules.driver_config import DriverConfig


class WebDriver:

    LOCATORS = {
        "id": By.ID,
        "name": By.NAME,
        "xpath": By.XPATH,
        "css": By.CSS_SELECTOR
    }

    def __init__(self, logger=None, config=None):
        config = config or DriverConfig()
        options = webdriver.ChromeOptions()

        if config.headless:
            options.add_argument("--headless=new")

        if config.proxy:
            options.add_argument(f"--proxy-server={config.proxy}")

        if config.ignore_cert_errors:
            options.add_argument("--ignore-certificate-errors")

        if config.user_agent:
            options.add_argument(f"user-agent={config.user_agent}")

        if config.window_size:
            options.add_argument(f"--window-size={config.window_size}")

        for arg in config.extra_args:
            options.add_argument(arg)

        self.driver = webdriver.Chrome(options=options)
        self.logger = logger

    # ---------------- NAVIGATION ----------------

    def navigate(self, url):
        self.driver.get(url)
        if self.logger:
            self.logger.log_action(url, action_type="NAVIGATE")

    def get_current_url(self):
        url = self.driver.current_url
        if self.logger:
            self.logger.log_action(f"Get URL -> {url}", action_type="NAVIGATE")
        return url

    def go_back(self):
        self.driver.back()
        if self.logger:
            self.logger.log_action("Go back", action_type="NAVIGATE")

    def refresh(self):
        self.driver.refresh()
        if self.logger:
            self.logger.log_action("Refresh page", action_type="NAVIGATE")

    # ---------------- ELEMENTS ----------------

    def _get_by(self, by):
        return self.LOCATORS.get(by.lower(), by)

    def wait_for_element(self, by, value, timeout=20):
        by = self._get_by(by)
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except Exception as e:
            if self.logger:
                self.logger.log_action(
                    f"Wait failed: {value} - {e}",
                    action_type="WAIT",
                    status="ERROR"
                )
            return None

    def find_element(self, by, value):
        try:
            el = self.driver.find_element(self._get_by(by), value)
            if self.logger:
                self.logger.log_action(f"Find element: {value}", action_type="FIND")
            return el
        except Exception as e:
            if self.logger:
                self.logger.log_action(
                    f"Find element failed: {value} - {e}",
                    action_type="ERROR"
                )
            raise

    def find_elements(self, by, value):
        els = self.driver.find_elements(self._get_by(by), value)
        if self.logger:
            self.logger.log_action(
                f"Find elements: {value} ({len(els)})",
                action_type="FIND"
            )
        return els

    def is_visible(self, by, value, timeout=10):
        return self.wait_for_element(by, value, timeout) is not None

    def is_present(self, by, value):
        return len(self.find_elements(by, value)) > 0

    # ---------------- ACTIONS ----------------

    def click(self, by, value):
        el = self.wait_for_element(by, value)
        if el:
            el.click()
            if self.logger:
                self.logger.log_action(f"Click: {value}", action_type="CLICK")

    def send_keys(self, by, value, keys, clear_first=True):
        el = self.wait_for_element(by, value)
        if el:
            if clear_first:
                el.clear()
            el.send_keys(keys)
            if self.logger:
                self.logger.log_action(
                    f"Type '{keys}' -> {value}",
                    action_type="SEND_KEYS"
                )

    def clear(self, by, value):
        el = self.wait_for_element(by, value)
        if el:
            el.clear()
            if self.logger:
                self.logger.log_action(f"Clear: {value}", action_type="CLEAR")

    def get_text(self, by, value):
        el = self.wait_for_element(by, value)
        text = el.text if el else None

        if self.logger:
            self.logger.log_action(
                f"Get text: {value} -> {text}",
                action_type="GET_TEXT"
            )

        return text

    def get_value(self, by, value):
        el = self.wait_for_element(by, value)
        val = el.get_attribute("value") if el else None

        if self.logger:
            self.logger.log_action(
                f"Get value: {value} -> {val}",
                action_type="GET_VALUE"
            )

        return val

    # ---------------- ADVANCED ACTIONS ----------------

    def hover(self, by, value):
        el = self.wait_for_element(by, value)
        if el:
            ActionChains(self.driver).move_to_element(el).perform()
            if self.logger:
                self.logger.log_action(f"Hover: {value}", action_type="HOVER")

    def select_dropdown(self, by, value, option_text):
        el = self.wait_for_element(by, value)
        if el:
            Select(el).select_by_visible_text(option_text)
            if self.logger:
                self.logger.log_action(
                    f"Select: {value} -> {option_text}",
                    action_type="SELECT"
                )

    def scroll_to(self, by, value):
        el = self.wait_for_element(by, value)
        if el:
            self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
            if self.logger:
                self.logger.log_action(f"Scroll to: {value}", action_type="SCROLL")

    def execute_js(self, script):
        result = self.driver.execute_script(script)

        if self.logger:
            self.logger.log_action(
                f"JS: {script[:50]}...",
                action_type="JS"
            )

        return result

    # ---------------- ASSERTIONS ----------------

    def assert_text(self, by, value, expected):
        actual = self.get_text(by, value)

        if actual != expected:
            if self.logger:
                self.logger.log_action(
                    f"ASSERT FAIL text: {value}",
                    action_type="ASSERT",
                    status="ERROR"
                )
            raise AssertionError(
                f"Text mismatch: expected '{expected}', got '{actual}'"
            )

    def assert_element_visible(self, by, value):
        if not self.is_visible(by, value):
            if self.logger:
                self.logger.log_action(
                    f"ASSERT FAIL visible: {value}",
                    action_type="ASSERT",
                    status="ERROR"
                )
            raise AssertionError(f"Element not visible: {value}")

    def assert_url(self, expected):
        actual = self.get_current_url()

        if actual != expected:
            if self.logger:
                self.logger.log_action(
                    f"ASSERT FAIL URL expected '{expected}' got '{actual}'",
                    action_type="ASSERT",
                    status="ERROR"
                )
            raise AssertionError(
                f"URL mismatch: expected '{expected}', got '{actual}'"
            )

    # ---------------- WINDOW / FRAME ----------------

    def switch_to_frame(self, frame):
        self.driver.switch_to.frame(frame)
        if self.logger:
            self.logger.log_action("Switch frame", action_type="WINDOW")

    def switch_to_default(self):
        self.driver.switch_to.default_content()
        if self.logger:
            self.logger.log_action("Switch default content", action_type="WINDOW")

    def switch_to_window(self, index):
        self.driver.switch_to.window(self.driver.window_handles[index])
        if self.logger:
            self.logger.log_action(f"Switch window {index}", action_type="WINDOW")

    # ---------------- UTIL ----------------

    def take_screenshot(self, filename):
        self.driver.save_screenshot(filename)
        if self.logger:
            self.logger.log_action(
                f"Screenshot: {filename}",
                action_type="SCREENSHOT"
            )

    def quit(self):
        self.driver.quit()
        if self.logger:
            self.logger.log_action("Driver quit", action_type="QUIT")