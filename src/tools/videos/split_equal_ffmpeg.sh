#!/bin/bash

# 函数：将视频按宽度等分分割
split_video_horizontally() {
    local input_file="$1"
    local parts="$2"
    local output_dir="$3"
    
    # 检查文件是否存在
    if [ ! -f "$input_file" ]; then
        echo "错误: 文件 '$input_file' 不存在"
        return 1
    fi
    
    # 检查目录是否存在，不存在则创建
    mkdir -p "$output_dir"
    
    # 获取视频信息
    local width=$(ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=p=0 "$input_file")
    local height=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of csv=p=0 "$input_file")
    
    if [ -z "$width" ] || [ -z "$height" ]; then
        echo "错误: 无法获取视频尺寸信息"
        return 1
    fi
    
    echo "视频尺寸: ${width}x${height}"
    
    # 计算每部分的宽度
    local part_width=$(echo "$width / $parts" | bc)
    echo "每部分宽度: $part_width"
    
    # 获取文件名（不含路径和扩展名）
    local filename=$(basename -- "$input_file")
    local name="${filename%.*}"
    
    # 分割视频
    for ((i=0; i<parts; i++)); do
        local start_pos=$(echo "$i * $part_width" | bc)
        local output_file="$output_dir/${name}_part$((i+1)).mp4"
        
        echo "处理部分 $((i+1))/$parts: 从位置 $start_pos 开始，宽度 $part_width"
        
        ffmpeg -i "$input_file" -vf "crop=$part_width:$height:$start_pos:0" -c:a copy "$output_file"
        
        if [ $? -eq 0 ]; then
            echo "成功创建: $output_file"
        else
            echo "错误: 无法创建 $output_file"
        fi
    done
    
    echo "完成! 所有 $parts 个部分已创建到 $output_dir 目录"
}

# 主程序
if [ $# -lt 2 ]; then
    echo "用法: $0 <输入视频文件> <分割数量> [输出目录]"
    echo "例如: $0 input.mp4 3 ./output"
    exit 1
fi

INPUT_FILE="$1"
PARTS="$2"
OUTPUT_DIR="${3:-./split_output}"

split_video_horizontally "$INPUT_FILE" "$PARTS" "$OUTPUT_DIR"