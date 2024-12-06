import hydra
from omegaconf import DictConfig
import os
from pathlib import Path
import logging
from typing import List
import math
from tqdm import tqdm

import sys; sys.path.append(r"C:\Users\huali\Desktop\1_Work\10_daily_tools")

# 导入之前创建的video grid maker中的函数
from tools.videos.create_grid import (
    resize_videos,
    create_rows,
    create_final_grid,
    cleanup_temp_files
)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_video_files(directory: str) -> List[str]:
    """获取目录下所有视频文件"""
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'}
    video_files = []
    
    for file in Path(directory).rglob('*'):
        if file.suffix.lower() in video_extensions:
            video_files.append(str(file))
    
    return sorted(video_files)  # 排序确保处理顺序一致

def chunk_videos(video_files: List[str], chunk_size: int) -> List[List[str]]:
    """将视频文件列表分成固定大小的组"""
    return [video_files[i:i + chunk_size] for i in range(0, len(video_files), chunk_size)]

# @hydra.main(config_path="config", config_name="batch_grid", version_base=None)
# def process_directory(cfg: DictConfig) -> None:
    
def process_directory() -> None:
    """
    处理目录中的所有视频文件，每4个视频创建一个2x2网格
    配置文件应包含:
    - input_directory: 输入视频目录
    - output_directory: 输出视频目录
    - video_size: 
        - width: 每个视频的宽度
        - height: 每个视频的高度
    """
    from omegaconf import DictConfig
    cfg = DictConfig({
        "video_size": {
            "width": 640,
            "height": 480,
        },
        # "input_directory": r"c:\Users\huali\Desktop\1_Work\1_毕业论文\1_论文材料\2 MoCap Benchmark\8 100ways\100ways-combined_videos-20241121\3 combined_videos",
        # "output_directory": r"c:\Users\huali\Desktop\1_Work\1_毕业论文\1_论文材料\2 MoCap Benchmark\8 100ways\100ways-combined_videos-20241121\3_combined_videos_2x2grids"
        
        # "input_directory": r"c:\Users\huali\Desktop\1_Work\1_毕业论文\4_投稿记录\3 CVPR\3 intro视频\2_videos\2_DiffGen\Tiny-100STYLES",
        # "output_directory": r"c:\Users\huali\Desktop\1_Work\1_毕业论文\4_投稿记录\3 CVPR\3 intro视频\2_videos\2_DiffGen\Tiny-100STYLES-grid"
            
        "input_directory": r"c:\Users\huali\Desktop\1_Work\1_毕业论文\4_投稿记录\3 CVPR\3 intro视频\2_videos\2_DiffGen\Tiny-100STYLES+LOCO-3w",
        "output_directory": r"c:\Users\huali\Desktop\1_Work\1_毕业论文\4_投稿记录\3 CVPR\3 intro视频\2_videos\2_DiffGen\Tiny-100STYLES+LOCO-3w-grid"
            
    })
    try:
        # 创建输出目录
        os.makedirs(cfg.output_directory, exist_ok=True)
        
        # 获取所有视频文件
        video_files = get_video_files(cfg.input_directory)
        if not video_files:
            logger.error(f"在目录 {cfg.input_directory} 中未找到视频文件")
            return
        
        logger.info(f"找到 {len(video_files)} 个视频文件")
        
        # 将视频分组，每组4个
        video_groups = chunk_videos(video_files, 4)
        
        # 处理每组视频
        for i, group in enumerate(tqdm(video_groups, desc="处理视频组")):
            try:
                # 创建输出文件名
                output_name = f"grid_group_{i+1}.mp4"
                output_path = os.path.join(cfg.output_directory, output_name)
                
                # 确保临时目录干净
                cleanup_temp_files()
                os.makedirs("temp", exist_ok=True)
                
                # 调整视频大小
                resized_videos = resize_videos(
                    group,
                    cfg.video_size.width,
                    cfg.video_size.height
                )
                
                # 创建行视频
                row_videos = create_rows(resized_videos, cols=2, rows=2)
                
                # 创建最终网格
                create_final_grid(row_videos, output_path)
                
                logger.info(f"成功创建组 {i+1} 的视频网格: {output_path}")
                
            except Exception as e:
                logger.error(f"处理组 {i+1} 时出错: {str(e)}")
                continue
            
            finally:
                cleanup_temp_files()
        
        logger.info("所有视频组处理完成")
        
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        raise

if __name__ == "__main__":
    process_directory()