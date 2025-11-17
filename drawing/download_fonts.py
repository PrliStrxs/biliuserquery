import os
import requests

def download_chinese_fonts():
    """
    下载免费的中文字体作为备用
    """
    fonts_dir = "drawing/fonts"
    os.makedirs(fonts_dir, exist_ok=True)
    
    # 字体下载URL（使用开源字体）
    font_urls = {
        "simhei.ttf": "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJK-Regular.ttc",
        "wqy_microhei.ttc": "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJK-Regular.ttc"
    }
    
    downloaded_fonts = []
    
    for font_name, font_url in font_urls.items():
        font_path = os.path.join(fonts_dir, font_name)
        if not os.path.exists(font_path):
            print(f"正在下载字体: {font_name}")
            try:
                response = requests.get(font_url, timeout=30)
                if response.status_code == 200:
                    with open(font_path, 'wb') as f:
                        f.write(response.content)
                    downloaded_fonts.append(font_name)
                    print(f"字体下载完成: {font_name}")
                else:
                    print(f"字体下载失败: {font_name} (状态码: {response.status_code})")
            except Exception as e:
                print(f"字体下载错误: {font_name} - {e}")
        else:
            print(f"字体已存在: {font_name}")
    
    return downloaded_fonts

if __name__ == "__main__":
    download_chinese_fonts()