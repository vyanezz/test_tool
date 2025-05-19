import time
from modules.mitmdump import TrafficMonitor
from modules.webdriver import WebDriver


class TestAutomation:
    def __init__(self):
        self.driver = None
        self.traffic = TrafficMonitor()


    def start_test(self, url, traffic_urls):
        self.traffic.set_urls(traffic_urls)
        self.traffic.start()
        time.sleep(3)


        self.driver = WebDriver()
        self.driver.navigate(url)
        self.driver.send_keys("id", 'et_pb_contact_name_0', 'test_automation_tool')
        self.driver.send_keys("id", 'et_pb_contact_message_0', 'Testing test_automation_tool')
        self.driver.click("name", 'et_builder_submit_button')

        time.sleep(3)

        self.driver.quit()
        self.traffic.stop()
