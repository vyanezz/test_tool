import time
from test import TestAutomation


def test_qa_form():
        if __name__ == '__main__':
                test = TestAutomation()
                driver, traffic = test.start_test(traffic_urls="https://ultimateqa.com/filling-out-forms/")


                driver.navigate("https://ultimateqa.com/filling-out-forms/")
                driver.send_keys("id", "et_pb_contact_name_0", "Test User")
                driver.send_keys("id", "et_pb_contact_message_0", "Pytest message")
                driver.click("name", "et_builder_submit_button")

                time.sleep(2)

                driver.quit()
                traffic.stop()
test_qa_form()