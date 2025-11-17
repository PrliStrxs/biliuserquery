import os
import textwrap
from PIL import Image, ImageDraw
from .font_manager import safe_text_draw, get_font_path, load_fonts

def draw_user_avatar(img, draw, mid, x=50, y=150, size=80):
    """
    绘制用户头像
    """
    avatar_path = None
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        if os.path.exists(f"img/{mid}_face{ext}"):
            avatar_path = f"img/{mid}_face{ext}"
            break
    
    if avatar_path:
        try:
            avatar = Image.open(avatar_path)
            avatar = avatar.resize((size, size), Image.LANCZOS)
            
            # 创建圆形遮罩
            mask = Image.new('L', (size, size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse([(0, 0), (size, size)], fill=255)
            
            # 应用圆形遮罩
            avatar_circle = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            avatar_circle.paste(avatar, (0, 0), mask)
            
            # 绘制头像
            img.paste(avatar_circle, (x, y), avatar_circle)
            return True
        except Exception as e:
            print(f"加载头像失败: {e}")
    
    # 绘制默认头像
    draw.ellipse([(x, y), (x+size, y+size)], fill=(200, 200, 200))
    return False

def draw_user_basic_info(draw, user_data, mid, x=150, y=160, fonts=None):
    """
    绘制用户基本信息（用户名、UID、等级、会员）
    """
    if fonts is None:
        from .font_manager import load_fonts
        font_path = get_font_path()
        fonts = load_fonts(font_path)
    
    name = user_data.get('name', '未知用户')
    
    # 处理长用户名 - 使用textwrap进行换行
    name_lines = textwrap.wrap(name, width=15)  # 每行最多15个字符
    name_lines = name_lines[:2]  # 最多显示2行
    
    name_y = y
    for i, line in enumerate(name_lines):
        safe_text_draw(draw, (x, name_y + i*25), line, fill=(0, 0, 0), font=fonts['name'])
    
    safe_text_draw(draw, (x, name_y + len(name_lines)*25), f"UID: {mid}", 
                  fill=(100, 100, 100), font=fonts['normal'])
    
    # 绘制等级和会员信息（分两行显示）
    level = user_data.get('level', 0)
    vip_text = user_data.get('vip_text', '')
    
    level_text = f"等级: Lv.{level}"
    safe_text_draw(draw, (x, name_y + len(name_lines)*25 + 30), level_text, 
                  fill=(251, 114, 153), font=fonts['normal'])
    
    if vip_text:
        vip_text_display = f"会员: {vip_text}"
        safe_text_draw(draw, (x, name_y + len(name_lines)*25 + 55), vip_text_display, 
                      fill=(251, 114, 153), font=fonts['normal'])
    
    # 返回基本信息区域结束的Y坐标
    return name_y + len(name_lines)*25 + 85

def draw_user_details(draw, user_data, start_y, x=50, fonts=None):
    """
    绘制用户详细信息（性别、签名、头衔、认证、勋章）
    """
    if fonts is None:
        from .font_manager import load_fonts
        font_path = get_font_path()
        fonts = load_fonts(font_path)
    
    y_offset = start_y
    
    # 性别
    sex = user_data.get('sex', '未知')
    safe_text_draw(draw, (x, y_offset), f"性别: {sex}", fill=(0, 0, 0), font=fonts['normal'])
    
    # 签名（处理长签名）
    sign = user_data.get('sign', '')
    if not sign:
        sign = "这个用户还没有签名~"
    
    # 添加"签名："前缀
    sign_with_prefix = f"签名: {sign}"
    
    # 使用textwrap处理长签名
    max_chars_per_line = 40  # 每行最多字符数
    sign_lines = textwrap.wrap(sign_with_prefix, width=max_chars_per_line)
    sign_lines = sign_lines[:3]  # 最多显示3行
    
    for i, line in enumerate(sign_lines):
        safe_text_draw(draw, (x, y_offset + 30 + i*25), line, fill=(100, 100, 100), font=fonts['normal'])
    
    # 更新y_offset位置
    y_offset += 30 + len(sign_lines)*25 + 10
    
    # 绘制头衔和认证信息
    official_title = user_data.get('official_title', '')
    if official_title:
        # 处理头衔显示 - 使用淡金黄色 (255, 215, 0)
        title_with_prefix = f"头衔: {official_title}"
        title_lines = textwrap.wrap(title_with_prefix, width=max_chars_per_line)
        title_lines = title_lines[:2]  # 最多显示2行
        
        for i, line in enumerate(title_lines):
            safe_text_draw(draw, (x, y_offset + i*25), line, fill=(255, 215, 0), font=fonts['normal'])
        
        y_offset += len(title_lines)*25
    
    attestation_title = user_data.get('attestation_title', '')
    if attestation_title:
        # 处理认证信息显示 - 使用淡蓝色 (100, 150, 255)
        attestation_with_prefix = f"认证: {attestation_title}"
        attestation_lines = textwrap.wrap(attestation_with_prefix, width=max_chars_per_line)
        attestation_lines = attestation_lines[:2]  # 最多显示2行
        
        for i, line in enumerate(attestation_lines):
            safe_text_draw(draw, (x, y_offset + i*25), line, fill=(100, 150, 255), font=fonts['normal'])
        
        y_offset += len(attestation_lines)*25
    
    # 绘制勋章信息
    nameplate_name = user_data.get('nameplate_name', '')
    if nameplate_name:
        safe_text_draw(draw, (x, y_offset), f"勋章: {nameplate_name}", fill=(0, 0, 0), font=fonts['normal'])
        y_offset += 25
    
    return y_offset