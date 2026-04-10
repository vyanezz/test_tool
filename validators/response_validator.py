class ResponseValidator:
    def __init__(self, logger=None):
        self.logger = logger

    def validate(
        self,
        flow,
        expected_status=None,
        expected_headers=None,
        json_body=None,
        form_urlencoded_body=None
    ):
        if expected_status is not None:
            self.validate_status(flow, expected_status)

        if expected_headers:
            self.validate_headers(flow, expected_headers)

        if json_body:
            self.validate_json_body(flow, json_body)

        if form_urlencoded_body:
            text_body = flow.response.text
            self._validate_form_urlencoded_body(form_urlencoded_body, text_body)

        return flow

    def validate_status(self, flow, expected_status):
        actual = flow.response.status_code
        if actual != expected_status:
            raise AssertionError(f"Expected status {expected_status}, got {actual}")

    def validate_headers(self, flow, expected_headers):
        return self._validate_headers(expected_headers, flow.response.headers)

    def validate_json_body(self, flow, expected_body):
        try:
            actual_body = flow.response.json()
        except Exception as e:
            raise AssertionError(f"Response body is not valid JSON: {e}")
        return self._validate_json_body(expected_body, actual_body)

    def _validate_json_body(self, expected_body, actual_body):
        for key, value in expected_body.items():
            actual_value = actual_body.get(key)
            if actual_value is None:
                raise AssertionError(
                    f"JSON body field not found: '{key}' (expected value: '{value}')"
                )
            if actual_value != value:
                raise AssertionError(
                    f"JSON body mismatch for '{key}': expected '{value}', got '{actual_value}'"
                )
        return True

    def _validate_headers(self, expected_headers, actual_headers):
        for key, value in expected_headers.items():
            actual_value = actual_headers.get(key)
            if actual_value is None:
                raise AssertionError(
                    f"Header not found: '{key}' (expected value: '{value}')"
                )
            if actual_value != value:
                raise AssertionError(
                    f"Header mismatch for '{key}': expected '{value}', got '{actual_value}'"
                )
        return True

    def _validate_form_urlencoded_body(self, expected, actual_text):
        from urllib.parse import parse_qs

        actual_dict = parse_qs(actual_text)
        actual_dict = {k: v[0] if len(v) == 1 else v for k, v in actual_dict.items()}

        for key, value in expected.items():
            if key not in actual_dict:
                raise AssertionError(
                    f"Form field not found: '{key}' (expected value: '{value}')"
                )
            if actual_dict[key] != value:
                raise AssertionError(
                    f"Form field mismatch for '{key}': expected '{value}', got '{actual_dict[key]}'"
                )