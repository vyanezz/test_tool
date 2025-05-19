from mitmproxy import http, ctx

class Interceptor:
    def __init__(self):
        self.filter_urls = []

    def configure(self, updated):
        filter_option = ctx.options.filter_urls
        if filter_option:
            self.filter_urls = [url.strip() for url in filter_option.split(",") if url.strip()]
        else:
            self.filter_urls = []



    def _url_matches(self, url):
        if not self.filter_urls:
            return False  # No filtros = no match
        return any(f in url for f in self.filter_urls)

    def request(self, flow: http.HTTPFlow):
        url = flow.request.url
        if self._url_matches(url):
            print("\n" + "=" * 40)
            print(f"📡 Interceptado: {url}")
            print(f"🔹 Método: {flow.request.method}")
            print(f"📩 Headers: {dict(flow.request.headers)}")
            #print(f"📄 Cuerpo: {flow.request.content.decode(errors='ignore')}\n")

    def response(self, flow: http.HTTPFlow):
        url = flow.request.url
        if self._url_matches(url):
            print(f"📬 Respuesta de {url}")
            print(f"🔹 Código HTTP: {flow.response.status_code}")
            #print(f"📄 Cuerpo: {flow.response.content.decode(errors='ignore')}\n")

def load(loader):
    loader.add_option(
        name="filter_urls",
        typespec=str,
        default="",
        help="Comma-separated list of URLs to intercept (e.g., https://example.com/api,https://foo.com/bar)"
    )

addons = [Interceptor()]
