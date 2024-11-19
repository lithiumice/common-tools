from scenedetect import detect, ContentDetector, split_video_ffmpeg
from scenedetect.scene_manager import save_images
import os
import argparse
from typing import Optional

def split_video_scenes(
    video_path: str,
    output_dir: str,
    threshold: float = 90.0,
    min_scene_len: int = 15,
    save_thumbnails: bool = False
) -> Optional[list]:
    """
    使用最高阈值分割视频场景并保存到指定目录
    
    参数:
        video_path: 输入视频路径
        output_dir: 输出目录路径
        threshold: 场景检测阈值 (0-100)
        min_scene_len: 最小场景长度(帧数)
        save_thumbnails: 是否保存场景缩略图
    
    返回:
        场景列表或None(如果发生错误)
    """
    try:
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 检测场景
        scenes = detect(
            video_path,
            ContentDetector(
                threshold=threshold,
                min_scene_len=min_scene_len
            )
        )
        
        if not scenes:
            print(f"没有检测到场景切换点: {video_path}")
            return None
            
        print(f"检测到 {len(scenes)} 个场景")
        
        # 分割视频
        split_video_ffmpeg(
            video_path,
            scenes,
            output_dir,
            show_progress=True
        )
        
        # # 保存缩略图
        # if save_thumbnails:
        #     thumb_dir = os.path.join(output_dir, "thumbnails")
        #     os.makedirs(thumb_dir, exist_ok=True)
        #     save_images(
        #         scenes,
        #         video_path,
        #         thumb_dir,
        #     )
            
        return scenes
        
    except Exception as e:
        print(f"处理视频时发生错误: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='视频场景分割工具')
    parser.add_argument('video_path', help='输入视频文件路径')
    parser.add_argument('output_dir', help='输出目录路径')
    parser.add_argument('--threshold', type=float, default=90.0, help='场景检测阈值 (0-100)')
    parser.add_argument('--min-scene-len', type=int, default=15, help='最小场景长度(帧数)')
    parser.add_argument('--save-thumbnails', action='store_true', help='保存场景缩略图')
    
    args = parser.parse_args()
    
    scenes = split_video_scenes(
        args.video_path,
        args.output_dir,
        args.threshold,
        args.min_scene_len,
        args.save_thumbnails
    )
    
    if scenes:
        print("视频场景分割完成!")

if __name__ == "__main__":
    main()