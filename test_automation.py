from modules.embedded_mitmproxy import EmbeddedMitmProxy
from modules.webdriver import WebDriver


class TestAutomation:
    def __init__(self):
        self.driver = None
        self.traffic = EmbeddedMitmProxy()

    def start_test(self):
        self.traffic.start()
        self.driver = WebDriver()
        return self

    def stop_test(self):
        if self.driver:
            self.driver.quit()
        if self.traffic:
            self.traffic.stop()

    def __getattr__(self, name):
        if hasattr(self.traffic, name):
            return getattr(self.traffic, name)
        elif hasattr(self.driver, name):
            return getattr(self.driver, name)
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")