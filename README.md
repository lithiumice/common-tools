
# 日常工具合集

## 环境配置

在Windows上使用：
- VsCode 
- Git Bash Terminal 
- MiniConda/Micromamba/Anaconda

## 运行

压缩文件夹
```
python tools/compress_folder.py
```

分割视频
```
python tools/pyscenedetect_clip.py INPUT_VID OUTPUT_DIR --threshold 6 --min-scene-len 10 --save-thumbnails
```

去除图片白边
```
python tools/images/cut_white.py INPUT_IMG OUT_IMG
```

图片阵列
```
python tools/images/create_grid.py INPUT_DIR -r 6 -c 8
```

图片爬虫
```
python "tools/banfo_biaoqingbao.py"
```

### Ubuntu 系统配置

先clone再运行
```
# 基本软件
sudo bash scripts/system_setting/install_ubuntu_software.sh

sudo bash scripts/system_setting/cuda_installer.sh

# 切换成清华源
sudo bash scripts/system_setting/switch_apt_source.sh
```


在不clone仓库的前提下使用bash脚本
```
bash <(curl -s https://raw.githubusercontent.com/lithiumice/common-tools/main/scripts/system_setting/install_ubuntu_software.sh)
```
