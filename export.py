import easyocr
import cv2
import numpy as np
from baidu_translate import baiduTranslate
from PIL import Image, ImageDraw, ImageFont
from OCRParser import makeparse
    
class OCR(object):
    def __init__(self, args):
        self.args = args
        if self.args.dewarp:
            from dewarp import process
            self.args.root1 = self.args.root0 = process(self.args.root0)
        self.img = cv2.imread(self.args.root0)
        self.draw_img = cv2.imread(self.args.root1)
        if self.args.resize:
            self.scale = 2160 / self.img.shape[1]
        self.baidu_translate = baiduTranslate(args.uid, args.bkey)
        self.reader = easyocr.Reader(['en'], gpu=args.gpu)
        self.answer, self.fa = [], []
        self.center, self.range, self.root = [], [], []
        self.text_line = [] # also the final text
    
    def resize_img(self, img, scale_persent):
        original_height, original_width = img.shape[:2]
        # scale_persent = 2160 / original_width
        new_height = int(original_height * scale_persent)
        new_width = int(original_width * scale_persent)
        new_dim = (new_width, new_height)
        enlarged_image = cv2.resize(img, new_dim, interpolation=cv2.INTER_LINEAR)
        return enlarged_image
    
    def get_text(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        pre_result = self.reader.readtext(gray)
        
        pre_centers = []
        for box in pre_result:
            x1, y1 = box[0][0][0], box[0][0][1]
            x2, y2 = box[0][2][0], box[0][2][1]
            center = ((x1 + x2) / 2, (y1 + y2) / 2)
            pre_centers.append(center)

        # 对文本框按照中心点的位置进行排序
        # sorted_indices = np.argsort([c[0] for c in centers])
        sorted_indices = np.lexsort((np.array([c[0] for c in pre_centers]), np.array([c[1] for c in pre_centers])))
        print(sorted_indices)
        sorted_boxes = [pre_result[i] for i in sorted_indices]
        
        line, texts = [], []
        lstx, lsty = 0, 0
        for i, box in enumerate(sorted_boxes):
            x1, y1 = box[0][0][0], box[0][0][1]
            x2, y2 = box[0][2][0], box[0][2][1]
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
            if(abs(lsty-cy) > self.args.thresh_line):
                if len(line) != 0:
                    texts.append(line)
                line = []
                line.append(i)
            else:
                line.append(i)
            lstx, lsty = cx, cy
        
        if len(line) != 0:
            texts.append(line)
            
        for line in texts:
            sorted_line = [sorted_boxes[i]
                        for i in sorted(line, key=lambda x: sorted_boxes[x][0][0][0])]
            # print(sorted_line)
            self.answer.append(sorted_line)
    
    def draw_raw(self, img):
        # 在原图上绘制排序后的文本框
        cnt = 0
        for j in self.answer:
            sorted_line = j
            for i, box in enumerate(sorted_line):
                x1, y1 = box[0][0][0], box[0][0][1]
                x2, y2 = box[0][2][0], box[0][2][1]
                x1, y1 = int(x1), int(y1)
                x2, y2 = int(x2), int(y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, str(cnt) + " " + box[1], (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cnt = cnt+1
        
        return img
    
    def getfa(self, x):
        if x != self.fa[x]:
            self.fa[x] = self.getfa(self.fa[x])
        return self.fa[x]
    
    def get_roots(self):
        self.fa = [i for i in range(len(self.answer))]
        
        def getfa(x):
            if x != self.fa[x]:
                self.fa[x] = getfa(self.fa[x])
            return self.fa[x]
        
        for sorted_line in self.answer:
            minx1, miny1, maxx2, maxy2 = int(1e9), int(1e9), 0, 0
            for box in sorted_line:
                minx1, miny1 = min(minx1,box[0][0][0]), min(miny1,box[0][0][1])
                maxx2, maxy2 = max(maxx2,box[0][2][0]), max(maxy2,box[0][2][1])
                
                maxx2, miny1 = max(maxx2,box[0][1][0]), min(miny1,box[0][1][1])
                minx1, maxy2 = min(minx1,box[0][3][0]), max(maxy2,box[0][3][1])
                
            self.center.append((miny1 + maxy2)/2)
            self.range.append((minx1, miny1, maxx2, maxy2))
        
        def merge(A, B):
            faA = getfa(B)
            faB = getfa(A)
            if faA != faB:
                self.fa[faA] = faB
                x1 = min(self.range[faA][0], self.range[faB][0])
                y1 = min(self.range[faA][1], self.range[faB][1])
                x2 = max(self.range[faA][2], self.range[faB][2])
                y2 = max(self.range[faA][3], self.range[faB][3])
                self.range[faB] = (x1, y1, x2, y2)
            return
        
        for i, _ in enumerate(self.answer):
            for j, _ in enumerate(self.answer):
                if i == j:
                    continue
                if abs(self.center[i] - self.center[j]) < self.args.thresh_box:
                    merge(i, j)
        
        for i, _ in enumerate(self.answer):
            if getfa(i) == i:
                self.root.append(i)
        
    def mask(self, img, x1, y1, x2, y2):
        roi = img[y1:y2, x1:x2]
    
        # 创建膨胀核
        kernel = np.ones((15, 15), np.uint8)

        # 应用膨胀操作
        roi = cv2.dilate(roi, kernel, iterations=3)
        img[y1:y2, x1:x2] = roi
        return img

    def draw_mask(self):
        height, width, _ = self.draw_img.shape

        # get mask
        for i in self.root:
            x1 = max(int(self.range[i][0]) - self.args.extra_size, 0)
            y1 = max(int(self.range[i][1]) - self.args.extra_size, 0)
            x2 = min(int(self.range[i][2]) + self.args.extra_size, width)
            y2 = min(int(self.range[i][3]) + self.args.extra_size, height)
            self.draw_img = self.mask(self.draw_img, x1, y1, x2, y2)
        
    
    def join_texts(self):
        self.text_line = []
        for _, line in enumerate(self.answer):
            str_list = []
            for _, box in enumerate(line):
                # print(box)
                str_list.append(box[1])
            self.text_line.append(" ".join(str_list))
        
        for i, line in enumerate(self.answer):
            fai = self.getfa(i)
            if fai == i:
                continue
            self.text_line[fai] = self.text_line[fai] + " " + self.text_line[i]
    
    def put_texts(self):
        img = Image.fromarray(self.draw_img)
        # 创建一个图像副本以便修改
        img_copy = img.copy()

        # 创建一个可以在图像上绘制文本的对象
        draw = ImageDraw.Draw(img_copy)

        # 指定字体文件和字体大小（根据需要更改）
        font_file = "SimHei.ttf"
        font_size = 35
        if self.args.resize:
            if self.scale > 1.0:
                font_size = int(font_size * self.scale)
        font = ImageFont.truetype(font_file, font_size, encoding="utf-8")

        for i in self.root:
            x1 = int(self.range[i][0])
            y1 = int(self.range[i][1])
            x2 = int(self.range[i][2])
            y2 = int(self.range[i][3])
            eng_text = self.text_line[i]
            cn_text = self.baidu_translate.translate(eng_text)
            # 在指定区域内绘制中文文本
            
            # 自动换行绘制中文文本
            text_width, text_height = draw.textsize(cn_text, font=font)
            max_width = x2 - x1  # 指定区域的宽度
            if text_width > max_width:
                # 文本超过指定区域宽度，需要进行自动换行
                lines = []
                line = ""
                for char in cn_text:
                    line_width, _ = draw.textsize(line + char, font=font)
                    if line_width <= max_width:
                        line += char
                    else:
                        lines.append(line)
                        line = char
                lines.append(line)
                # 在指定区域内绘制中文文本（自动换行）
                y = y1
                for line in lines:
                    draw.text((x1, y), line, fill=(0, 0, 0), font=font)
                    y += text_height
            else:
                # 文本未超过指定区域宽度，直接绘制在指定区域内
                draw.text((x1, y1), cn_text, fill=(0, 0, 0), font=font)
            print(eng_text)
            print(cn_text)

        # 显示图像
        # img_copy.show()

        img_copy = np.array(img_copy)
        self.draw_img = img_copy

    def solve(self):
        if self.args.resize:
            self.img = self.resize_img(img=self.img, scale_persent=self.scale)
            self.draw_img = self.resize_img(img=self.draw_img, scale_persent=self.scale)
        self.get_text()
        self.get_roots()
        self.draw_mask()
        self.join_texts()
        self.put_texts()
        if self.args.resize:
            self.draw_img = self.resize_img(img=self.draw_img, scale_persent=1.0/self.scale)
        cv2.imwrite(self.args.output, self.draw_img)
        if self.args.dewarp:
            import os
            os.remove(self.args.root0)

def main(args):
    ocr = OCR(args=args)
    ocr.solve()
    
    

if __name__ == '__main__':
    args = makeparse().parse_args()
    main(args)