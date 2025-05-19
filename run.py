from test import TestAutomation

url_test = 'https://ultimateqa.com/filling-out-forms/'

test = TestAutomation()
if __name__ == "__main__":
    test.start_test(url=url_test, traffic_urls=url_test)
