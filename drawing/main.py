import json
import os
from PIL import ImageDraw
from .font_manager import get_font_path, load_fonts
from .background_drawer import create_canvas, draw_header_background, draw_header_title, draw_statistics_background, draw_footer
from .user_info_drawer import draw_user_avatar, draw_user_basic_info, draw_user_details
from .image_drawer import load_user_images, draw_user_pendant, draw_user_images_grid
from .stats_drawer import draw_statistics_title, draw_statistics_cards

def draw_user_card(mid):
    """
    主绘制函数 - 绘制用户信息卡片
    """
    # 检查数据文件是否存在
    data_file = f"data/{mid}_data.json"
    if not os.path.exists(data_file):
        print(f"数据文件不存在: {data_file}")
        return False
    
    # 加载数据
    with open(data_file, 'r', encoding='utf-8') as f:
        user_data = json.load(f)
    
    # 创建画布
    width = 800
    height = 1000
    img, draw = create_canvas(width, height)
    
    # 加载字体
    font_path = get_font_path()
    fonts = load_fonts(font_path)
    fonts['path'] = font_path  # 保存字体路径供后续使用
    
    # 1. 绘制顶部背景和标题
    draw_header_background(draw, width)
    draw_header_title(draw, width, fonts)
    
    # 2. 绘制用户头像和基本信息
    draw_user_avatar(img, draw, mid)
    basic_info_end_y = draw_user_basic_info(draw, user_data, mid, fonts=fonts)
    
    # 3. 绘制用户详细信息
    details_end_y = draw_user_details(draw, user_data, basic_info_end_y, fonts=fonts)
    
    # 4. 绘制头像框
    img, has_pendant = draw_user_pendant(img, mid)
    if has_pendant:
        draw = ImageDraw.Draw(img)  # 重新创建draw对象
    
    # 5. 加载和绘制用户图片网格
    user_images = load_user_images(mid)
    if user_images:
        img, draw, images_height = draw_user_images_grid(img, user_images, details_end_y, width)
        images_end_y = details_end_y + images_height + 30
    else:
        images_end_y = details_end_y
    
    # 6. 绘制统计数据区域
    stats_bg_end_y = draw_statistics_background(draw, width, images_end_y + 30)
    draw_statistics_title(draw, width, images_end_y + 30, fonts)
    draw_statistics_cards(draw, user_data, width, images_end_y + 30, fonts)
    
    # 7. 绘制底部信息
    draw_footer(draw, width, height, fonts)
    
    # 确保输出目录存在
    os.makedirs("output", exist_ok=True)
    
    # 保存图片
    output_path = f"output/{mid}.png"
    img.save(output_path, "PNG")
    print(f"用户信息卡片已生成: {output_path}")
    
    return True