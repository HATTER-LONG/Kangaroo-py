import requests


if __name__ == "__main__":
    url = "https://www.baidu.com"
    response = requests.get(url)
    print(response.text)
