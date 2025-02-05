from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class WebDriver:
    def __init__(self, proxy=None):
        options = webdriver.ChromeOptions()

        if proxy:
            options.add_argument(f"--proxy-server={proxy}")

        self.driver = webdriver.Chrome(options=options)

    def navigate(self, url):
        self.driver.get(url)

    def wait_for_element(self, by, value, timeout=20):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
        except Exception as e:
            print(f"Error esperando el elemento: {e}")
            return None

    def find_element(self, by, value):
        print(by, value)  # Esto te ayudará a verificar los valores
        return self.driver.find_element(by, value)

    def click(self, by, value):
        element = self.wait_for_element(by, value)
        if element:
            element.click()

    def send_keys(self, by, value, keys):
        element = self.wait_for_element(by, value)
        if element:
            element.send_keys(keys)

    def take_screenshot(self, filename):
        self.driver.save_screenshot(filename)

    def quit(self):
        self.driver.quit()
