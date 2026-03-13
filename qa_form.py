from test_automation import TestAutomation

def test_qa_form():
        if __name__ == '__main__':
                test = TestAutomation(enable_logger=True)

                test.navigate("https://ultimateqa.com/filling-out-forms/")

                test.wait_for_request("https://ultimateqa.com/filling-out-forms/", "GET")

                test.send_keys("id", "et_pb_contact_name_0", "Test User")
                test.send_keys("id", "et_pb_contact_message_0", "Test message")
                test.click("name", "et_builder_submit_button")

                test.wait_for_request(endpoint="https://ultimateqa.com/filling-out-forms/",
                                          method="POST",
                                          timeout=10,
                                          headers={"accept-language": "es-ES,es;q=0.9", "cache-control":"max-age=0"},
                                          form_urlencoded_body={
                                              "et_pb_contact_name_0": "Test Users",
                                              "et_pb_contact_message_0": "Test message",
                                              "et_pb_contactform_submit_0": "et_contact_proccess",
                                              "_wpnonce-et-pb-contact-form-submitted-0": "bf019df153",
                                              "_wp_http_referer": "/filling-out-forms/"
                                          }
                                      )

                test.stop_test()
test_qa_form()