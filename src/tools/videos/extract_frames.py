# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-

# import argparse
# import os
# import subprocess
# import json
# import math


# def get_video_info(video_path):
#     """获取视频信息：总帧数、帧率、时长等"""
#     cmd = ['ffprobe', 
#            '-v', 'quiet', 
#            '-print_format', 'json', 
#            '-show_format', 
#            '-show_streams', 
#            video_path]
    
#     result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     info = json.loads(result.stdout)
    
#     # 找到视频流
#     video_stream = None
#     for stream in info['streams']:
#         if stream['codec_type'] == 'video':
#             video_stream = stream
#             break
    
#     if not video_stream:
#         raise ValueError("No video stream found in the input file")
    
#     # 提取信息
#     frame_rate = eval(video_stream.get('avg_frame_rate', '0/0'))  # 可能是形如 "24/1" 的字符串
#     duration = float(info['format'].get('duration', '0'))
    
#     # 有些视频可能没有明确的nb_frames
#     if 'nb_frames' in video_stream:
#         total_frames = int(video_stream['nb_frames'])
#     else:
#         # 估算总帧数
#         total_frames = int(duration * frame_rate)
    
#     return {
#         'total_frames': total_frames,
#         'frame_rate': frame_rate,
#         'duration': duration,
#         'width': int(video_stream.get('width', 0)),
#         'height': int(video_stream.get('height', 0))
#     }


# def extract_by_frame_interval(video_path, output_dir, interval, format='jpg', quality=2):
#     """每隔n帧提取一张图片"""
#     os.makedirs(output_dir, exist_ok=True)
    
#     # 构建ffmpeg命令
#     output_path = os.path.join(output_dir, f'frame_%04d.{format}')
#     cmd = [
#         'ffmpeg',
#         '-i', video_path,
#         '-vf', f'select=not(mod(n\,{interval}))',
#         '-vsync', 'vfr',
#         '-q:v', str(quality),
#         '-frame_pts', '0',
#         output_path
#     ]
    
#     print(f"Running: {' '.join(cmd)}")
#     subprocess.run(cmd)
#     print(f"提取完成，文件保存在: {output_dir}")


# def extract_by_time_interval(video_path, output_dir, interval_sec, format='jpg', quality=2):
#     """每隔n秒提取一张图片"""
#     os.makedirs(output_dir, exist_ok=True)
    
#     # 构建ffmpeg命令
#     output_path = os.path.join(output_dir, f'frame_%04d.{format}')
#     cmd = [
#         'ffmpeg',
#         '-i', video_path,
#         '-vf', f'fps=1/{interval_sec}',
#         '-q:v', str(quality),
#         output_path
#     ]
    
#     print(f"Running: {' '.join(cmd)}")
#     subprocess.run(cmd)
#     print(f"提取完成，文件保存在: {output_dir}")


# def extract_total_frames(video_path, output_dir, total_frames, format='jpg', quality=2):
#     """总共提取m张均匀分布的图片"""
#     os.makedirs(output_dir, exist_ok=True)
    
#     # 获取视频信息
#     info = get_video_info(video_path)
    
#     # 计算提取间隔
#     # 取整，确保提取帧数不超过请求的数量
#     interval = math.ceil(info['total_frames'] / total_frames)
    
#     # 构建ffmpeg命令
#     output_path = os.path.join(output_dir, f'frame_%04d.{format}')
#     cmd = [
#         'ffmpeg',
#         '-i', video_path,
#         '-vf', f'select=not(mod(n\,{interval}))',
#         '-vsync', 'vfr',
#         '-q:v', str(quality),
#         '-frames:v', str(total_frames),
#         output_path
#     ]
    
#     print(f"Running: {' '.join(cmd)}")
#     subprocess.run(cmd)
#     print(f"提取完成，文件保存在: {output_dir}")


# def extract_keyframes(video_path, output_dir, format='jpg', quality=2):
#     """仅提取关键帧"""
#     os.makedirs(output_dir, exist_ok=True)
    
#     # 构建ffmpeg命令
#     output_path = os.path.join(output_dir, f'keyframe_%04d.{format}')
#     cmd = [
#         'ffmpeg',
#         '-i', video_path,
#         '-vf', 'select=eq(pict_type\,I)',
#         '-vsync', 'vfr',
#         '-q:v', str(quality),
#         output_path
#     ]
    
#     print(f"Running: {' '.join(cmd)}")
#     subprocess.run(cmd)
#     print(f"提取完成，文件保存在: {output_dir}")


