from PIL import Image
import os
import glob
from pathlib import Path

def get_image_paths(base_path_a, track_num):
    
    # Path for image A
    path_a = os.path.join(base_path_a, "blender_difftraj_npzs_render_work", f"track_{track_num}", "rendered_frames", "high_blue_seq.png")
    
    # Path for image B folder
    path_b_folder = os.path.join(base_path_a, "extact_video_track", f"track_{track_num+1}_video")
    
    # Get all frames with interval 5
    all_frames = sorted(glob.glob(os.path.join(path_b_folder, "*.jpg")))
    
    # Select 8 frames with interval 30 (selecting every 6th frame from the interval-5 frames)
    selected_frames = all_frames[::6][:8]
    
    return path_a, selected_frames

def create_montage(base_path_a, track_num, output_path):
    path_a, b_image_paths = get_image_paths(base_path_a, track_num)
    
    # Read image A
    img_a = Image.open(path_a)
    
    # Read all B images and find the maximum dimensions
    b_images = [Image.open(path) for path in b_image_paths]
    # import ipdb; ipdb.set_trace()
    max_width = max(img.width for img in b_images)
    max_height = max(img.height for img in b_images)
    
    # Resize all B images to the maximum dimensions
    resized_b_images = [img.resize((max_width, max_height), Image.Resampling.LANCZOS) 
                       for img in b_images]
    
    # Create 2x4 montage of B images
    montage_width = max_width * 4
    montage_height = max_height * 2
    montage = Image.new('RGBA', (montage_width, montage_height))
    
    # Place B images in 2x4 grid
    for idx, img in enumerate(resized_b_images):
        row = idx // 4
        col = idx % 4
        x = col * max_width
        y = row * max_height
        montage.paste(img, (x, y))
    
    # # Resize image A to match the height of the montage
    # new_a_width = int(img_a.width * (montage_height / img_a.height))
    # img_a_resized = img_a.resize((new_a_width, montage_height), Image.Resampling.LANCZOS)
    
    # # Create final image (montage + image A)
    # final_width = montage_width + new_a_width
    # final_image = Image.new('RGBA', (final_width, montage_height))
    # final_image.paste(montage, (0, 0))
    # final_image.paste(img_a_resized, (montage_width, 0))
        
        
    # Resize montage to match the height of image A
    montage_scale = img_a.height / montage_height
    new_montage_width = int(montage_width * montage_scale)
    new_montage_height = img_a.height
    montage_resized = montage.resize((new_montage_width, new_montage_height), Image.Resampling.LANCZOS)

    # Create final image (montage + image A)
    final_width = new_montage_width + img_a.width
    final_image = Image.new('RGBA', (final_width, img_a.height))
    final_image.paste(montage_resized, (0, 0))
    final_image.paste(img_a, (new_montage_width, 0))


    # Save the final image
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"final_montage_track_{track_num}.png")
    final_image.save(output_file)
    print(f"Saved montage for track {track_num} to {output_file}")

def main():
    # Base paths
    base_path_a = r"c:\Users\lithiumice\Desktop\1_Work\1_毕业论文\4_论文材料\3 构建数据集\2 数据集插图\WuCYAXQBU18"
    # Specify output directory
    output_path = str(Path(base_path_a) / "montage_output")
    
    # Process tracks (you can modify the range based on how many tracks you have)
    for track_num in range(0, 56):  # Example: processing only track 0
        try:
            create_montage(base_path_a, track_num, output_path)
        except Exception as e:
            print(f"Error processing track {track_num}: {str(e)}")

if __name__ == "__main__":
    main()
    
    