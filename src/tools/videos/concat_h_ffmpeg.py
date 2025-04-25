import subprocess
import sys
import re

def get_video_height(video_path):
    """获取视频的高度"""
    cmd = ['ffprobe', '-v', 'error', '-select_streams', 'v', '-show_entries', 
           'stream=height', '-of', 'csv=p=0', video_path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return int(result.stdout.strip())

def horizontal_stack_videos(input_paths, output_path):
    """水平拼接多个视频"""
    # 获取所有视频的高度并找出最小值
    heights = [get_video_height(path) for path in input_paths]
    min_height = min(heights)
    
    # 构建ffmpeg命令
    ffmpeg_cmd = ['ffmpeg']
    filter_complex = ""
    
    # 添加所有输入文件
    for i, input_path in enumerate(input_paths):
        ffmpeg_cmd.extend(['-i', input_path])
        # 缩放视频到相同高度，保持宽高比，并确保尺寸是偶数
        filter_complex += f"[{i}:v]scale=-1:{min_height}:force_original_aspect_ratio=decrease,pad='iw+mod(iw,2)':'ih+mod(ih,2)'[v{i}]; "
    
    # 添加水平堆叠滤镜
    v_inputs = "".join(f"[v{i}]" for i in range(len(input_paths)))
    filter_complex += f"{v_inputs}hstack=inputs={len(input_paths)}[out]"
    
    # 完成命令
    ffmpeg_cmd.extend([
        '-filter_complex', filter_complex,
        '-map', '[out]',
        '-c:v', 'libx264',
        output_path,
        '-y'  # 覆盖现有文件
    ])
    
    # 执行命令
    print(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
    subprocess.run(ffmpeg_cmd)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py input1.mp4 input2.mp4 ... output.mp4")
        sys.exit(1)
    
    # 最后一个参数是输出路径，其余是输入路径
    output_path = sys.argv[-1]
    input_paths = sys.argv[1:-1]
    
    horizontal_stack_videos(input_paths, output_path)