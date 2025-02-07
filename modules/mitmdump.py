import threading
from mitmproxy.tools.main import mitmdump


class TrafficMonitor:
    def __init__(self, port=8080, filter_urls=None):
        self.port = port
        self.thread = None
        self.traffic_urls = None

    def set_urls(self, traffic_urls=None):
        if not traffic_urls:
            self.traffic_urls = []
        else:
            self.traffic_urls = [traffic_urls] if isinstance(traffic_urls, str) else traffic_urls

    def start(self):
        self.thread = threading.Thread(target=self._start_mitmproxy)
        self.thread.start()

    def _start_mitmproxy(self):
        """Executed in thread"""
        mitmdump(["-p", str(self.port), "-s", "interceptor.py"] + self.traffic_urls)

    def stop(self):
        if self.thread:
            self.thread.join()
