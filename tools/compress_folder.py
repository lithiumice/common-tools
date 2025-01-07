import os
import zipfile
from datetime import datetime
from tqdm import tqdm
import shutil


def compress_folders(root_dir):
    # 获取所有子文件夹
    folders = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]
    
    # 按文件名长度排序
    folders.sort(key=len)
    
    for index, folder in tqdm(enumerate(folders, start=1)):
        folder_path = os.path.join(root_dir, folder)
        
        # 获取文件夹最后修改时间
        mod_time = os.path.getmtime(folder_path)
        mod_time_str = datetime.fromtimestamp(mod_time).strftime("%Y%m%d_%H%M%S")
        
        # 创建新的文件名
        new_folder_name = folder.replace(' ', '_')
        zip_filename = f"{index:03d}_{new_folder_name}_{mod_time_str}.zip"
        
        # 创建ZIP文件
        zip_path = os.path.join(root_dir, zip_filename)
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname)
        
        print(f"Compressed: {zip_filename}")
        # break
        
        shutil.rmtree(folder_path)
        
        print(f"Deleted: {folder}")
        
        

# 使用示例
root_directory = r"D:\6 嵌入式项目"
compress_folders(root_directory)
