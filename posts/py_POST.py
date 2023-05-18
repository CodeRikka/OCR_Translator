import requests

url = 'http://cn-yw-plc-2.openfrp.top:25000/export'  # 替换为服务器的实际IP地址和端口以及路径

data = {
    'root0': './pics/example2.jpg',  # 根据实际参数进行替换
    'root1': './pics/example2.jpg',
    'output': './pics/output.jpg',
    'thresh_line': '10',
    'thresh_box': '160',
    'extra_size': '20',
    'font_size': '35',
    'uid': '20220630001260579',
    'bkey': '15Yr0dRYfINuQF0w6ptK',
    'gpu': 'True',
    'resize': 'True',
    'dewarp': 'False'
}

response = requests.post(url, data=data)

print(response.status_code)  # 打印响应状态码
print(response.text)  # 打印响应内容
