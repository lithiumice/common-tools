import imageio
import numpy as np
from PIL import Image
from tqdm import tqdm

def process_videos(video_a_path, video_b_path, output_path):
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
    for i, frame_a in tqdm(enumerate(reader_a)):
        # Calculate the corresponding time in video B
        time_b = (i / fps_a) * (duration_b / duration_a)
        frame_index_b = int(time_b * fps_b)

        # Read the corresponding frame from video B
        reader_b.set_image_index(frame_index_b)
        frame_b = reader_b.get_next_data()
        
        # Resize frame B to match the height of frame A
        scale = frame_a.shape[0] / frame_b.shape[0]
        _new_s = (int(frame_b.shape[1] * scale), int(frame_b.shape[0] * scale))
        frame_b_resized = Image.fromarray(frame_b).resize(_new_s)
        frame_b_resized = np.array(frame_b_resized)
        combined_frame = np.concatenate((frame_b_resized, frame_a), axis=1)        
        
        
        # 纵向拼接
        # # Resize frame B to match the height of frame A
        # scale = frame_a.shape[1] / frame_b.shape[1]
        # _new_s = (int(frame_b.shape[1] * scale), int(frame_b.shape[0] * scale))
        # frame_b_resized = Image.fromarray(frame_b).resize(_new_s)
        # frame_b_resized = np.array(frame_b_resized)
        # combined_frame = np.concatenate((frame_b_resized, frame_a), axis=0)

        # Write the combined frame
        writer.append_data(combined_frame)

    # Close the readers and writer
    reader_a.close()
    reader_b.close()
    writer.close()

# Example usage
video_a_path = r"c:\Users\huali\Desktop\Porjects\毕业论文 材料\female-Kongfu-MoCap\Imitation结果.mp4"
video_b_path = r"c:\Users\huali\Desktop\Porjects\毕业论文 材料\female-Kongfu-MoCap\原始视频.mp4"
output_path = 'output/合并视频.mp4'

process_videos(video_a_path, video_b_path, output_path)