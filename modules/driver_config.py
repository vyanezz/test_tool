class DriverConfig:
    def __init__(
        self,
        headless=False,
        proxy=None,
        user_agent=None,
        window_size="1920,1080",
        ignore_cert_errors=True,
        extra_args=None
    ):
        self.headless = headless
        self.proxy = proxy
        self.user_agent = user_agent
        self.window_size = window_size
        self.ignore_cert_errors = ignore_cert_errors
        self.extra_args = extra_args or []