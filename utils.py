import random as random
from PIL import Image
import os 

img_path = "E:\\fbendforsmartdetect\\img"

def generate_captcha():
    images = []
    val_str = []
    for filename in os.listdir(img_path):
        # 构建文件的完整路径
        file_path = os.path.join(img_path,filename)
        for files in os.listdir(file_path):
            files_path = os.path.join(file_path,files)
            if os.path.isfile(files_path) and files_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                try:
                # 打开图像
                    with Image.open(files_path) as img:
                    # 将图像添加到列表中
                        images.append(files_path)
                except IOError:
                    print(f"Cannot open image {files}. It will be skipped.")
            elif os.path.isfile(files_path) and files_path.lower().endswith(('.txt')):
                try:
                    with open(files_path, 'r', encoding='utf-8') as file:
                    # 读取文件内容
                        content = file.read()
                        val_str.append(content)
                except IOError:
                    print(f"Cannot open val_str {files_path}. It will be skipped.")
    print(len(images))
    index = random.randint(0,len(images) -1 )
    return images[index],val_str[index]    