# def extract_scene_changes(video_path, output_dir, threshold=0.4, format='jpg', quality=2):
#     """提取场景变化帧"""
#     os.makedirs(output_dir, exist_ok=True)
    
#     # 构建ffmpeg命令
#     output_path = os.path.join(output_dir, f'scene_%04d.{format}')
#     cmd = [
#         'ffmpeg',
#         '-i', video_path,
#         '-vf', f'select=gt(scene\,{threshold})',
#         '-vsync', 'vfr',
#         '-q:v', str(quality),
#         output_path
#     ]
    
#     print(f"Running: {' '.join(cmd)}")
#     subprocess.run(cmd)
#     print(f"提取完成，文件保存在: {output_dir}")


# def main():
#     parser = argparse.ArgumentParser(description='从视频中提取帧')
#     parser.add_argument('video_path', help='输入视频文件路径')
#     parser.add_argument('output_dir', help='输出目录路径')
    
#     # 提取方式子命令
#     subparsers = parser.add_subparsers(dest='mode', help='提取模式', required=True)
    
#     # 1. 间隔n帧提取一张
#     frame_parser = subparsers.add_parser('frame', help='按帧间隔提取')
#     frame_parser.add_argument('-i', '--interval', type=int, required=True, help='帧间隔')
    
#     # 2. 间隔n秒提取一张
#     time_parser = subparsers.add_parser('time', help='按时间间隔提取')
#     time_parser.add_argument('-i', '--interval', type=float, required=True, help='时间间隔(秒)')
    
#     # 3. 总共提取m张
#     total_parser = subparsers.add_parser('total', help='提取指定总数的帧')
#     total_parser.add_argument('-n', '--number', type=int, required=True, help='总共提取的帧数')
    
#     # 4. 提取关键帧
#     key_parser = subparsers.add_parser('keyframe', help='只提取关键帧')
    
#     # 5. 提取场景变化帧
#     scene_parser = subparsers.add_parser('scene', help='提取场景变化帧')
#     scene_parser.add_argument('-t', '--threshold', type=float, default=0.4, 
#                               help='场景变化阈值(0.0-1.0)，越大表示要求变化越明显')
    
#     # 所有模式通用参数
#     for p in [frame_parser, time_parser, total_parser, key_parser, scene_parser]:
#         p.add_argument('-f', '--format', type=str, default='jpg', 
#                        choices=['jpg', 'png', 'bmp'], help='输出图片格式')
#         p.add_argument('-q', '--quality', type=int, default=2, 
#                        choices=range(1, 32), help='图片质量(1-31)，1最高')
    
#     args = parser.parse_args()
    
#     # 根据模式执行不同的提取方法
#     if args.mode == 'frame':
#         extract_by_frame_interval(args.video_path, args.output_dir, args.interval, 
#                                  args.format, args.quality)
#     elif args.mode == 'time':
#         extract_by_time_interval(args.video_path, args.output_dir, args.interval, 
#                                 args.format, args.quality)
#     elif args.mode == 'total':
#         extract_total_frames(args.video_path, args.output_dir, args.number, 
#                             args.format, args.quality)
#     elif args.mode == 'keyframe':
#         extract_keyframes(args.video_path, args.output_dir, args.format, args.quality)
#     elif args.mode == 'scene':
#         extract_scene_changes(args.video_path, args.output_dir, args.threshold, 
#                              args.format, args.quality)


# if __name__ == '__main__':
#     main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import json
import math
import tempfile
from PIL import Image, ImageDraw, ImageFont


def get_video_info(video_path):
    """获取视频信息：总帧数、帧率、时长等"""
    cmd = ['ffprobe', 
           '-v', 'quiet', 
           '-print_format', 'json', 
           '-show_format', 
           '-show_streams', 
           video_path]
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    info = json.loads(result.stdout)
    
    # 找到视频流
    video_stream = None
    for stream in info['streams']:
        if stream['codec_type'] == 'video':
            video_stream = stream
            break
    
    if not video_stream:
        raise ValueError("No video stream found in the input file")
    
    # 提取信息
    frame_rate = eval(video_stream.get('avg_frame_rate', '0/0'))  # 可能是形如 "24/1" 的字符串
    duration = float(info['format'].get('duration', '0'))
    
    # 有些视频可能没有明确的nb_frames
    if 'nb_frames' in video_stream:
        total_frames = int(video_stream['nb_frames'])
    else:
        # 估算总帧数
        total_frames = int(duration * frame_rate)
    
    return {
        'total_frames': total_frames,
        'frame_rate': frame_rate,
        'duration': duration,
        'width': int(video_stream.get('width', 0)),
        'height': int(video_stream.get('height', 0))
    }


