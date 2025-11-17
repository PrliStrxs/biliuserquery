import os
from PIL import Image

def load_user_images(mid):
    """
    加载用户的所有图片（头像、头像框、勋章）
    """
    images = {}
    
    # 加载头像
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        if os.path.exists(f"img/{mid}_face{ext}"):
            try:
                avatar = Image.open(f"img/{mid}_face{ext}")
                if avatar.mode != 'RGBA':
                    avatar = avatar.convert('RGBA')
                avatar = avatar.resize((100, 100), Image.LANCZOS)
                images['avatar'] = avatar
                break
            except Exception as e:
                print(f"加载头像失败: {e}")
    
    # 加载头像框
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        if os.path.exists(f"img/{mid}_pendant{ext}"):
            try:
                pendant = Image.open(f"img/{mid}_pendant{ext}")
                if pendant.mode != 'RGBA':
                    pendant = pendant.convert('RGBA')
                pendant = pendant.resize((100, 100), Image.LANCZOS)
                images['pendant'] = pendant
                break
            except Exception as e:
                print(f"加载头像框失败: {e}")
    
    # 加载勋章
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        if os.path.exists(f"img/{mid}_nameplate{ext}"):
            try:
                nameplate = Image.open(f"img/{mid}_nameplate{ext}")
                if nameplate.mode != 'RGBA':
                    nameplate = nameplate.convert('RGBA')
                nameplate = nameplate.resize((100, 100), Image.LANCZOS)
                images['nameplate'] = nameplate
                break
            except Exception as e:
                print(f"加载勋章失败: {e}")
    
    return images

def draw_user_pendant(img, mid, avatar_x=50, avatar_y=150, avatar_size=80):
    """
    绘制用户头像框
    """
    pendant_path = None
    for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        if os.path.exists(f"img/{mid}_pendant{ext}"):
            pendant_path = f"img/{mid}_pendant{ext}"
            break
    
    if pendant_path:
        try:
            pendant = Image.open(pendant_path)
            # 确保头像框是RGBA模式以保留透明度
            if pendant.mode != 'RGBA':
                pendant = pendant.convert('RGBA')
                
            # 调整头像框大小，使其比头像稍大
            pendant_size = avatar_size + 40  # 增加更多空间
            pendant = pendant.resize((pendant_size, pendant_size), Image.LANCZOS)
            
            # 计算头像框位置，使其居中于头像
            pendant_x = avatar_x - (pendant_size - avatar_size) // 2
            pendant_y = avatar_y - (pendant_size - avatar_size) // 2
            
            # 创建临时图像用于合成
            temp_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
            temp_img.paste(pendant, (pendant_x, pendant_y), pendant)
            
            # 将头像框合成到主图像
            img = Image.alpha_composite(img.convert('RGBA'), temp_img).convert('RGB')
            
            return img, True
            
        except Exception as e:
            print(f"加载头像框失败: {e}")
    
    return img, False

def draw_user_images_grid(img, images, start_y, width=800):
    """
    在网格中绘制用户图片
    """
    from PIL import ImageDraw
    
    draw = ImageDraw.Draw(img)
    
    # 按顺序绘制图片（勋章、头像、头像框）- 每行显示最多3个图片
    images_per_row = 3
    
    # 创建图片列表，按指定顺序
    image_order = ['nameplate', 'avatar', 'pendant']
    images_to_show = []
    
    for img_type in image_order:
        if img_type in images:
            images_to_show.append((img_type, images[img_type]))
    
    for i in range(0, len(images_to_show), images_per_row):
        row_images = images_to_show[i:i+images_per_row]
        row_y = start_y + 20 + (i // images_per_row) * 110  # 每行间距为110px，增加20px的顶部间距

        # 计算该行图片的总宽度，以便居中
        total_width = len(row_images) * 100 + (len(row_images) - 1) * 20  # 每张图片100px，间距20px
        start_x = (width - total_width) // 2
        
        for j, (img_type, img_data) in enumerate(row_images):
            x_pos = start_x + j * 120  # 每张图片加上间距
        
            # 创建临时图像用于合成
            temp_img = Image.new('RGBA', img.size, (0, 0, 0, 0))
            temp_img.paste(img_data, (x_pos, row_y), img_data)
            
            # 将图片合成到主图像
            img = Image.alpha_composite(img.convert('RGBA'), temp_img).convert('RGB')
            
            # 重新创建draw对象
            draw = ImageDraw.Draw(img)
    
    # 计算需要的高度
    rows_needed = (len(images_to_show) + images_per_row - 1) // images_per_row  # 向上取整
    total_height = rows_needed * 110
    
    return img, draw, total_height