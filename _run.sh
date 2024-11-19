export https_proxy=http://127.0.0.1:7890
export http_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7890



pip install scenedetect
pip install --upgrade scenedetect[opencv]



python 2_T_pyscenedetect_clip.py "c:\Users\lithiumice\Desktop\1_Work\1_硕士毕业论文\4_论文材料\3 构建数据集\1 动画师演示动捕可视化\50 walks\50_type_walk.webm" \
"c:\Users\lithiumice\Desktop\1_Work\1_硕士毕业论文\4_论文材料\3 构建数据集\1 动画师演示动捕可视化\50 walks\1 切片视频 thres6" \
--threshold 6 --min-scene-len 10 --save-thumbnails

ffmpeg -i "c:\Users\lithiumice\Desktop\1_Work\1_硕士毕业论文\4_论文材料\3 构建数据集\1 动画师演示动捕可视化\100 ways\1 切片视频 thres6\0 原始视频-Scene-039.mp4" \
 "c:\Users\lithiumice\Desktop\1_Work\1_硕士毕业论文\4_论文材料\3 构建数据集\1 动画师演示动捕可视化\100 ways\1 切片视频 thres6\0 原始视频-Scene-039 pngs\Scene-039-%04d.png"


c:\Users\lithiumice\Desktop\1_Work\1_毕业论文\4_论文材料\3 构建数据集\2 数据集插图\WuCYAXQBU18\blender_difftraj_npzs_render_work\track_0\rendered_frames\high_blue_seq.png

c:\Users\lithiumice\Desktop\1_Work\1_毕业论文\4_论文材料\3 构建数据集\2 数据集插图\WuCYAXQBU18\extact_track_image\track_1_video.jpg

c:\Users\lithiumice\Desktop\1_Work\1_毕业论文\4_论文材料\3 构建数据集\2 数据集插图\WuCYAXQBU18\extact_video_track\track_1_video\0000.jpg

