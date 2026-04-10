from validators.request_validator import RequestValidator
from validators.response_validator import ResponseValidator

class ApiValidator:
    def __init__(self, interceptor, logger=None, default_timeout=5):
        self.request = RequestValidator(interceptor, logger, default_timeout)
        self.response = ResponseValidator(logger)

    def wait_for_request(self, *args, **kwargs):
        return self.request.wait_for_request(*args, **kwargs)

    def wait_for_response(self, flow, *args, **kwargs):
        return self.response.validate(flow, *args, **kwargs)