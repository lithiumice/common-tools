import requests
import os
from tqdm import tqdm
import time

def download_video(url, save_path, headers=None):
    """下载单个视频文件，支持断点续传"""
    if os.path.exists(save_path):
        # 获取已下载的文件大小
        temp_size = os.path.getsize(save_path)
        headers['Range'] = f'bytes={temp_size}-'
    else:
        temp_size = 0
    
    try:
        response = requests.get(url, headers=headers, stream=True)
        # 获取文件总大小
        total_size = int(response.headers.get('content-length', 0)) + temp_size
        
        mode = 'ab' if temp_size > 0 else 'wb'
        with open(save_path, mode) as f:
            with tqdm(total=total_size, initial=temp_size, unit='B', unit_scale=True, desc=os.path.basename(save_path)) as pbar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        return True
    except Exception as e:
        print(f"下载出错: {url}")
        print(f"错误信息: {str(e)}")
        return False

def main():
    # 基础URL
    base_url = "https://play.xfvod.pro/R/R-%E7%91%9E%E5%85%8B%E5%92%8C%E8%8E%AB%E8%92%82"
    
    # 设置请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': '*/*',
        'Accept-Encoding': 'identity;q=1, *;q=0',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive'
    }
    
    # 创建下载目录
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    # 下载所有季
    for season in range(1, 8):  # 1-7季
        season_dir = f"downloads/S{season}"
        if not os.path.exists(season_dir):
            os.makedirs(season_dir)
        
        # 每季的集数（假设每季20集，实际集数可能需要调整）
        for episode in range(1, 21):
            episode_num = str(episode).zfill(2)  # 01, 02, ..., 20
            video_url = f"{base_url}/S{season}/{episode_num}.mp4"
            save_path = f"{season_dir}/{episode_num}.mp4"
            
            # if os.path.exists(save_path):
            #     print(f"第{season}季 第{episode_num}集 已存在，跳过下载")
            #     continue
            
            print(f"\n开始下载 第{season}季 第{episode_num}集")
            success = download_video(video_url, save_path, headers.copy())
            
            if not success:
                print(f"第{season}季 第{episode_num}集 下载失败")
                
                break # 下载失败则跳出当前季的下载，一般说明没有更多的剧集了
            
            # 添加延时避免请求过快
            time.sleep(1)

if __name__ == "__main__":
    main()