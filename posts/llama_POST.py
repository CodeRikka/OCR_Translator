import requests

def submit_request_spell_sent(question):
    url = "http://localhost:25005/spell_sent"  # 应用程序的 URL
    data = {"question": question}  # 请求的数据

    response = requests.post(url, data=data)  # 发送 POST 请求

    if response.status_code == 200:
        result = response.json()  # 获取返回的 JSON 数据
        return result
    else:
        print("Request failed with status code:", response.status_code)
        return None

def submit_request_spell_paragraph(question):
    url = "http://localhost:25005/spell_paragraph"  # 应用程序的 URL
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
    result = submit_request_spell_sent(question)
    if result is not None:
        print("Result:", result)
