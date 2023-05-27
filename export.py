import easyocr
import cv2
import numpy as np
from tools.baidu_translate import baiduTranslate
from PIL import Image, ImageDraw, ImageFont
from tools.OCRParser import makeparse

from sklearn.cluster import KMeans ,AgglomerativeClustering
from sklearn.preprocessing import MinMaxScaler

from tools.checker import correct_spelling

class OCR(object):
    def __init__(self, args):
        self.args = args
        if self.args.dewarp:
            from tools.dewarp import process
            self.args.root1 = self.args.root0 = process(self.args.root0)
        self.img = cv2.imread(self.args.root0)
        self.draw_img = cv2.imread(self.args.root1)
        if self.args.resize:
            self.scale = 2160 / self.img.shape[1]
        self.baidu_translate = baiduTranslate(args.uid, args.bkey)
        self.reader = easyocr.Reader(['en'], gpu=args.gpu)
        self.range = []
        # self.text_in_paragraphs
    
    def resize_img(self, img, scale_persent):
        original_height, original_width = img.shape[:2]
        # scale_persent = 2160 / original_width
        new_height = int(original_height * scale_persent)
        new_width = int(original_width * scale_persent)
        new_dim = (new_width, new_height)
        enlarged_image = cv2.resize(img, new_dim, interpolation=cv2.INTER_LINEAR)
        return enlarged_image
    
    def get_default(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        pre_result = self.reader.readtext(gray)
        
        # 按照文本框的中心点的横坐标进行排序
        sorted_pre_result = sorted(pre_result, key=lambda box: (box[0][0][1] + box[0][2][1]) / 2)

        split_threshold = self.args.thresh_box  # 根据实际情况调整

        self.paragraphs = [[]]  # 初始化段落列表
        current_paragraph = self.paragraphs[0]

        for box in sorted_pre_result:
            if len(current_paragraph) == 0:
                current_paragraph.append(box)
            else:
                prev_box = current_paragraph[-1]
                center_diff = abs(prev_box[0][0][1] + prev_box[0][2][1] - box[0][0][1] - box[0][2][1]) / 2
                if center_diff > split_threshold:
                    current_paragraph = [box]
                    self.paragraphs.append(current_paragraph)
                else:
                    current_paragraph.append(box)
        print(len(self.paragraphs))
    
    def get_kmeans(self, clusters):
        # 读取图片并进行灰度处理
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # 使用OCR识别文本框，并提取位置信息
        pre_result = self.reader.readtext(gray)
        pre_centers = []
        for box in pre_result:
            x1, y1 = box[0][0][0], box[0][0][1]
            x2, y2 = box[0][2][0], box[0][2][1]
            center = [(x1 + x2) / 2, (y1 + y2) / 2]
            pre_centers.append(center)

        # 将位置信息转换为聚类算法的输入格式
        X = np.array(pre_centers)
        scaler = MinMaxScaler()
        X_normalized = scaler.fit_transform(X)
        print(X_normalized)
        
        # 聚类算法
        kmeans = KMeans(n_clusters=clusters, random_state=0).fit(X_normalized)

        # 获取聚类结果，每个类别对应一个段落
        labels = kmeans.labels_
        self.paragraphs = [[] for _ in range(clusters)]
        for i in range(len(labels)):
            self.paragraphs[labels[i]].append(pre_result[i])
    
    def get_agglomerative(self):
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        # 生成样本数据，每个样本是一个文本框的位置信息
        pre_result = self.reader.readtext(gray)
        pre_centers = []
        for box in pre_result:
            x1, y1 = box[0][0][0], box[0][0][1]
            x2, y2 = box[0][2][0], box[0][2][1]
            center = [(x1 + x2) / 2, (y1 + y2) / 2]
            pre_centers.append(center)

        # 将位置信息转换为聚类算法的输入格式
        X = np.array(pre_centers)
        # 归一化
        scaler = MinMaxScaler()
        X_normalized = scaler.fit_transform(X)
        print(X_normalized)

        # 聚类算法
        agg_clustering = AgglomerativeClustering(n_clusters=None, distance_threshold=3.0, linkage='ward')
        labels = agg_clustering.fit_predict(X_normalized)

        # 获取聚类结果，每个类别对应一个段落
        n_clusters = len(set(labels))
        self.paragraphs = [[] for _ in range(n_clusters)]
        for i in range(len(labels)):
            self.paragraphs[labels[i]].append(pre_result[i])

        print(len(self.paragraphs))
    
    def sort_boxes(self, paragraph):
        pre_centers = []
        for box in paragraph:
            x1, y1 = box[0][0][0], box[0][0][1]
            x2, y2 = box[0][2][0], box[0][2][1]
            center = [(x1 + x2) / 2, (y1 + y2) / 2]
            pre_centers.append(center)
        
        # 对一个paragraph内的box进行从上到下，从左到右的排序
        sorted_paragraph = [x for _, x in sorted(zip(pre_centers, paragraph), key=lambda pair: (pair[0][1], pair[0][0]))]
        
        return sorted_paragraph
    
    def sort_paragraph(self):
        for i, paragraph in enumerate(self.paragraphs):
            self.paragraphs[i] = self.sort_boxes(paragraph)
        print(self.paragraphs)
    
    def merge_text(self, paragraph):
        def sort_line(line):
            sorted_line = sorted(line, key=lambda box: box[0][0][0])  # 按照盒子的左边界位置进行排序
            return sorted_line
        line = []
        lsty = -100
        text = " "
        for box in paragraph:
            y1, y2 = box[0][0][1], box[0][2][1]
            cy = (y1 + y2) /2
            if(abs(lsty-cy) > self.args.thresh_line):
                if len(line) != 0:
                    line = sort_line(line)
                    words = [box[1] for box in line]
                    joined_words = " ".join(words)
                    text = text + joined_words + " "
                line = []
            line.append(box)
            lsty = cy
        if len(line) != 0:
            line = sort_line(line)
            words = [box[1] for box in line]
            joined_words = " ".join(words)
            text = text + joined_words + " "
        print(text)
        return text
    
    def merge(self):
        
        self.text = []
        for paragraph in self.paragraphs:
            min_x, min_y = float('inf'), float('inf')
            max_x, max_y = float('-inf'), float('-inf')
            paragraph_text = self.merge_text(paragraph=paragraph)
            for box in paragraph:
                points = box[0]
                for point in points:
                    x, y = point
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)
            
            self.range.append((min_x, min_y, max_x, max_y))
            self.text.append(paragraph_text)
        print(self.text)
        print(self.range)
    
    
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

        for range in self.range:
            x1, y1, x2, y2 = range
            x1 = max(int(x1) - self.args.extra_size, 0)
            y1 = max(int(y1) - self.args.extra_size, 0)
            x2 = min(int(x2) + self.args.extra_size, width)
            y2 = min(int(y2) + self.args.extra_size, height)
            self.draw_img = self.mask(self.draw_img, x1, y1, x2, y2)
    
    def llama_correct(self, paragraph_text):
        from tools.sentence_split import sentence_token_nltk
        from posts.llama_POST import submit_request
        sents = sentence_token_nltk(paragraph_text)
        text = ""
        for sent in sents:
            result_list = submit_request(sent)
            raw_answer = result_list[0]
            answers = raw_answer.split("Answer:")
            last_answer = answers[-1].strip()
            real_answer = last_answer.replace("Answer:", "").strip()
            text = text + real_answer + " "
        return text
    
    def put_texts(self):
        img = Image.fromarray(self.draw_img)
        # 创建一个图像副本以便修改
        img_copy = img.copy()

        # 创建一个可以在图像上绘制文本的对象
        draw = ImageDraw.Draw(img_copy)

        # 指定字体文件和字体大小（根据需要更改）
        font_file = "./src/SimHei.ttf"
        font_size = self.args.font_size
        if self.args.resize:
            if self.scale > 1.0:
                font_size = int(font_size * self.scale)
        font = ImageFont.truetype(font_file, font_size, encoding="utf-8")

        for i in range(len(self.paragraphs)):
            x1 = int(self.range[i][0])
            y1 = int(self.range[i][1])
            x2 = int(self.range[i][2])
            y2 = int(self.range[i][3])
            eng_text = self.text[i]
            # eng_text = correct_spelling(eng_text)
            if self.args.llama and len(eng_text) > 20:
                eng_text = self.llama_correct(eng_text)
            else:
                eng_text = correct_spelling(eng_text)
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
        if self.args.model == 0:
            self.get_default()
        elif self.args.model == 1:
            self.get_kmeans(2)
        else:
            self.get_agglomerative()
        self.sort_paragraph()
        self.merge()
        self.draw_mask()
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