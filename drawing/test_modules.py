import os
import sys

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(__file__))

def test_font_manager():
    """测试字体管理模块"""
    print("测试字体管理模块...")
    from font_manager import get_font_path, load_fonts
    font_path = get_font_path()
    print(f"找到字体路径: {font_path}")
    
    if font_path:
        fonts = load_fonts(font_path)
        print("字体加载成功")
        return True
    else:
        print("未找到字体")
        return False

def test_background_drawer():
    """测试背景绘制模块"""
    print("测试背景绘制模块...")
    from background_drawer import create_canvas, draw_header_background
    img, draw = create_canvas(800, 200)
    draw_header_background(draw, 800)
    print("背景绘制测试完成")
    return True

def test_all_modules():
    """测试所有模块"""
    print("开始测试所有绘图模块...")
    
    tests = [
        test_font_manager,
        test_background_drawer,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"测试失败: {e}")
            results.append(False)
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"测试完成: {success_count}/{total_count} 个测试通过")
    return all(results)

if __name__ == "__main__":
    test_all_modules()