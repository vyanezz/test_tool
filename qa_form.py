from test_automation import TestAutomation

def test_qa_form():
        if __name__ == '__main__':
                test = TestAutomation(enable_logger=False)

                test.navigate("https://ultimateqa.com/filling-out-forms/")

                assert test.wait_for_call("https://ultimateqa.com/filling-out-forms/", "GET")

                test.send_keys("id", "et_pb_contact_name_0", "Test User")
                test.send_keys("id", "et_pb_contact_message_0", "Pytest message")
                test.click("name", "et_builder_submit_button")

                assert test.wait_for_call("https://ultimateqa.com/filling-out-forms/", "POST", 10)

                test.stop_test()
test_qa_form()