def add_frame_info(image_path, current_frame, total_frames):
    """在图片左上角添加帧信息"""
    try:
        # 打开图片
        img = Image.open(image_path)
        img_width, img_height = img.size
        
        # 计算字体大小为图像高度的1/10
        font_size = max(int(img_height / 10), 12)  # 最小字体大小为12
        
        # 加载字体，尝试加载宋体，如果找不到则使用默认字体
        try:
            # 尝试加载系统宋体
            font = ImageFont.truetype("simsun.ttc", font_size)
        except OSError:
            try:
                # macOS系统尝试
                font = ImageFont.truetype("/System/Library/Fonts/STHeiti Light.ttc", font_size)
            except OSError:
                # 如果都找不到，使用默认字体
                font = ImageFont.load_default()
        
        draw = ImageDraw.Draw(img)
        
        # 绘制白色背景框
        text = f"{current_frame}/{total_frames}"
        
        # 使用兼容不同版本PIL/Pillow的方法获取文本尺寸
        if hasattr(draw, 'textsize'):  # 旧版Pillow
            text_width, text_height = draw.textsize(text, font=font)
        elif hasattr(font, 'getbbox'):  # Pillow 9.0.0+
            bbox = font.getbbox(text)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
        else:  # 尝试其他方法
            # 预估文本尺寸，基于图像尺寸
            text_width = int(img_width * 0.2)  # 大约占宽度的20%
            text_height = font_size
        
        # 添加一些内边距
        padding = max(int(font_size * 0.3), 5)
        
        # 绘制白色背景框
        draw.rectangle(
            [(padding, padding), 
             (text_width + padding * 2, text_height + padding * 2)], 
            fill='white'
        )
        
        # 绘制黑色文本
        draw.text((padding * 1.5, padding), text, fill='black', font=font)
        
        # 保存图片
        img.save(image_path)
        return True
    except Exception as e:
        print(f"添加帧信息时出错: {e}")
        return False


def process_extracted_frames(temp_dir, output_dir, total_frames, format='jpg'):
    """处理提取的帧，添加帧信息并重命名"""
    # 获取临时目录中的所有图片文件
    files = sorted([f for f in os.listdir(temp_dir) if f.endswith(f'.{format}')])
    
    for i, file in enumerate(files):
        current_frame = i + 1  # 当前处理的是第几张
        temp_path = os.path.join(temp_dir, file)
        
        # 添加帧信息
        add_frame_info(temp_path, current_frame, len(files))
        
        # 重命名并移动到输出目录
        output_path = os.path.join(output_dir, f'frame_{current_frame}_of_{len(files)}.{format}')
        os.rename(temp_path, output_path)


def extract_by_frame_interval(video_path, output_dir, interval, format='jpg', quality=2):
    """每隔n帧提取一张图片"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取视频信息
    info = get_video_info(video_path)
    total_frames = info['total_frames']
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 构建ffmpeg命令提取到临时目录
        temp_output_path = os.path.join(temp_dir, f'frame_%04d.{format}')
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'select=not(mod(n\,{interval}))',
            '-vsync', 'vfr',
            '-q:v', str(quality),
            '-frame_pts', '0',
            temp_output_path
        ]
        
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        
        # 处理提取的帧
        process_extracted_frames(temp_dir, output_dir, total_frames, format)
    
    print(f"提取完成，文件保存在: {output_dir}")


def extract_by_time_interval(video_path, output_dir, interval_sec, format='jpg', quality=2):
    """每隔n秒提取一张图片"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取视频信息
    info = get_video_info(video_path)
    total_frames = info['total_frames']
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 构建ffmpeg命令提取到临时目录
        temp_output_path = os.path.join(temp_dir, f'frame_%04d.{format}')
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'fps=1/{interval_sec}',
            '-q:v', str(quality),
            temp_output_path
        ]
        
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        
        # 处理提取的帧
        process_extracted_frames(temp_dir, output_dir, total_frames, format)
    
    print(f"提取完成，文件保存在: {output_dir}")


