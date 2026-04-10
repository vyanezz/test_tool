from test_automation import TestAutomation

def qa_form():
        if __name__ == '__main__':
                test = TestAutomation(enable_logger=True, headless=True)

                test.navigate("https://httpbin.org/forms/post")

                test.wait_for_request("https://httpbin.org/forms/post", "GET")

                test.send_keys("name", "custname", "Jhon")
                test.send_keys("name", "custtel", "600123456")
                test.send_keys("NAME", "custemail", "Jhon@test.com")

                test.click("XPATH", "//input[@name='size' and @value='medium']")
                test.click("XPATH", "//input[@value='bacon']")
                test.click("XPATH", "//input[@value='cheese']")
                test.click("XPATH", "//input[@value='mushroom']")

                test.send_keys("NAME", "delivery", "11:00")

                test.click("XPATH", "//button[contains(text(),'Submit')]")

                flow = test.wait_for_request(endpoint="https://httpbin.org/post",
                                          method="POST",
                                          timeout=10,
                                          headers={"accept-language": "es-ES,es;q=0.9"},
                                          form_urlencoded_body={
                                              "custname": "Jhon",
                                              "custtel": "600123456",
                                              "custemail": "Jhon@test.com",
                                              "size": "medium",
                                              "topping": ["bacon","cheese","mushroom"],
                                              "delivery": "11:00",
                                          }
                                      )

                test.wait_for_response(
                    flow,
                    expected_status=200,
                    expected_headers={"Content-Type": "application/json"},
                    json_body={"form": { "comments": "",  "custemail": "Jhon@test.com", "custname": "Jhon", "custtel": "600123456", "delivery": "11:00", "size": "medium", "topping": ["bacon", "cheese", "mushroom"]}},
                )

                test.stop_test()
qa_form()