# common.py
import os
import json
import threading
from collections import deque

# 查询历史记录文件
HISTORY_FILE = "query_history.json"
history_lock = threading.Lock()

def load_query_history():
    """从文件加载查询历史记录"""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return deque(data, maxlen=3)
        else:
            return deque(maxlen=3)
    except Exception as e:
        print(f"加载查询历史失败: {e}")
        return deque(maxlen=3)

def save_query_history(history):
    """保存查询历史记录到文件"""
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(history), f, ensure_ascii=False)
    except Exception as e:
        print(f"保存查询历史失败: {e}")

def delete_user_data(mid):
    """
    删除指定用户的所有数据
    """
    # 删除JSON数据文件
    data_file = f"data/{mid}_data.json"
    if os.path.exists(data_file):
        try:
            os.remove(data_file)
            print(f"已删除用户数据文件: {data_file}")
        except Exception as e:
            print(f"删除数据文件失败: {e}")
    
    # 删除图片文件
    img_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    for ext in img_extensions:
        img_file = f"img/{mid}_face{ext}"
        if os.path.exists(img_file):
            try:
                os.remove(img_file)
                print(f"已删除用户头像: {img_file}")
            except Exception as e:
                print(f"删除头像文件失败: {e}")
        
        img_file = f"img/{mid}_pendant{ext}"
        if os.path.exists(img_file):
            try:
                os.remove(img_file)
                print(f"已删除用户头像框: {img_file}")
            except Exception as e:
                print(f"删除头像框文件失败: {e}")
        
        img_file = f"img/{mid}_nameplate{ext}"
        if os.path.exists(img_file):
            try:
                os.remove(img_file)
                print(f"已删除用户勋章: {img_file}")
            except Exception as e:
                print(f"删除勋章文件失败: {e}")
    
    # 删除生成的用户卡片
    card_file = f"output/{mid}.png"
    if os.path.exists(card_file):
        try:
            os.remove(card_file)
            print(f"已删除用户卡片: {card_file}")
        except Exception as e:
            print(f"删除用户卡片失败: {e}")

def manage_query_history(mid):
    """
    管理查询历史记录，如果超过3个用户则删除最早的
    """
    with history_lock:
        # 从文件加载历史记录
        query_history = load_query_history()
        
        print(f"当前查询历史: {list(query_history)}")
        print(f"新查询用户: {mid}")
        
        # 检查是否是第四个查询，如果是则删除第一个查询的用户数据
        if len(query_history) >= 3:
            # 删除最早的用户数据
            oldest_mid = query_history[0]
            print(f"查询历史已满，正在删除最早的用户数据 (MID: {oldest_mid})...")
            delete_user_data(oldest_mid)
            query_history.popleft()
        
        # 如果用户已经在历史记录中，先移除再添加到末尾（更新顺序）
        if mid in query_history:
            query_history.remove(mid)
        
        # 添加到查询历史记录
        query_history.append(mid)
        print(f"更新后查询历史: {list(query_history)}")
        
        # 保存到文件
        save_query_history(query_history)