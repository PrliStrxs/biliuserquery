from .font_manager import safe_text_draw

def draw_statistics_title(draw, width, y_position, fonts):
    """
    绘制统计数据标题
    """
    safe_text_draw(draw, (width//2, y_position+15), "账号数据", fill=(0, 0, 0), 
                  font=fonts['normal'], anchor="mm")

def draw_statistics_cards(draw, user_data, width, start_y, fonts):
    """
    绘制统计数据卡片
    """
    # 统计数据（4个卡片）- 扩大卡片尺寸
    card_width = (width - 100) // 2  # 增加宽度
    card_height = 50  # 增加高度
    card_margin = 20
    
    # 不使用数字格式化，显示具体数字
    stats = [
        {"label": "粉丝数", "value": str(user_data.get('follower', 0)), "color": (251, 114, 153)},
        {"label": "关注数", "value": str(user_data.get('following', 0)), "color": (0, 160, 220)},
        {"label": "播放量", "value": str(user_data.get('view', 0)), "color": (255, 150, 0)},
        {"label": "获赞数", "value": str(user_data.get('likes', 0)), "color": (0, 180, 120)}
    ]
    
    for i, stat in enumerate(stats):
        row = i // 2
        col = i % 2
        
        x = 50 + col * (card_width + card_margin)
        y = start_y + 45 + row * (card_height + 15)
        
        # 绘制统计卡片 - 扩大卡片
        draw.rectangle([(x, y), (x+card_width, y+card_height)], 
                      fill=(255, 255, 255), outline=(230, 230, 230), width=1)
        
        # 绘制数值（居中）- 使用更小的字体确保数字不超出边界
        value = stat["value"]
        
        # 如果数字太长，自动缩小字体
        current_font_size = 16
        while current_font_size >= 10:
            try:
                if fonts.get('path'):
                    from PIL import ImageFont
                    current_font = ImageFont.truetype(fonts['path'], current_font_size)
                else:
                    current_font = fonts['stat']
                    
                value_bbox = draw.textbbox((0, 0), value, font=current_font)
                value_width = value_bbox[2] - value_bbox[0]
                
                if value_width <= card_width - 20:  # 留出边距
                    break
                current_font_size -= 1
            except:
                current_font = fonts['stat']
                break
        
        # 计算位置
        value_bbox = draw.textbbox((0, 0), value, font=current_font)
        value_width = value_bbox[2] - value_bbox[0]
        value_x = x + (card_width - value_width) // 2
        
        safe_text_draw(draw, (value_x, y+10), value, fill=stat["color"], font=current_font)
        
        # 绘制标签
        label_bbox = draw.textbbox((0, 0), stat["label"], font=fonts['normal'])
        label_width = label_bbox[2] - label_bbox[0]
        label_x = x + (card_width - label_width) // 2
        
        safe_text_draw(draw, (label_x, y+30), stat["label"], fill=(100, 100, 100), font=fonts['normal'])