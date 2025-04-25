
# Python Tools

## 激活环境

conda activate base

### Install

pip install --upgrade scenedetect[opencv]
pip install bs4 requests


### 设置Proxy

Linux

export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

Windows

set https_proxy=http://127.0.0.1:7890
set http_proxy=http://127.0.0.1:7890
set all_proxy=socks5://127.0.0.1:7890


## 实用脚本

压缩整理文件夹
python tools\compress_folder.py

临时测试裁剪视频
python tools\pyscenedetect_clip.py input_video output --threshold 6 --min-scene-len 10 --save-thumbnails

爬取表情包
python "tools\banfo_biaoqingbao.py"