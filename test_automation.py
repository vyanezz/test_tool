from modules.embedded_mitmproxy import EmbeddedMitmProxy
from modules.webdriver import WebDriver


class TestAutomation:
    def __init__(self):
        self.driver = None
        self.traffic = EmbeddedMitmProxy()

    def start_test(self):
        self.traffic.start()
        self.driver = WebDriver()

        return self.driver, self.traffic
