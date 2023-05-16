from flask import Flask, request
from export import main

import argparse

app = Flask(__name__)

@app.route('/export', methods=['POST'])
def export():
    # 获取请求参数
    args = request.form.to_dict()
    
    print(args)
    
    # 解析参数
    root0 = request.form.get('root0', default='E:/Code/python/ocr/pics/example6.jpg')
    root1 = request.form.get('root1', default='E:/Code/python/ocr/pics/example6.jpg')
    output = request.form.get('output', default='./pics/output.jpg')
    thresh_line = int(request.form.get('thresh_line', default='10'))
    thresh_box = int(request.form.get('thresh_box', default='160'))
    extra_size = int(request.form.get('extra_size', default='20'))
    font_size = int(request.form.get('font_size', default='35'))
    uid = request.form.get('uid', default='20220630001260579')
    bkey = request.form.get('bkey', default='15Yr0dRYfINuQF0w6ptK')
    gpu = request.form.get('gpu', default='True').lower() == 'true'
    resize = request.form.get('resize', default='True').lower() == 'true'
    dewarp = request.form.get('dewarp', default='False').lower() == 'true'
    args = argparse.Namespace(
        root0=root0,
        root1=root1,
        output=output,
        thresh_line=thresh_line,
        thresh_box=thresh_box,
        extra_size=extra_size,
        font_size=font_size,
        uid=uid,
        bkey=bkey,
        gpu=gpu,
        resize=resize,
        dewarp=dewarp
    )
    print(args)
    main(args=args)
    # 返回处理结果给客户端
    return 'Export completed'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=25000)