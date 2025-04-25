import hydra
from omegaconf import DictConfig
import subprocess
import os
from typing import List, Tuple
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@hydra.main(config_path="conf", config_name="create_grid", version_base=None)
def create_video_grid(cfg: DictConfig) -> None:
    """
    使用FFmpeg创建视频网格
    配置文件应包含:
    - input_videos: 输入视频路径列表
    - output_path: 输出视频路径
    - grid: 
        - rows: 行数
        - cols: 列数
    - video_size: 
        - width: 每个视频的宽度
        - height: 每个视频的高度
    """
    try:
        # 验证输入参数
        if len(cfg.input_videos) > cfg.grid.rows * cfg.grid.cols:
            raise ValueError("输入视频数量超过网格容量")

        # 创建临时工作目录
        os.makedirs("temp", exist_ok=True)

        # 第1步: 调整所有视频的大小
        resized_videos = resize_videos(
            cfg.input_videos,
            cfg.video_size.width,
            cfg.video_size.height
        )

        # 第2步: 创建每一行的视频
        row_videos = create_rows(
            resized_videos,
            cfg.grid.cols,
            cfg.grid.rows
        )

        # 第3步: 合并所有行
        create_final_grid(row_videos, cfg.output_path)

        logger.info(f"视频网格已成功创建: {cfg.output_path}")

    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        raise

    finally:
        # 清理临时文件
        cleanup_temp_files()

def resize_videos(video_paths: List[str], width: int, height: int) -> List[str]:
    """调整所有输入视频的大小"""
    resized_videos = []
    for idx, video in enumerate(video_paths):
        output_path = f"temp/resized_{idx}.mp4"
        cmd = [
            "ffmpeg", "-y", "-i", video,
            "-vf", f"scale={width}:{height}",
            "-c:v", "libx264",
            "-c:a", "aac",
            output_path
        ]
        subprocess.run(cmd, check=True)
        resized_videos.append(output_path)
    return resized_videos

def create_rows(videos: List[str], cols: int, rows: int) -> List[str]:
    """创建每一行的视频"""
    row_videos = []
    for row in range(rows):
        start_idx = row * cols
        end_idx = min(start_idx + cols, len(videos))
        row_videos_subset = videos[start_idx:end_idx]
        
        # 如果这一行视频数量不足，用黑色视频填充
        while len(row_videos_subset) < cols:
            black_video = create_black_video(
                videos[0],
                f"temp/black_{row}_{len(row_videos_subset)}.mp4"
            )
            row_videos_subset.append(black_video)
        
        output_path = f"temp/row_{row}.mp4"
        create_row(row_videos_subset, output_path)
        row_videos.append(output_path)
    
    return row_videos

def create_row(videos: List[str], output_path: str) -> None:
    """使用FFmpeg的hstack过滤器横向合并视频"""
    filter_complex = "[0:v]"
    for i in range(1, len(videos)):
        filter_complex += f"[{i}:v]"
    filter_complex += f"hstack=inputs={len(videos)}"
    
    cmd = ["ffmpeg", "-y"]
    for video in videos:
        cmd.extend(["-i", video])
    cmd.extend([
        "-filter_complex", filter_complex,
        "-c:v", "libx264",
        output_path
    ])
    subprocess.run(cmd, check=True)

def create_final_grid(row_videos: List[str], output_path: str) -> None:
    """使用FFmpeg的vstack过滤器纵向合并所有行"""
    filter_complex = "[0:v]"
    for i in range(1, len(row_videos)):
        filter_complex += f"[{i}:v]"
    filter_complex += f"vstack=inputs={len(row_videos)}"
    
    cmd = ["ffmpeg", "-y"]
    for video in row_videos:
        cmd.extend(["-i", video])
    cmd.extend([
        "-filter_complex", filter_complex,
        "-c:v", "libx264",
        output_path
    ])
    subprocess.run(cmd, check=True)

def create_black_video(template_video: str, output_path: str) -> str:
    """创建一个黑色的填充视频"""
    cmd = [
        "ffmpeg", "-y",
        "-i", template_video,
        "-vf", "geq=0:128:128",  # 创建黑色帧
        "-c:v", "libx264",
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path

def cleanup_temp_files() -> None:
    """清理临时文件"""
    if os.path.exists("temp"):
        for file in os.listdir("temp"):
            os.remove(os.path.join("temp", file))
        os.rmdir("temp")

if __name__ == "__main__":
    create_video_grid()