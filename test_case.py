import requests

def test_case():
    url = "http://127.0.0.1:8000/iot/testcase"
    resp = requests.get(url)
    print(resp.status_code)
    print(resp.json())

def send_data():
    url = "http://127.0.0.1:8000/iot/35/80"
    resp = requests.get(url)
    print(resp.status_code)
    #print(resp.json())
test_case()
send_data()