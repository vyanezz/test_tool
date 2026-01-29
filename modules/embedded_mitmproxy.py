import asyncio
import threading
from mitmproxy import options
from mitmproxy.tools.dump import DumpMaster
from interceptors.interceptor import Interceptor
import time
from utils import logger

class EmbeddedMitmProxy:
    def __init__(self, port=8080):
        self.port = port
        self.mitm = None
        self.interceptor = None
        self.thread = None

    def _run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._async_run())

    async def _async_run(self):
        opts = options.Options(listen_host="127.0.0.1", listen_port=self.port)
        self.mitm = DumpMaster(opts, with_termlog=False, with_dumper=False)
        self.interceptor = Interceptor()
        self.mitm.addons.add(self.interceptor)

        try:
            await self.mitm.run()
        except KeyboardInterrupt:
            self.mitm.shutdown()

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def stop(self):
        if self.mitm:
            self.mitm.shutdown()
        if self.thread:
            self.thread.join()

    def validate_api_call(self, endpoint, method=None, timeout=5):
        if not self.interceptor:
            return False

        start = time.time()

        while time.time() - start < timeout:
            for flow in self.interceptor.flows:
                if endpoint in flow.request.url:
                    if method is None or flow.request.method.upper() == method.upper():
                        logger.log_api_call(endpoint,method)
                        return True
            time.sleep(0.1)

        return False