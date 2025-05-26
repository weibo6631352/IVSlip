"""
输液单管理系统主入口模块
"""
import sys
import os

# 确保可以正确导入项目内的模块
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 确保当前目录在路径中
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 添加可能的额外资源目录
executable_dir = os.path.dirname(sys.executable)
if os.path.exists(os.path.join(executable_dir, 'ivmanager')):
    # 可能是打包后的环境，添加可执行文件目录
    if executable_dir not in sys.path:
        sys.path.append(executable_dir)

# 导入主函数并运行
from ivmanager.core.app import main

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        error_msg = f"程序出错: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        
        # 在打包环境下，可能需要将错误写入日志文件
        try:
            log_dir = os.path.join(os.path.dirname(sys.executable), 'logs')
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            
            with open(os.path.join(log_dir, 'error.log'), 'a', encoding='utf-8') as f:
                f.write(f"[{os.path.basename(__file__)}] {error_msg}\n")
        except:
            pass
        
        # 显示错误消息框
        try:
            from PyQt5.QtWidgets import QApplication, QMessageBox
            app = QApplication(sys.argv)
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("程序错误")
            msg_box.setText("程序运行出错")
            msg_box.setDetailedText(error_msg)
            msg_box.exec_()
        except:
            pass 