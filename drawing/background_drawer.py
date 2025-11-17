from PIL import Image, ImageDraw

def create_canvas(width=800, height=1000):
    """
    创建画布
    """
    # 创建白色背景
    img = Image.new('RGB', (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_header_background(draw, width, height=120):
    """
    绘制顶部背景（B站主题色 #FB7299）
    """
    draw.rectangle([(0, 0), (width, height)], fill=(251, 114, 153))
    return height

def draw_header_title(draw, width, fonts):
    """
    绘制标题
    """
    from .font_manager import safe_text_draw
    safe_text_draw(draw, (width//2, 30), "B站用户信息卡片", fill=(255, 255, 255), 
                  font=fonts['title'], anchor="mm")

def draw_statistics_background(draw, width, y_position, height=160):
    """
    绘制统计数据区域背景
    """
    # 统计数据背景
    stat_bg_color = (245, 245, 245)
    draw.rectangle([(30, y_position), (width-30, y_position+height)], 
                  fill=stat_bg_color, outline=(220, 220, 220), width=2)
    return y_position + height

def draw_footer(draw, width, height, fonts):
    """
    绘制底部信息
    """
    from .font_manager import safe_text_draw
    safe_text_draw(draw, (width//2, height-30), "来源 by 兆孽的B站用户查询", 
                  fill=(150, 150, 150), font=fonts['small'], anchor="mm")