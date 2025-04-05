import os
import sys
import subprocess
import json
import math
from pathlib import Path

def get_video_info(input_file):
    """获取视频的宽度和高度信息"""
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-select_streams', 'v:0', 
        '-show_entries', 'stream=width,height', 
        '-of', 'json', 
        input_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        info = json.loads(result.stdout)
        width = info['streams'][0]['width']
        height = info['streams'][0]['height']
        return width, height
    except subprocess.CalledProcessError as e:
        print(f"错误: 无法获取视频信息: {e}")
        print(f"ffprobe 输出: {e.stderr}")
        sys.exit(1)
    except (json.JSONDecodeError, KeyError) as e:
        print(f"错误: 解析视频信息失败: {e}")
        sys.exit(1)

def split_video_horizontally(input_file, parts, output_dir=None):
    """将视频按宽度等分分割"""
    # 检查输入文件是否存在
    if not os.path.isfile(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        return False

    # 设置输出目录
    if output_dir is None:
        output_dir = './split_output'
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取视频信息
    width, height = get_video_info(input_file)
    print(f"视频尺寸: {width}x{height}")
    
    # 计算每部分的宽度
    part_width = math.floor(width / parts)
    print(f"每部分宽度: {part_width}")
    
    # 获取文件名（不含路径和扩展名）
    file_path = Path(input_file)
    filename = file_path.stem
    
    # 分割视频
    for i in range(parts):
        start_pos = i * part_width
        output_file = os.path.join(output_dir, f"{filename}_part{i+1}.mp4")
        
        print(f"处理部分 {i+1}/{parts}: 从位置 {start_pos} 开始，宽度 {part_width}")
        
        cmd = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f"crop={part_width}:{height}:{start_pos}:0",
            '-c:a', 'copy',
            output_file
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"成功创建: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"错误: 无法创建 {output_file}")
            print(f"FFmpeg 错误: {e.stderr.decode()}")
            continue
    
    print(f"完成! 所有 {parts} 个部分已创建到 {output_dir} 目录")
    return True

def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) < 3:
        print(f"用法: {sys.argv[0]} <输入视频文件> <分割数量> [输出目录]")
        print(f"例如: {sys.argv[0]} input.mp4 3 ./output")
        return 1
    
    input_file = sys.argv[1]
    
    try:
        parts = int(sys.argv[2])
        if parts <= 0:
            raise ValueError("分割数量必须大于0")
    except ValueError:
        print(f"错误: 分割数量必须是正整数")
        return 1
    
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None
    
    # 执行视频分割
    success = split_video_horizontally(input_file, parts, output_dir)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())