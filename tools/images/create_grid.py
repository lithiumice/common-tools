#!/usr/bin/env python3
import os
import argparse
from PIL import Image, ImageDraw

def create_image_grid(folder_path, output_path, row, col, h_spacing, v_spacing, scale_images=True):
    """
    创建图片网格，并将图片适当缩放以适应网格单元格
    
    参数:
    folder_path: 包含图片的文件夹路径
    output_path: 输出文件的路径
    row: 行数
    col: 列数
    h_spacing: 水平间距
    v_spacing: 垂直间距
    scale_images: 是否缩放图片以适应网格单元格
    """
    # 获取文件夹中的所有图片文件
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    if not image_files:
        print(f"错误: 在 {folder_path} 中未找到图片文件")
        return
    
    # 确保我们有足够的图片
    if len(image_files) < row * col:
        print(f"警告: 只找到 {len(image_files)} 个图片，少于请求的 {row*col} 个位置")
    
    # 找出所有图片中最大的宽度和高度
    max_width = max_height = 0
    for img_file in image_files:
        with Image.open(os.path.join(folder_path, img_file)) as img:
            max_width = max(max_width, img.width)
            max_height = max(max_height, img.height)
    
    # 计算新图片的大小
    grid_width = col * (max_width + h_spacing) + h_spacing
    grid_height = row * (max_height + v_spacing) + v_spacing
    
    # 创建新图片（白色背景）
    new_image = Image.new('RGBA', (grid_width, grid_height), color=(255, 255, 255, 255))
    draw = ImageDraw.Draw(new_image)
    
    # 在新图片上排列所有图片
    for i, img_file in enumerate(image_files):
        if i >= row * col:
            break
        
        x = (i % col) * (max_width + h_spacing) + h_spacing
        y = (i // col) * (max_height + v_spacing) + v_spacing
        
        with Image.open(os.path.join(folder_path, img_file)) as img:
            # 转换图片模式为RGBA
            img = img.convert('RGBA')
            
            if scale_images:
                # 计算缩放比例，以适应方框大小并保持纵横比
                scale = min(max_width / img.width, max_height / img.height)
                
                # 计算新的尺寸
                new_size = (int(img.width * scale), int(img.height * scale))
                
                # 缩放图片
                img_resized = img.resize(new_size, Image.LANCZOS)
            else:
                # 不缩放
                img_resized = img
            
            # 创建一个白色背景的新图片
            img_with_bg = Image.new('RGBA', (max_width, max_height), (255, 255, 255, 255))
            
            # 计算居中位置
            paste_x = (max_width - img_resized.width) // 2
            paste_y = (max_height - img_resized.height) // 2
            
            # 将缩放后的图片粘贴到白色背景上
            img_with_bg.paste(img_resized, (paste_x, paste_y), img_resized)
            
            # 在每个图片周围画一个黑色边框
            border_width = 15
            
            # 绘制边框
            draw.line([(x-1, y-1), (x+max_width, y-1)], fill='black', width=border_width)  # 上边框
            draw.line([(x-1, y+max_height), (x+max_width, y+max_height)], fill='black', width=border_width)  # 下边框
            draw.line([(x-1, y-1), (x-1, y+max_height)], fill='black', width=border_width)  # 左边框
            draw.line([(x+max_width, y-1), (x+max_width, y+max_height)], fill='black', width=border_width)  # 右边框
            
            # 将带背景的图片粘贴到新图片上
            new_image.paste(img_with_bg, (x, y))
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 保存图片
    # 如果是RGBA模式但保存为JPG，需要转换为RGB
    if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        if new_image.mode == 'RGBA':
            # 创建白色背景
            background = Image.new('RGB', new_image.size, (255, 255, 255))
            # 合成图像
            background.paste(new_image, mask=new_image.split()[3])  # 使用alpha通道作为mask
            new_image = background
        
    new_image.save(output_path, quality=80, optimize=True)
    print(f"图片网格已保存到: {output_path}")
    
    return new_image

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='创建图片网格')
    parser.add_argument('folder_path', help='包含图片的文件夹路径')
    parser.add_argument('-o', '--output', default='output_grid.jpg', help='输出文件路径')
    parser.add_argument('-r', '--rows', type=int, default=3, help='行数')
    parser.add_argument('-c', '--cols', type=int, default=3, help='列数')
    parser.add_argument('-hs', '--hspacing', type=int, default=30, help='水平间距')
    parser.add_argument('-vs', '--vspacing', type=int, default=40, help='垂直间距')
    parser.add_argument('-s', '--scale', type=float, default=1.0, help='最终输出图片的缩放比例')
    parser.add_argument('--no-fit', action='store_true', help='不缩放图片以适应网格单元格')
    parser.add_argument('-q', '--quality', type=int, default=80, help='JPEG质量 (1-95)')
    
    args = parser.parse_args()
    
    # 创建图片网格
    result = create_image_grid(
        args.folder_path, 
        args.output, 
        args.rows, 
        args.cols, 
        args.hspacing, 
        args.vspacing,
        not args.no_fit
    )
    
    # 如果需要进一步缩放最终输出
    if args.scale != 1.0:
        result.thumbnail((int(result.width * args.scale), int(result.height * args.scale)))
        # 如果是RGBA模式但保存为JPG，需要转换为RGB
        if args.output.lower().endswith('.jpg') or args.output.lower().endswith('.jpeg'):
            if result.mode == 'RGBA':
                # 创建白色背景
                background = Image.new('RGB', result.size, (255, 255, 255))
                # 合成图像
                background.paste(result, mask=result.split()[3])  # 使用alpha通道作为mask
                result = background
        
        result.save(args.output, quality=args.quality, optimize=True)
        print(f"最终图片已缩放为原尺寸的 {args.scale} 倍")

if __name__ == "__main__":
    main()