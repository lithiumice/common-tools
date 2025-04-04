
# Python Tools

## Env

On Windows， using VsCode + Git Bash Terminal + MiniConda/MicroConda/Anaconda

Conda
```
conda activate universe
```

Install
```
pip install -r requirements.txt
conda activate base
pip install scenedetect
pip install --upgrade scenedetect[opencv]
pip install hydra-core
```

Linux

```
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890
```

Windows

```
set https_proxy=http://127.0.0.1:7890
set http_proxy=http://127.0.0.1:7890
set all_proxy=socks5://127.0.0.1:7890
```




## Run

compress folder into zip file
```
python tools\compress_folder.py
```

segment video into clips
```
python tools\pyscenedetect_clip.py input_video output --threshold 6 --min-scene-len 10 --save-thumbnails
```

cut image white boarder
```
python tools/images/cut_white.py "c:\Users\huali\Desktop\1_Work\1_毕业论文\3_论文插图\数据集批量可视化\20240301 数据集 cherrypick Imitation Blender渲染图\Blender渲染图-Imitation" output/cut_white_0403
```

create paper image grid
```
python tools/images/create_grid.py "output/cut_white_0403" -r 6 -c 8
```

pictures scrawper
```
pip install bs4 requests
python "tools\banfo_biaoqingbao.py"
```
