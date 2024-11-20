import os
from PIL import Image, ImageDraw

def create_image_grid(folder_path, row, col, a, b):
    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    # 找出最大的宽度和高度
    max_width = max_height = 0
    for img_file in image_files:
        with Image.open(os.path.join(folder_path, img_file)) as img:
            max_width = max(max_width, img.width)
            max_height = max(max_height, img.height)
    
    # 计算新图片的大小
    grid_width = col * (max_width + a) + a
    grid_height = row * (max_height + b) + b
    
    # 创建新图片（白色背景）
    new_image = Image.new('RGBA', (grid_width, grid_height), color=(255, 255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    
    # 在新图片上排列所有图片
    for i, img_file in enumerate(image_files[:row*col]):
        if i >= row * col:
            break
        
        x = (i % col) * (max_width + a) + a
        y = (i // col) * (max_height + b) + b
        
        with Image.open(os.path.join(folder_path, img_file)) as img:
            # 转换图片模式为RGBA
            img = img.convert('RGBA')
            
            # 计算缩放比例
            # scale = min(max_width / img.width, max_height / img.height)
            scale = 1
            
            new_size = (int(img.width / scale), int(img.height / scale))
            
            # 缩放图片
            img_resized = img.resize(new_size, Image.LANCZOS)
            
            # 创建一个白色背景的新图片
            img_with_bg = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 255))
            
            # 计算居中位置
            paste_x = (max_width - new_size[0]) // 2
            paste_y = (max_height - new_size[1]) // 2
            
            # 将缩放后的图片粘贴到白色背景上
            img_with_bg.paste(img_resized, (paste_x, paste_y), img_resized)
            
            # 在每个图片周围画一个黑色边框
            width = 15
            # draw.rectangle([x-1, y-1, x+max_width, y+max_height], outline='black', width=width)
            # 上边框
            draw.line([(x-1, y-1), (x+max_width, y-1)], fill='black', width=width)
            # 下边框
            draw.line([(x-1, y+max_height), (x+max_width, y+max_height)], fill='black', width=width)
            # 左边框
            draw.line([(x-1, y-1), (x-1, y+max_height)], fill='black', width=width)
            # 右边框
            draw.line([(x+max_width, y-1), (x+max_width, y+max_height)], fill='black', width=width)
            # 将带背景的图片粘贴到新图片上
            
            
            new_image.paste(img_with_bg, (x, y))
    
    return new_image



# 使用示例
folder_path = r"c:\Users\huali\Desktop\1_Work\1_硕士毕业论文\0_论文材料\0_论文插图\1 Blender渲染图-Imitation\Blender渲染图-Imitation"
row = 8
col = 9

# row = 3
# col = 4


a = 30  # 横向间隔
b = 40  # 纵向间隔

result = create_image_grid(folder_path, row, col, a, b)
# result.save('output_grid.png')
# 自定义保存图片的质量使得图片在3MB以下
# 将图片缩小到原来的0.5倍
scale = 0.3
result.thumbnail((result.width * scale, result.height * scale))
result.save('output/Blender渲染图-Imitation_6x9.png', quality=80, optimize=True)

print("Done")
