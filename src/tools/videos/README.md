
## 将批量的可视化图片拼接成一个大图

```
input_directory="c:/Users/huali/Desktop/1_Work/1_毕业论文/1_论文材料/2 MoCap Benchmark/8 100ways/100ways-combined_videos-20241121/3 combined_videos" output_directory="c:/Users/huali/Desktop/1_Work/1_毕业论文/1_论文材料/2 MoCap Benchmark/8 100ways/100ways-combined_videos-20241121/3_combined_videos_2x2grids"
```



## 从单个演示视频提取图片并拼接成一个论文大图

7s, 30fps, 210 frames, 

```
python $(cygpath -u "tools/videos/video_to_motage.py") $(cygpath -u "c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/input-init-mica-mediepipe-deeplab.mp4") --interval 1 --cols 1 --title "SHOW Ablation Visualization"
```

## 用ffmpeg将一个视频按宽度等分分割

```
$(cygpath -u "xxx")
chmod +x split_video.sh
bash $(cygpath -u "tools/videos/split_equal_ffmpeg.sh") $(cygpath -u "c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/input-deeplab-tracking.mp4") 3 ./output

python $(cygpath -u "tools/videos/split_equal_ffmpeg.py") $(cygpath -u "c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/input-deeplab-tracking.mp4") 3 ./output

```

## 拼接视频

```
python tools/videos/create_grid.py input_videos=[r"c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/input-init-mica-mediepipe-deeplab.mp4",r"c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/split/SHOW结果.mp4"] grid.rows=1 grid.cols=2

python tools/videos/create_grid.py input_videos=['c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/input-init-mica-mediepipe-deeplab.mp4'] grid.rows=1 grid.cols=2


python tools/videos/create_grid.py grid.rows=1 grid.cols=2


python tools/videos/concat_h_ffmpeg.py c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/input-init-mica-mediepipe-deeplab.mp4 c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/split/SHOW结果.mp4 debug/tmp.mp4


```

## 抽取帧

下面是一个能够以多种方式从视频中抽取特定数量帧的Python脚本：

这个脚本提供了5种不同的方式从视频中提取帧：

1. **按帧间隔提取**：每隔n帧提取一张图片
2. **按时间间隔提取**：每隔n秒提取一张图片
3. **提取指定总数**：从整个视频中均匀提取m张图片
4. **提取关键帧**：只提取视频中的关键帧(I-frames)
5. **提取场景变化帧**：在场景变化处提取帧

### 使用方法

基本使用格式：
```
python tools/videos/extract_frames.py 视频路径 输出目录 提取模式 [模式参数] [通用参数]
```

#### 使用示例：

1. **按帧间隔提取**（每隔30帧提取一张）：
```
python tools/videos/extract_frames.py video.mp4 ./output_frames frame -i 30
```

2. **按时间间隔提取**（每隔5秒提取一张）：
```
python tools/videos/extract_frames.py video.mp4 ./output_frames time -i 5
```

3. **提取指定总数**（总共提取100张均匀分布的图片）：
```
python tools/videos/extract_frames.py video.mp4 ./output_frames total -n 100
python tools/videos/extract_frames.py c:/Users/huali/Desktop/1_Work/1_毕业论文/11-SHOW整理/论文材料/论文视频材料/整理/合并所有.mp4 ./debug/output_frames2 total -n 8
```

4. **提取关键帧**：
```
python tools/videos/extract_frames.py video.mp4 ./output_frames keyframe
```

5. **提取场景变化帧**（检测阈值0.3）：
```
python tools/videos/extract_frames.py video.mp4 ./output_frames scene -t 0.3
```

所有模式都支持以下通用参数：
- `-f, --format`：输出图片格式（jpg, png, bmp），默认为jpg
- `-q, --quality`：图片质量（1-31，1为最高质量），默认为2

这个脚本依赖于ffmpeg，请确保系统中已安装ffmpeg并可在命令行中访问。


```
# 每隔30帧提取一张，使用默认字体
python extract_frames.py video.mp4 ./output_frames frame -i 30

# 每隔5秒提取一张，指定使用宋体字体
python extract_frames.py video.mp4 ./output_frames time -i 5 --fontpath "C:/Windows/Fonts/simsun.ttc"

# 总共提取100张，使用PNG格式
python extract_frames.py video.mp4 ./output_frames total -n 100 -f png
```

