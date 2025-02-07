from mitmproxy import http
import sys


class Interceptor:
    def __init__(self, filter_urls=None):
        self.filter_urls = filter_urls

    def request(self, flow: http.HTTPFlow):
        url = flow.request.url

        if not self.filter_urls or any(filter_url in url for filter_url in self.filter_urls):
            print(f"📡 Interceptado: {url}")
            print(f"🔹 Método: {flow.request.method}")
            print(f"📩 Headers: {dict(flow.request.headers)}")
            print(f"📄 Cuerpo: {flow.request.content.decode(errors='ignore')}\n")

    def response(self, flow: http.HTTPFlow):
        url = flow.request.url

        if not self.filter_urls or any(filter_url in url for filter_url in self.filter_urls):
            print(f"📬 Respuesta de {url}")
            print(f"🔹 Código HTTP: {flow.response.status_code}")
            print(f"📄 Cuerpo: {flow.response.text[:500]}...\n")  # Solo los primeros 500 caracteres


addons = [Interceptor(sys.argv[1].split(",") if len(sys.argv) > 1 else [])]
