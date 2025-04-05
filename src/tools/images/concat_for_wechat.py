from PIL import Image
from natsort import natsorted
import os

def process_images(input_folder, output_file, target_width, spacing):
    # 获取输入文件夹中的所有图片
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    images = []

    # 读取并调整图片大小
    for image_file in image_files:
        img = Image.open(os.path.join(input_folder, image_file))
        aspect_ratio = img.height / img.width
        new_height = int(target_width * aspect_ratio)
        img_resized = img.resize((target_width, new_height), Image.LANCZOS)
        images.append(img_resized)

    # 计算总高度
    total_height = sum(img.height for img in images) + spacing * (len(images) - 1)

    # 创建新图像
    result_image = Image.new('RGB', (target_width, total_height), color='white')

    # 粘贴调整大小后的图像
    y_offset = 0
    for img in images:
        result_image.paste(img, (0, y_offset))
        y_offset += img.height + spacing

    # 保存结果
    result_image.save(output_file)
    print(f"已保存拼接后的图片: {output_file}")

# 使用示例
input_folder = r'Z:\图片合集\相机照片\Nikon Z30\修图 lightroom\新建文件夹\广州塔 人文 2'
input_folder = r'Z:\图片合集\相机照片\Nikon Z30\修图 lightroom\新建文件夹\广州塔 建筑风景'
input_folder = r'Z:\图片合集\相机照片\Nikon Z30\修图 lightroom\新建文件夹\广州塔 人文'
input_folder = r'Z:\图片合集\相机照片\Nikon Z30\修图 lightroom\新建文件夹\白云山 人文'
input_folder = r'Z:\图片合集\相机照片\Nikon Z30\修图 lightroom\新建文件夹\白云山 人文 2'
input_folder = r'Z:\图片合集\相机照片\Nikon Z30\修图 lightroom\新建文件夹\白云山 人文 3'
input_folder = r'Z:\图片合集\相机照片\Nikon Z30\修图 lightroom\新建文件夹\白云山 风景'
input_folder = r'Z:\图片合集\相机照片\Nikon Z30\修图 lightroom\新建文件夹\白云山 风景 2'


output_file = input_folder + '.jpg'
target_width = 800  # 目标宽度
spacing = 10  # 图片之间的间隔像素

process_images(input_folder, output_file, target_width, spacing)