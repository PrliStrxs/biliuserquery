import os
import sys

# 添加drawing目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'drawing'))

from drawing import draw_user_card
from PIL import ImageDraw

if __name__ == "__main__":
    """
    单独运行时的主程序
    """
    print("=" * 50)
    print("B站用户信息卡片生成器")
    print("=" * 50)
    
    while True:
        try:
            mid_input = input("\n请输入B站用户MID（输入'quit'退出）: ").strip()
            
            if mid_input.lower() == 'quit':
                print("程序退出，再见！")
                break
            
            # 验证MID是否为数字
            if not mid_input.isdigit():
                print("错误: MID必须是数字")
                continue
            
            mid = int(mid_input)
            
            # 生成信息卡片
            success = draw_user_card(mid)
            if not success:
                print("生成信息卡片失败，请检查数据是否存在")
            
        except KeyboardInterrupt:
            print("\n\n程序被用户中断")
            break
        except Exception as e:
            print(f"发生未知错误: {e}")