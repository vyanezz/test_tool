from multiprocessing import Process
import subprocess
import sys
import os
import signal

class TrafficMonitor:
    def __init__(self, port=8080):  # Cambia el puerto si 8080 está ocupado
        self.process = None
        self.port = port
        self.traffic_urls = []

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
            "-q",
            "-s", "interceptors/interceptor.py",
            "--set", f"filter_urls={','.join(self.traffic_urls)}"
        ]
        subprocess.call(args)

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.join()
            try:
                    if sys.platform == "win32":
                        tasks = subprocess.check_output("tasklist", shell=True).decode('cp1252')
                        for line in tasks.splitlines():
                            if "mitmdump.exe" in line or "mitmproxy.exe" in line:
                                pid = int(line.split()[1])
                                subprocess.call(f"taskkill /PID {pid} /F", shell=True)
                                print(f"🛑 Proceso mitmproxy/mitmdump terminado. PID: {pid}")
                    else:
                        # Linux / macOS
                        result = subprocess.check_output(["pgrep", "-f", "mitmdump"]).decode().split()
                        for pid in result:
                            os.kill(int(pid), signal.SIGTERM)
                            print(f"🛑 Proceso mitmdump terminado. PID: {pid}")
            except Exception as e:
                    print(f"⚠️ No se pudo terminar mitmdump: {e}")

