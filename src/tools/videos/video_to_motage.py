import cv2
import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import math
import argparse

def extract_frames(video_path, output_dir, interval=1):
    """
    从视频中按间隔提取帧
    
    参数:
    video_path: 视频文件路径
    output_dir: 输出目录
    interval: 间隔秒数
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    vidcap = cv2.VideoCapture(video_path)
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval)
    
    success, image = vidcap.read()
    count = 0
    frame_count = 0
    
    while success:
        if count % frame_interval == 0:
            cv2.imwrite(f"{output_dir}/frame_{frame_count:04d}.png", image)
            frame_count += 1
        success, image = vidcap.read()
        count += 1
        
    print(f"共提取了 {frame_count} 帧")
    return frame_count

def optimize_frames(input_dir, output_dir, target_width=800):
    """
    优化帧的尺寸、对比度和锐度
    
    参数:
    input_dir: 输入图像目录
    output_dir: 输出目录
    target_width: 目标宽度
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    optimized_count = 0
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_dir, filename)
            img = Image.open(img_path)
            
            # 调整尺寸
            width, height = img.size
            new_width = target_width
            new_height = int(height * (new_width / width))
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # 提高对比度
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)  # 增加20%的对比度
            
            # 锐化
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(1.5)  # 增加50%的锐度
            
            # 保存
            img.save(os.path.join(output_dir, filename), quality=95)
            optimized_count += 1
    
    print(f"已优化 {optimized_count} 帧")
    return optimized_count

def create_montage(input_dir, output_path, cols=4, margin=10, title="连续帧可视化展示"):
    """
    创建帧拼接图
    
    参数:
    input_dir: 输入图像目录
    output_path: 输出拼接图路径
    cols: 每行的图像数量
    margin: 图像间距
    title: 拼接图标题
    """
    # 获取所有图像文件
    image_files = [f for f in os.listdir(input_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()  # 确保按顺序排列
    
    if not image_files:
        print("未找到图像文件")
        return None
    
    # 加载第一张图片以获取尺寸
    first_img = Image.open(os.path.join(input_dir, image_files[0]))
    img_width, img_height = first_img.size
    
    # 计算行数
    num_images = len(image_files)
    rows = math.ceil(num_images / cols)
    
    # 创建拼接画布 (添加顶部空间用于标题)
    title_height = 60
    canvas_width = cols * img_width + (cols + 1) * margin
    canvas_height = rows * img_height + (rows + 1) * margin + title_height
    canvas = Image.new('RGB', (canvas_width, canvas_height), color=(255, 255, 255))
    
    # 绘图对象
    draw = ImageDraw.Draw(canvas)
    
    # 加载字体
    try:
        frame_font = ImageFont.truetype("arial.ttf", 20)
        title_font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        frame_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # 添加标题
    title_width = draw.textlength(title, font=title_font) if hasattr(draw, 'textlength') else len(title) * 20
    draw.text(((canvas_width - title_width) // 2, margin), title, fill=(0, 0, 0), font=title_font)
    
    # 放置图像
    for i, img_file in enumerate(image_files):
        img = Image.open(os.path.join(input_dir, img_file))
        row = i // cols
        col = i % cols
        x = margin + col * (img_width + margin)
        y = margin + title_height + row * (img_height + margin)
        canvas.paste(img, (x, y))
        
        # 添加帧编号 (半透明背景)
        label_width = 40
        label_height = 30
        # 创建半透明的矩形
        overlay = Image.new('RGBA', (label_width, label_height), (255, 255, 255, 180))
        canvas.paste(overlay, (x, y), overlay)
        # 添加文本
        draw.text((x+5, y+5), f"{i+1}", fill=(0, 0, 0), font=frame_font)
    
    # 保存拼接图
    canvas.save(output_path, quality=95, dpi=(300, 300))
    print(f"拼接图已保存至 {output_path}")
    return output_path

def video_to_montage(video_path, output_dir="output", output_filename="paper_figure.png", 
                    interval=2, cols=4, margin=15, width=800, title=None):
    """
    完整的视频到论文图的转换流程
    
    参数:
    video_path: 视频文件路径
    output_dir: 输出目录
    output_filename: 输出文件名
    interval: 帧间隔(秒)
    cols: 每行的图像数量
    margin: 图像间距
    width: 目标图像宽度
    title: 拼接图标题
    """
    if title is None:
        video_name = os.path.splitext(os.path.basename(video_path))[0]
        title = f"{video_name} - 可视化过程展示"
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    frames_dir = os.path.join(output_dir, "frames")
    optimized_dir = os.path.join(output_dir, "optimized")
    
    # 1. 提取帧
    print(f"步骤1/3: 正在从视频提取帧 (每{interval}秒)...")
    frame_count = extract_frames(video_path, frames_dir, interval)
    
    # 2. 优化帧
    print(f"步骤2/3: 正在优化{frame_count}个帧...")
    # optimize_frames(frames_dir, optimized_dir, width)
    optimized_dir = frames_dir
    
    # 3. 创建拼接图
    print(f"步骤3/3: 正在创建拼接图 (每行{cols}帧)...")
    output_path = os.path.join(output_dir, output_filename)
    result = create_montage(optimized_dir, output_path, cols, margin, title)
    
    if result:
        print(f"\n完成! 最终图像已保存至: {os.path.abspath(output_path)}")
        print(f"分辨率: 300 DPI, 适合论文使用")
        return output_path
    else:
        print("处理失败")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="将视频转换为论文连续帧拼接图")
    parser.add_argument("video_path", help="输入视频的路径")
    parser.add_argument("--output-dir", default="output", help="输出目录")
    parser.add_argument("--output-filename", default="paper_figure.png", help="输出文件名")
    parser.add_argument("--interval", type=float, default=2.0, help="提取帧的时间间隔(秒)")
    parser.add_argument("--cols", type=int, default=4, help="每行显示的帧数量")
    parser.add_argument("--margin", type=int, default=15, help="帧之间的间距")
    parser.add_argument("--width", type=int, default=800, help="每个帧的目标宽度")
    parser.add_argument("--title", help="拼接图的标题")
    
    args = parser.parse_args()
    
    video_to_montage(
        args.video_path, 
        args.output_dir, 
        args.output_filename, 
        args.interval, 
        args.cols, 
        args.margin, 
        args.width, 
        args.title
    )