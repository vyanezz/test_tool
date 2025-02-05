import time

from modules.webdriver import WebDriver


class TestAutomation:
    def __init__(self):
        self.driver = WebDriver()

    def start_test(self, url):
        self.driver.navigate(url)

        self.driver.send_keys("id", 'et_pb_contact_name_0', 'test_automation tool')
        self.driver.send_keys("id", 'et_pb_contact_message_0', 'Testing test_automation tool')
        self.driver.click("name", 'et_builder_submit_button')

        time.sleep(5)

        self.driver.quit()


