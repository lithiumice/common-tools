
# Paper Tools

## 环境配置

On Windows， using VsCode + Git Bash Terminal + MiniConda/MicroConda/Anaconda

Launch IPython:
```
uvx ipython
```

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
python tools/images/cut_white.py INPUT_IMG OUT_IMg
```

图片阵列
```
python tools/images/create_grid.py "aaa" -r 6 -c 8
```

图片爬虫
```
python "tools/banfo_biaoqingbao.py"
```
