from pathlib import Path
import os

from pdf2image import convert_from_path

# PDF 文件的路径
pdf_path = "D:\\kaiyuan\\pdf2image\\testpdf.pdf"

page_indexes = [1, 3, 5]

output_folder = "D:\\kaiyuan\\pdf2image\\output_images"
Path(output_folder).mkdir(parents=True, exist_ok=True)

# 调用 convert_from_path 函数，将所有页面转换为图片
images = convert_from_path(
    pdf_path=pdf_path,
    dpi=300,  # 设置 DPI 分辨率
    output_folder=None,  # 不保存到文件夹，直接在内存中处理
    fmt="png",  # 输出格式为 PNG
)

for idx, img in enumerate(images):
    if (idx + 1) in page_indexes:
        img.save(os.path.join(output_folder, f"page_{idx + 1}.png"))
        img.close()

print(f"所有指定的图片已成功保存到 {output_folder}")
