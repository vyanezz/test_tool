import time

class ApiValidator:
    def __init__(self, interceptor, logger=None, default_timeout=5):
        self.interceptor = interceptor
        self.logger = logger
        self.default_timeout = default_timeout

    def wait_for_request(self, endpoint, method=None, headers=None, json_body=None, form_urlencoded_body=None, timeout=None):
        if not self.interceptor:
            raise RuntimeError("Interceptor not initialized")

        timeout = timeout or self.default_timeout
        start = time.time()

        endpoint_found = False
        method_found = False

        while time.time() - start < timeout:
            for flow in self.interceptor.flows:

                if endpoint not in flow.request.url:
                    continue
                endpoint_found = True

                if method and flow.request.method.upper() != method.upper():
                    continue
                method_found = True

                if headers:
                    self._validate_headers(headers, flow.request.headers)

                if json_body:
                    try:
                        flow_json = flow.request.json()
                    except Exception as e:
                        raise AssertionError(f"Request found for endpoint '{endpoint}' but body is not valid JSON: {e}")
                    self._validate_json_body(json_body, flow_json)

                if form_urlencoded_body:
                    self._validate_form_urlencoded_body(form_urlencoded_body, flow.request.text)

                if self.logger:
                    self.logger.log_api_call(endpoint, method)

                return flow

            time.sleep(0.1)

        if not endpoint_found:
            raise TimeoutError(f"No request detected for endpoint '{endpoint}' within {timeout}s")

        if method and not method_found:
            raise AssertionError(
                f"Request to endpoint '{endpoint}' detected but HTTP method did not match. "
                f"Expected: {method}"
            )

        raise TimeoutError(
            f"Request detected for endpoint '{endpoint}' but headers did not match expected values: {headers}"
        )

    def _validate_json_body(self, expected_body, actual_body):
        for key, value in expected_body.items():
            actual_value = actual_body.get(key)
            if actual_value is None:
                raise AssertionError(f"JSON body field not found: '{key}' (expected value: '{value}')")
            if actual_value != value:
                raise AssertionError(f"JSON body mismatch for '{key}': expected '{value}', got '{actual_value}'")
        return True

    def _validate_form_urlencoded_body(self, expected, actual_text):
        from urllib.parse import parse_qs
        import difflib

        actual_dict = parse_qs(actual_text)
        actual_dict = {k: v[0] if len(v) == 1 else v for k, v in actual_dict.items()}

        for key, value in expected.items():
            if key not in actual_dict:
                close_matches = difflib.get_close_matches(key, actual_dict.keys(), n=1, cutoff=0.6)
                suggestion = f" Did you mean '{close_matches[0]}'?" if close_matches else ""
                raise AssertionError(f"Form field not found: '{key}' (expected value: '{value}').{suggestion}")
            if actual_dict[key] != value:
                raise AssertionError(f"Form field mismatch for '{key}': expected '{value}', got '{actual_dict[key]}'")

    def _validate_headers(self, expected_headers, actual_headers):
        """
        Checks expected headers exist and match actual headers.
        Raises AssertionError if a header is missing or mismatched.
        """
        for key, value in expected_headers.items():
            actual_value = actual_headers.get(key)
            if actual_value is None:
                raise AssertionError(f"Header not found: '{key}' (expected value: '{value}')")
            if actual_value != value:
                raise AssertionError(
                    f"Header mismatch for '{key}': expected '{value}', got '{actual_value}'"
                )
        return True