def extract_total_frames(video_path, output_dir, total_frames_to_extract, format='jpg', quality=2):
    """总共提取m张均匀分布的图片"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取视频信息
    info = get_video_info(video_path)
    total_frames = info['total_frames']
    
    # 计算提取间隔
    # 取整，确保提取帧数不超过请求的数量
    interval = math.ceil(total_frames / total_frames_to_extract)
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 构建ffmpeg命令提取到临时目录
        temp_output_path = os.path.join(temp_dir, f'frame_%04d.{format}')
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'select=not(mod(n\,{interval}))',
            '-vsync', 'vfr',
            '-q:v', str(quality),
            '-frames:v', str(total_frames_to_extract),
            temp_output_path
        ]
        
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        
        # 处理提取的帧
        process_extracted_frames(temp_dir, output_dir, total_frames, format)
    
    print(f"提取完成，文件保存在: {output_dir}")


def extract_keyframes(video_path, output_dir, format='jpg', quality=2):
    """仅提取关键帧"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取视频信息
    info = get_video_info(video_path)
    total_frames = info['total_frames']
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 构建ffmpeg命令提取到临时目录
        temp_output_path = os.path.join(temp_dir, f'keyframe_%04d.{format}')
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', 'select=eq(pict_type\,I)',
            '-vsync', 'vfr',
            '-q:v', str(quality),
            temp_output_path
        ]
        
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        
        # 处理提取的帧
        process_extracted_frames(temp_dir, output_dir, total_frames, format)
    
    print(f"提取完成，文件保存在: {output_dir}")


def extract_scene_changes(video_path, output_dir, threshold=0.4, format='jpg', quality=2):
    """提取场景变化帧"""
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取视频信息
    info = get_video_info(video_path)
    total_frames = info['total_frames']
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 构建ffmpeg命令提取到临时目录
        temp_output_path = os.path.join(temp_dir, f'scene_%04d.{format}')
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'select=gt(scene\,{threshold})',
            '-vsync', 'vfr',
            '-q:v', str(quality),
            temp_output_path
        ]
        
        print(f"Running: {' '.join(cmd)}")
        subprocess.run(cmd)
        
        # 处理提取的帧
        process_extracted_frames(temp_dir, output_dir, total_frames, format)
    
    print(f"提取完成，文件保存在: {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='从视频中提取帧')
    parser.add_argument('video_path', help='输入视频文件路径')
    parser.add_argument('output_dir', help='输出目录路径')
    
    # 提取方式子命令
    subparsers = parser.add_subparsers(dest='mode', help='提取模式', required=True)
    
    # 1. 间隔n帧提取一张
    frame_parser = subparsers.add_parser('frame', help='按帧间隔提取')
    frame_parser.add_argument('-i', '--interval', type=int, required=True, help='帧间隔')
    
    # 2. 间隔n秒提取一张
    time_parser = subparsers.add_parser('time', help='按时间间隔提取')
    time_parser.add_argument('-i', '--interval', type=float, required=True, help='时间间隔(秒)')
    
    # 3. 总共提取m张
    total_parser = subparsers.add_parser('total', help='提取指定总数的帧')
    total_parser.add_argument('-n', '--number', type=int, required=True, help='总共提取的帧数')
    
    # 4. 提取关键帧
    key_parser = subparsers.add_parser('keyframe', help='只提取关键帧')
    
    # 5. 提取场景变化帧
    scene_parser = subparsers.add_parser('scene', help='提取场景变化帧')
    scene_parser.add_argument('-t', '--threshold', type=float, default=0.4, 
                              help='场景变化阈值(0.0-1.0)，越大表示要求变化越明显')
    
    # 所有模式通用参数
    for p in [frame_parser, time_parser, total_parser, key_parser, scene_parser]:
        p.add_argument('-f', '--format', type=str, default='jpg', 
                       choices=['jpg', 'png', 'bmp'], help='输出图片格式')
        p.add_argument('-q', '--quality', type=int, default=2, 
                       choices=range(1, 32), help='图片质量(1-31)，1最高')
    
    args = parser.parse_args()
    
    # 根据模式执行不同的提取方法
    if args.mode == 'frame':
        extract_by_frame_interval(args.video_path, args.output_dir, args.interval, 
                                 args.format, args.quality)
    elif args.mode == 'time':
        extract_by_time_interval(args.video_path, args.output_dir, args.interval, 
                                args.format, args.quality)
    elif args.mode == 'total':
        extract_total_frames(args.video_path, args.output_dir, args.number, 
                            args.format, args.quality)
    elif args.mode == 'keyframe':
        extract_keyframes(args.video_path, args.output_dir, args.format, args.quality)
    elif args.mode == 'scene':
        extract_scene_changes(args.video_path, args.output_dir, args.threshold, 
                             args.format, args.quality)


if __name__ == '__main__':
    main()