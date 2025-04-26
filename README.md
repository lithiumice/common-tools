
# Paper Tools

## ENV

On Windows， using VsCode + Git Bash Terminal + MiniConda/MicroConda/Anaconda

Launch IPython:
```
uvx ipython
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
python tools/images/cut_white.py "aaa" bbb
```

create paper image grid
```
python tools/images/create_grid.py "aaa" -r 6 -c 8
```

pictures scrawper
```
pip install bs4 requests
python "tools\banfo_biaoqingbao.py"
```

```
cd src/sync_code/RLM/audio_streamer/
python audio_streamer.py
```
