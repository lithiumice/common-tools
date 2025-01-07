

import os
import imageio
import numpy as np
from PIL import Image
from tqdm import tqdm
import re
import cv2



def process_videos_imageio(video_a_path, video_b_path, output_path, direction="hov"):
    # Open both videos
    reader_a = imageio.get_reader(video_a_path)
    reader_b = imageio.get_reader(video_b_path)

    # Get metadata
    meta_a = reader_a.get_meta_data()
    meta_b = reader_b.get_meta_data()

    fps_a = meta_a.get('fps', 30)
    duration_a = meta_a.get('duration', reader_a.count_frames() / fps_a)
    
    fps_b = meta_b.get('fps', 30)
    duration_b = meta_b.get('duration', reader_b.count_frames() / fps_b)

    # Create a writer for the output video
    writer = imageio.get_writer(output_path, fps=fps_a)

    # Process each frame of video A
    for i, frame_a in tqdm(enumerate(reader_a), desc=f"Processing {os.path.basename(video_a_path)}"):
        # Calculate the corresponding time in video B
        time_b = (i / fps_a) * (duration_b / duration_a)
        frame_index_b = int(time_b * fps_b)

        # Read the corresponding frame from video B
        reader_b.set_image_index(frame_index_b)
        frame_b = reader_b.get_next_data()
        
        if direction == "hov":
            # Resize frame B to match the height of frame A
            scale = frame_a.shape[0] / frame_b.shape[0]
            new_size = (int(frame_b.shape[1] * scale), int(frame_b.shape[0] * scale))
            frame_b_resized = Image.fromarray(frame_b).resize(new_size)
            frame_b_resized = np.array(frame_b_resized)
            combined_frame = np.concatenate((frame_b_resized, frame_a), axis=1)        
        else:
            # Vertical concatenation
            scale = frame_a.shape[1] / frame_b.shape[1]
            new_size = (int(frame_b.shape[1] * scale), int(frame_b.shape[0] * scale))
            frame_b_resized = Image.fromarray(frame_b).resize(new_size)
            frame_b_resized = np.array(frame_b_resized)
            combined_frame = np.concatenate((frame_b_resized, frame_a), axis=0)

        # Write the combined frame
        writer.append_data(combined_frame)

    # Close the readers and writer
    reader_a.close()
    reader_b.close()
    writer.close()


def get_video_info(video_path):
    """使用 OpenCV 获取视频信息"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Unable to open video: {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    cap.release()
    
    return {
        'fps': fps if fps > 0 else 30,  # 默认 30fps
        'frame_count': frame_count,
        'width': width,
        'height': height,
        'duration': frame_count / (fps if fps > 0 else 30)
    }

def process_videos(video_a_path, video_b_path, output_path, direction="hov"):
    try:
        # 获取视频信息
        info_a = get_video_info(video_a_path)
        info_b = get_video_info(video_b_path)
        
        # 使用 cv2.VideoCapture 读取视频
        cap_a = cv2.VideoCapture(video_a_path)
        cap_b = cv2.VideoCapture(video_b_path)
        
        if not cap_a.isOpened() or not cap_b.isOpened():
            raise ValueError("Unable to open one or both videos")

        # 设置输出视频参数
        fps = info_a['fps']
        if direction == "hov":
            # 水平拼接
            output_height = info_a['height']
            output_width = int(info_b['width'] * (info_a['height'] / info_b['height'])) + info_a['width']
        else:
            # 垂直拼接
            output_width = info_a['width']
            output_height = int(info_b['height'] * (info_a['width'] / info_b['width'])) + info_a['height']

        # 创建视频写入器
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))

        frame_count_a = int(info_a['frame_count'])
        
        # 处理每一帧
        with tqdm(total=frame_count_a, desc=f"Processing {os.path.basename(video_a_path)}") as pbar:
            for i in range(frame_count_a):
                # 读取视频 A 的帧
                ret_a, frame_a = cap_a.read()
                if not ret_a:
                    break

                # 计算视频 B 对应的帧索引
                frame_index_b = int(i * (info_b['frame_count'] / info_a['frame_count']))
                cap_b.set(cv2.CAP_PROP_POS_FRAMES, frame_index_b)
                ret_b, frame_b = cap_b.read()
                
                if not ret_b:
                    break

                if direction == "hov":
                    # 水平拼接
                    scale = frame_a.shape[0] / frame_b.shape[0]
                    new_width = int(frame_b.shape[1] * scale)
                    frame_b_resized = cv2.resize(frame_b, (new_width, frame_a.shape[0]))
                    combined_frame = np.concatenate((frame_b_resized, frame_a), axis=1)
                else:
                    # 垂直拼接
                    scale = frame_a.shape[1] / frame_b.shape[1]
                    new_height = int(frame_b.shape[0] * scale)
                    frame_b_resized = cv2.resize(frame_b, (frame_a.shape[1], new_height))
                    combined_frame = np.concatenate((frame_b_resized, frame_a), axis=0)

                out.write(combined_frame)
                pbar.update(1)

        # 释放资源
        cap_a.release()
        cap_b.release()
        out.release()

    except Exception as e:
        print(f"Error processing videos: {str(e)}")
        # 确保资源被释放
        try:
            cap_a.release()
            cap_b.release()
            out.release()
        except:
            pass
        raise





def batch_process_videos(base_dir_a, base_dir_b, output_dir, direction="hov"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get list of videos in directory A
    videos_a = [f for f in os.listdir(base_dir_a) if f.endswith('.webm')]
    
    # Process each video pair
    for video_a_name in videos_a:
        # Extract the VideoName part
        video_name = os.path.splitext(video_a_name)[0]
        
        # Construct the corresponding video B filename
        video_b_name = f"re-{video_name}_ID0_difTraj_raw_blender_high_blue.mp4"
        
        # Full paths
        video_a_path = os.path.join(base_dir_a, video_a_name)
        video_b_path = os.path.join(base_dir_b, video_b_name)
        
        # Skip if video B doesn't exist
        if not os.path.exists(video_b_path):
            print(f"Skipping {video_name}: Matching video not found in second directory")
            continue
        
        # Create output path
        output_path = os.path.join(output_dir, f"combined_{video_name}.mp4")
        
        print(f"\nProcessing pair: {video_name}")
        
        # try:
        #     process_videos(video_a_path, video_b_path, output_path, direction)
        #     print(f"Successfully processed: {video_name}")
        # except Exception as e:
        #     print(f"Error processing {video_name}: {str(e)}")
            
        process_videos(video_a_path, video_b_path, output_path, direction)

# Directory paths
base_dir_a = r"c:\Users\lithiumice\Desktop\1_Work\1_毕业论文\4_论文材料\3 构建数据集\2 Cherrypick-Animation\100 ways\3 Imitation\1 切片视频-分割处有问题"
base_dir_b = r"c:\Users\lithiumice\Desktop\1_Work\1_毕业论文\4_论文材料\3 构建数据集\2 Cherrypick-Animation\100 ways\3 Imitation\2 Blender渲染视频"
output_dir = r"c:\Users\lithiumice\Desktop\1_Work\1_毕业论文\4_论文材料\3 构建数据集\2 Cherrypick-Animation\100 ways\3 Imitation\combined_videos"

# Run the batch processing
batch_process_videos(base_dir_a, base_dir_b, output_dir, direction="hov")
