import time

class ApiValidator:
    def __init__(self, interceptor, logger=None, default_timeout=5):
        self.interceptor = interceptor
        self.logger = logger
        self.default_timeout = default_timeout


    def wait_for_call(self, endpoint, method=None, timeout=None):
        if not self.interceptor:
            raise RuntimeError("Interceptor not initialized")

        timeout = timeout or self.default_timeout
        start = time.time()

        while time.time() - start < timeout:
            for flow in self.interceptor.flows:
                if endpoint in flow.request.url:
                    if method is None or flow.request.method.upper() == method.upper():
                        if self.logger:
                            self.logger.log_api_call(endpoint, method)
                        return True
            time.sleep(0.1)

        return False