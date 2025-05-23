from mitmproxy import http

class Interceptor:
    def __init__(self):
        self.flows = []

    def request(self, flow: http.HTTPFlow):
        self.flows.append(flow)
