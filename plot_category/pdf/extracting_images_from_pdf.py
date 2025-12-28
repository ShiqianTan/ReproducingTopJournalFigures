import fitz  # 即PyMuPDF
import os

def extract_images_from_pdf(pdf_path, output_folder="extracted_pdf_images"):
    """
    从电子版PDF中提取所有内嵌图片
    :param pdf_path: PDF文件的路径（相对路径或绝对路径）
    :param output_folder: 提取图片的保存文件夹
    """
    # 1. 创建输出文件夹（若不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"创建输出文件夹：{output_folder}")

    # 2. 打开PDF文档
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"打开PDF失败：{e}")
        return

    # 3. 遍历PDF的每一页，提取图片
    image_count = 0  # 统计提取的图片总数
    for page_num in range(len(doc)):
        page = doc[page_num]  # 获取当前页
        image_list = page.get_images(full=True)  # 获取当前页所有图片（full=True返回完整图片信息）

        if not image_list:
            print(f"第 {page_num+1} 页无内嵌图片")
            continue

        print(f"第 {page_num+1} 页发现 {len(image_list)} 张图片，开始提取...")

        # 4. 遍历当前页的所有图片，保存到本地
        for img_index, img_info in enumerate(image_list):
            # img_info是元组，其中第0个元素是图片xref（唯一标识），第2个元素是图片宽度，第3个元素是图片高度
            xref = img_info[0]
            img_width = img_info[2]
            img_height = img_info[3]

            # 提取图片本身
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]  # 获取图片二进制数据
            image_ext = base_image["ext"]  # 获取图片格式（png/jpg等）

            # 5. 构造图片保存路径（按「页码-图片索引.格式」命名，方便追溯）
            image_filename = f"page_{page_num+1}_img_{img_index+1}.{image_ext}"
            image_save_path = os.path.join(output_folder, image_filename)

            # 6. 写入文件保存图片
            with open(image_save_path, "wb") as f:
                f.write(image_bytes)

            image_count += 1
            print(f"  已保存：{image_filename}（尺寸：{img_width}x{img_height}）")

    # 7. 操作完成提示
    doc.close()
    print(f"\n提取完成！共提取 {image_count} 张图片，保存至：{os.path.abspath(output_folder)}")

# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 替换为你的电子版PDF文件路径（相对路径或绝对路径）
    YOUR_PDF_FILE = "Data Visualization in R and Python (Marco Cremonini) (Z-Library).pdf"
    
    # 调用函数提取图片
    extract_images_from_pdf(YOUR_PDF_FILE)


  # sorting_images_by_page.py
  import os
  import json
  import re
  
  img_dir = "./extracted_pdf_images"
  
  pattern = re.compile(r"page_(\d+)_img_(\d+)\.png$", re.IGNORECASE)
  
  def sort_key(fname: str):
      m = pattern.search(fname)
      if m:
          page = int(m.group(1))
          idx  = int(m.group(2))
          return (page, idx)
      # 不符合命名规则的放到最后，并按文件名排序
      return (float("inf"), float("inf"), fname)
  
  images = sorted(
      [f for f in os.listdir(img_dir) if f.lower().endswith(".png")],
      key=sort_key
  )
  print(images)
