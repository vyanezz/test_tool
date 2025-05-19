from multiprocessing import Process
import subprocess


class TrafficMonitor:
    def __init__(self, port=8080, filter_urls=None):
        self.process = None
        self.port = port
        self.thread = None
        self.traffic_urls = None

    def set_urls(self, traffic_urls=None):
        if not traffic_urls:
            self.traffic_urls = []
        else:
            self.traffic_urls = [traffic_urls] if isinstance(traffic_urls, str) else traffic_urls


    def start(self):
        self.process = Process(target=self._start_mitmproxy)
        self.process.start()

    def _start_mitmproxy(self):
        args = [
            "mitmdump",
            "-p", str(self.port),
            "-s", "interceptors/interceptor.py",
            "-q",  # <-- aquí el flag quiet para bajar logs de mitmdump
            "--set", f"filter_urls={','.join(self.traffic_urls)}"
        ]
        subprocess.Popen(args)

    def stop(self):
        if self.thread:
            self.thread.join()
