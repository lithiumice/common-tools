
# Tools

## Env
export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890

### Install
pip install scenedetect
pip install --upgrade scenedetect[opencv]

## Run
python tools\compress_folder.py

python tools\pyscenedetect_clip.py input_video output \
    --threshold 6 --min-scene-len 10 --save-thumbnails

