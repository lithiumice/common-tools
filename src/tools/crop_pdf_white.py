import fitz
import os

from pathlib import Path

def crop_pdf_margins(input_path, output_path, margin=0):
    """
    裁剪PDF文件的白边
    
    参数:
    input_path: 输入PDF文件路径
    output_path: 输出PDF文件路径
    margin: 保留的边距(像素)
    """
    if not output_path: 
        output_path = os.path.join(Path(input_path).parent, f"cropped_{Path(input_path).name}")
    
    # 打开PDF文件
    pdf_doc = fitz.open(input_path)
    
    # 创建新的PDF文档
    new_doc = fitz.open()
    
    # 遍历每一页
    for page_num in range(pdf_doc.page_count):
        # 获取当前页
        page = pdf_doc[page_num]
        
        # 获取页面上的所有内容区域
        content_bbox = page.get_text("blocks")
        
        if not content_bbox:
            # 如果没有检测到内容,复制原页面
            new_doc.insert_pdf(pdf_doc, from_page=page_num, to_page=page_num)
            continue
            
        # 裁剪的同时保留一定的边距
        # 计算内容的边界框
        x0 = min(block[0] for block in content_bbox) - margin
        y0 = min(block[1] for block in content_bbox) - margin
        x1 = max(block[2] for block in content_bbox) + margin
        y1 = max(block[3] for block in content_bbox) + margin
        
        # 确保边界在页面范围内
        x0 = max(0, x0)
        y0 = max(0, y0)
        x1 = min(page.rect.width, x1)
        y1 = min(page.rect.height, y1)
        
        # 创建新的页面
        new_page = new_doc.new_page(
            width=x1 - x0,
            height=y1 - y0
        )
        
        # 复制并裁剪内容
        new_page.show_pdf_page(
            new_page.rect,
            pdf_doc,
            page_num,
            clip=fitz.Rect(x0, y0, x1, y1)
        )
        
    # if os.path.exists(output_path):
    #     os.remove(output_path)
    
    # 保存新文档
    new_doc.save(output_path)
    
    # 关闭文档
    pdf_doc.close()
    new_doc.close()

def process_directory(input_dir, output_dir, margin=0):
    """
    处理整个目录中的PDF文件
    
    参数:
    input_dir: 输入目录路径
    output_dir: 输出目录路径
    margin: 保留的边距(像素)
    """
    # 创建输出目录(如果不存在)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 遍历目录中的所有PDF文件
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"cropped_{filename}")
            
            try:
                print(f"处理文件: {filename}")
                crop_pdf_margins(input_path, output_path, margin)
                print(f"完成处理: {filename}")
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")

# 使用示例
if __name__ == "__main__":
    # Install
    # pip install PyMuPDF
    
    # 处理单个文件
    crop_pdf_margins(r"c:\Users\huali\Desktop\1_Work\1_硕士毕业论文\0_论文材料\0_论文插图\3 动作生成\20241027_混合训练实验.pdf", None, margin=20)
    
    # 处理整个目录
    # process_directory("input_folder", "output_folder", margin=10)