import requests

def submit_request(question):
    url = "http://localhost:25005/spell"  # 应用程序的 URL
    data = {"question": question}  # 请求的数据

    response = requests.post(url, data=data)  # 发送 POST 请求

    if response.status_code == 200:
        result = response.json()  # 获取返回的 JSON 数据
        return result
    else:
        print("Request failed with status code:", response.status_code)
        return None


if __name__ == "__main__":
    # 调用示例
    question = "fact is that im not a humman"
    result = submit_request(question)
    if result is not None:
        print("Result:", result)
