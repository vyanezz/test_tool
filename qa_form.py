from test_automation import TestAutomation

def test_qa_form():
        if __name__ == '__main__':
                test = TestAutomation()
                driver, traffic = test.start_test()

                driver.navigate("https://ultimateqa.com/filling-out-forms/")

                assert traffic.validate_api_call("https://ultimateqa.com/filling-out-forms/", "GET")

                driver.send_keys("id", "et_pb_contact_name_0", "Test User")
                driver.send_keys("id", "et_pb_contact_message_0", "Pytest message")
                driver.click("name", "et_builder_submit_button")

                assert traffic.validate_api_call("https://ultimateqa.com/filling-out-forms/", "POST")

                driver.quit()
                traffic.stop()
test_qa_form()