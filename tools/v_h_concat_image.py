import os
from PIL import Image

def get_files_sorted_by_number(folder_path, extension=".png"):
    # 获取文件夹中的所有文件名
    files = [f for f in os.listdir(folder_path) if f.endswith(extension)]
    
    # 按文件名中的数字排序
    # files.sort(key=lambda x: int(os.path.splitext(x)[0]))
    from natsort import natsorted
    files = natsorted(files)
    
    return files

def select_divisible_by_10(files):
    # 选择序号整除10的文件
    return [f for i, f in enumerate(files, start=1) if i % 10 == 0]

def concatenate_images_horizontally(images):
    # 获取所有图像的高度和总宽度
    heights = [img.height for img in images]
    widths = [img.width for img in images]
    
    max_height = max(heights)
    total_width = sum(widths)
    
    # 创建一个新的空白图像
    new_image = Image.new('RGBA', (total_width, max_height))
    
    # 将图像粘贴到新图像中
    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.width
    
    return new_image

def main(folder_path, output_path):
    # 获取文件夹中所有PNG文件并按序号排序
    files = get_files_sorted_by_number(folder_path)
    
    # 选择序号整除10的文件
    divisible_by_10_files = select_divisible_by_10(files)
    
    # 只取前10个文件
    selected_files = divisible_by_10_files[:10]
    
    # 打开并加载图像
    images = [Image.open(os.path.join(folder_path, f)) for f in selected_files]
    
    # 横向拼接图像
    concatenated_image = concatenate_images_horizontally(images)
    
    # 保存结果图像
    concatenated_image.save(output_path)


def m0():
    folder_path = r"c:\Users\huali\Desktop\1_Work\1_硕士毕业论文\0_论文材料\2 MoCap Benchmark\1_taijiquan\taijiquan原始视频"  # 替换为你的文件夹路径
    output_path = "output/taijiquan原始视频.png"     # 替换为你希望保存的输出文件路径
    main(folder_path, output_path)
    
    
def m1():
    folder_path = r"C:\Users\huali\Desktop\1_Work\1_硕士毕业论文\0_论文材料\2 MoCap Benchmark\1_taijiquan\wham和difftraj对比\difftraj_0_c2_blender_high_orange"  # 替换为你的文件夹路径
    output_path = "output/difftraj_0_c2_blender_high_orange.png"     # 替换为你希望保存的输出文件路径
    main(folder_path, output_path)
    

def m2():
    folder_path = r"C:\Users\huali\Desktop\1_Work\1_硕士毕业论文\0_论文材料\2 MoCap Benchmark\1_taijiquan\wham和difftraj对比\wham_0_blender_high_orange"  # 替换为你的文件夹路径
    output_path = "output/wham_0_blender_high_orange.png"     # 替换为你希望保存的输出文件路径
    main(folder_path, output_path)
    

    
if __name__ == "__main__":
    m0()