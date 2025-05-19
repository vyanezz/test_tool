import time
from modules.mitmdump import TrafficMonitor
from modules.webdriver import WebDriver


class TestAutomation:
    def __init__(self):
        self.driver = None
        self.traffic = TrafficMonitor()


    def start_test(self, traffic_urls):
        self.traffic.set_urls(traffic_urls)
        self.traffic.start()
        self.driver = WebDriver()
        time.sleep(3)

        return self.driver, self.traffic
