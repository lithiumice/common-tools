import os
from PIL import Image
import logging
from pathlib import Path

class ImageCleaner:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.corrupted_files = []
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        
        # 设置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('image_cleaner.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def is_image_corrupted(self, file_path):
        """检查图片是否损坏"""
        try:
            with Image.open(file_path) as img:
                # 尝试加载图片数据
                img.verify()
                # # 额外验证：尝试获取图片的基本信息
                # img.load()
                # img.getdata()
            return False
        except Exception as e:
            self.logger.warning(f"文件损坏: {file_path} - 错误: {str(e)}")
            return True

    def scan_directory(self):
        """扫描目录中的所有图片文件"""
        self.logger.info(f"开始扫描目录: {self.directory}")
        
        try:
            for file_path in self.directory.rglob("*"):
                if file_path.suffix.lower() in self.supported_formats:
                    if self.is_image_corrupted(file_path):
                        self.corrupted_files.append(file_path)
        
        except Exception as e:
            self.logger.error(f"扫描过程中发生错误: {str(e)}")
            raise

        self.logger.info(f"扫描完成. 发现 {len(self.corrupted_files)} 个损坏的文件")

    def remove_corrupted_files(self, auto_remove=False):
        """删除损坏的文件"""
        if not self.corrupted_files:
            self.logger.info("没有发现损坏的文件")
            return

        self.logger.info("发现以下损坏的文件:")
        for file_path in self.corrupted_files:
            self.logger.info(f"- {file_path}")

        if auto_remove or input("\n是否删除这些文件? (y/n): ").lower() == 'y':
            for file_path in self.corrupted_files:
                try:
                    file_path.unlink()
                    self.logger.info(f"已删除: {file_path}")
                except Exception as e:
                    self.logger.error(f"删除文件失败 {file_path}: {str(e)}")
        else:
            self.logger.info("操作已取消")

def main():
    # 获取用户输入的目录路径
    directory = input("请输入要扫描的目录路径: ").strip()
    
    if not os.path.exists(directory):
        print("错误: 目录不存在!")
        return

    try:
        cleaner = ImageCleaner(directory)
        cleaner.scan_directory()
        cleaner.remove_corrupted_files()
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()