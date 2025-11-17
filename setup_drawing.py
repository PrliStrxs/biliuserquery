import os
import sys

def setup_drawing_environment():
    """
    设置绘图环境
    """
    print("正在设置绘图环境...")
    
    # 创建必要的目录
    directories = [
        "drawing/fonts",
        "output",
        "data",
        "img"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"创建目录: {directory}")
    
    # 尝试下载字体
    try:
        from drawing.download_fonts import download_chinese_fonts
        downloaded = download_chinese_fonts()
        if downloaded:
            print(f"成功下载字体: {', '.join(downloaded)}")
        else:
            print("未下载新字体")
    except Exception as e:
        print(f"字体下载失败: {e}")
    
    # 测试模块
    try:
        from drawing.test_modules import test_all_modules
        if test_all_modules():
            print("所有模块测试通过!")
        else:
            print("部分模块测试失败，但环境已基本设置完成")
    except Exception as e:
        print(f"模块测试失败: {e}")
    
    print("绘图环境设置完成!")

if __name__ == "__main__":
    setup_drawing_environment()