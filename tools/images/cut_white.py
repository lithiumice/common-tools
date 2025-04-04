#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
脚本功能：批量裁剪图片周围的空白并保存到目标文件夹
支持格式：jpg, jpeg, png, gif, bmp, tiff
"""

import os
import argparse
from pathlib import Path
from PIL import Image, ImageChops


def trim_whitespace(image):
    """裁剪图片周围的空白区域"""
    # 转换图片模式为RGBA以处理透明背景
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # 获取非透明区域的边界
    bg = Image.new('RGBA', image.size, (255, 255, 255, 0))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    
    if bbox:
        # 裁剪图片
        cropped = image.crop(bbox)
        return cropped
    else:
        # 如果没有找到非空白区域，返回原图
        return image


def process_images(input_dir, output_dir, recursive=False, margin=0):
    """处理文件夹中的所有图片"""
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的图片格式
    img_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    
    # 获取所有图片文件路径
    if recursive:
        image_paths = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                file_path = Path(root) / file
                if file_path.suffix.lower() in img_extensions:
                    image_paths.append(file_path)
    else:
        image_paths = [
            Path(input_dir) / file for file in os.listdir(input_dir)
            if Path(input_dir, file).is_file() and Path(file).suffix.lower() in img_extensions
        ]
    
    # 处理每一张图片
    for img_path in image_paths:
        try:
            # 打开图片
            img = Image.open(img_path)
            
            # 裁剪空白
            cropped_img = trim_whitespace(img)
            
            # 添加边距
            if margin > 0:
                new_size = (cropped_img.width + 2 * margin, cropped_img.height + 2 * margin)
                new_img = Image.new(cropped_img.mode, new_size, (255, 255, 255, 0))
                new_img.paste(cropped_img, (margin, margin))
                cropped_img = new_img
            
            # 构造输出路径
            if recursive:
                rel_path = img_path.relative_to(input_dir)
                output_path = Path(output_dir) / rel_path
                os.makedirs(output_path.parent, exist_ok=True)
            else:
                output_path = Path(output_dir) / img_path.name
            
            # 保存裁剪后的图片
            cropped_img.save(output_path)
            print(f"处理完成: {img_path} -> {output_path}")
        
        except Exception as e:
            print(f"处理图片 {img_path} 时出错: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='批量裁剪图片周围的空白')
    parser.add_argument('input_dir', help='输入图片文件夹路径')
    parser.add_argument('output_dir', help='输出图片文件夹路径')
    parser.add_argument('-r', '--recursive', action='store_true', help='是否递归处理子文件夹')
    parser.add_argument('-m', '--margin', type=int, default=0, help='裁剪后添加的边距像素数')
    args = parser.parse_args()
    
    process_images(args.input_dir, args.output_dir, args.recursive, args.margin)
    print("所有图片处理完成!")


if __name__ == "__main__":
    main()