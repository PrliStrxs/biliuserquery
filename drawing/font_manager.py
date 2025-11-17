import os
import platform

def get_font_path():
    """
    获取可用的字体路径，优先使用系统中文字体
    兼容Windows和Linux系统
    """
    # 首先检查项目目录中的字体
    project_fonts = [
        "simhei.ttf",
        "./simhei.ttf",
        "fonts/simhei.ttf",
        "./fonts/simhei.ttf",
        "drawing/fonts/simhei.ttf",
        "drawing/fonts/wqy_microhei.ttc",
        "msyh.ttc",  # 微软雅黑
        "./msyh.ttc",
        "fonts/msyh.ttc",
        "./fonts/msyh.ttc",
        "drawing/fonts/msyh.ttc"
    ]
    
    for font_path in project_fonts:
        if os.path.exists(font_path):
            print(f"使用项目字体: {font_path}")
            return font_path
    
    # 根据系统类型查找系统字体
    system = platform.system()
    
    if system == "Windows":
        # Windows 系统字体路径
        windows_fonts = [
            "C:/Windows/Fonts/simhei.ttf",  # 黑体
            "C:/Windows/Fonts/msyh.ttc",    # 微软雅黑
            "C:/Windows/Fonts/msyh.ttf",    # 微软雅黑
            "C:/Windows/Fonts/simsun.ttc",  # 宋体
            "C:/Windows/Fonts/simkai.ttf",  # 楷体
        ]
        for font_path in windows_fonts:
            if os.path.exists(font_path):
                print(f"使用Windows系统字体: {font_path}")
                return font_path
    
    elif system == "Linux":
        # Linux 系统字体路径
        linux_fonts = [
            "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/arphic/uming.ttc",  # 文鼎明体
            "/usr/share/fonts/truetype/arphic/ukai.ttc",   # 文鼎楷体
        ]
        for font_path in linux_fonts:
            if os.path.exists(font_path):
                print(f"使用Linux系统字体: {font_path}")
                return font_path
    
    elif system == "Darwin":  # macOS
        mac_fonts = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/System/Library/Fonts/AppleGothic.ttf",
            "/Library/Fonts/Arial Unicode.ttf",
        ]
        for font_path in mac_fonts:
            if os.path.exists(font_path):
                print(f"使用macOS系统字体: {font_path}")
                return font_path
    
    print("警告: 未找到中文字体，将使用默认字体（可能不支持中文）")
    return None

def load_fonts(font_path):
    """
    加载各种大小的字体
    """
    from PIL import ImageFont
    
    try:
        if font_path:
            title_font = ImageFont.truetype(font_path, 28)  # 标题字体
            name_font = ImageFont.truetype(font_path, 24)   # 名字字体
            normal_font = ImageFont.truetype(font_path, 18) # 正文字体
            stat_font = ImageFont.truetype(font_path, 16)   # 统计数据字体
            small_font = ImageFont.truetype(font_path, 16)  # 小字体
        else:
            # 如果找不到字体，使用默认字体
            title_font = ImageFont.load_default()
            name_font = ImageFont.load_default()
            normal_font = ImageFont.load_default()
            stat_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            print("使用默认字体，中文可能显示为方块")
        
        return {
            'title': title_font,
            'name': name_font,
            'normal': normal_font,
            'stat': stat_font,
            'small': small_font
        }
    except Exception as e:
        print(f"加载字体失败: {e}")
        # 使用默认字体
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
        stat_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        print("使用默认字体，中文可能显示为方块")
        
        return {
            'title': title_font,
            'name': name_font,
            'normal': normal_font,
            'stat': stat_font,
            'small': small_font
        }

def safe_text_draw(draw, position, text, font, fill, anchor=None):
    """
    安全的文本绘制函数，处理编码问题
    """
    try:
        if anchor:
            draw.text(position, text, fill=fill, font=font, anchor=anchor)
        else:
            draw.text(position, text, fill=fill, font=font)
        return True
    except UnicodeEncodeError:
        # 如果遇到编码问题，尝试使用不同的编码
        try:
            # 尝试UTF-8编码
            text_encoded = text.encode('utf-8').decode('utf-8')
            if anchor:
                draw.text(position, text_encoded, fill=fill, font=font, anchor=anchor)
            else:
                draw.text(position, text_encoded, fill=fill, font=font)
            return True
        except:
            # 如果还是失败，使用替换字符
            text_safe = text.encode('utf-8', 'replace').decode('utf-8')
            if anchor:
                draw.text(position, text_safe, fill=fill, font=font, anchor=anchor)
            else:
                draw.text(position, text_safe, fill=fill, font=font)
            return True
    except Exception as e:
        print(f"绘制文本失败: {e}")
        return False