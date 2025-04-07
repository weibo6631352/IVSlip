"""
应用程序核心模块
"""
import sys
import os
import win32gui
import win32con
import win32process
import psutil
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon

from ivmanager.ui.form import InfusionForm
from ivmanager.utils.resource import get_resource_path


class SingleInstanceApp(QApplication):
    """
    单实例应用程序类，确保应用程序只有一个实例运行
    """
    def __init__(self, *args, **kwargs):
        super(SingleInstanceApp, self).__init__(*args, **kwargs)
        self.setQuitOnLastWindowClosed(False)
        self.lock_file = None
        self.lock_file_path = os.path.join(os.path.expanduser("~"), ".infusion_app.lock")
        
        # 尝试在更好的位置创建锁文件
        app_data_dir = os.getenv('APPDATA')
        if app_data_dir:
            lock_dir = os.path.join(app_data_dir, "IVManagementSystem")
            os.makedirs(lock_dir, exist_ok=True)
            self.lock_file_path = os.path.join(lock_dir, "app.lock")
            
        self.check_single_instance()

    def check_single_instance(self):
        """检查是否有其他实例正在运行"""
        # 检查锁文件是否存在
        if os.path.exists(self.lock_file_path):
            try:
                # 读取进程ID
                with open(self.lock_file_path, 'r') as f:
                    pid = f.read().strip()
                    
                # 检查进程是否存在
                if pid and self.is_process_running(int(pid)):
                    # 尝试将已有窗口置前
                    if self.activate_existing_window(int(pid)):
                        self.show_existing_instance(True)
                    else:
                        self.show_existing_instance(False)
                    sys.exit(0)
                else:
                    # 如果进程不存在，删除锁文件
                    os.remove(self.lock_file_path)
            except Exception as e:
                print(f"错误: {e}")
                # 任何错误都删除可能损坏的锁文件
                try:
                    os.remove(self.lock_file_path)
                except:
                    pass
                
        # 创建新的锁文件
        self.lock_file = open(self.lock_file_path, "w")
        self.lock_file.write(str(os.getpid()))
        self.lock_file.flush()
        
        # 确保在程序退出时删除锁文件
        self.aboutToQuit.connect(self.cleanup_lock)

    def is_process_running(self, pid):
        """检查给定PID的进程是否正在运行"""
        try:
            process = psutil.Process(pid)
            return process.is_running() and process.name().lower().endswith(('python.exe', 'pythonw.exe', '输液单管理系统.exe'))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
    
    def find_window_by_pid(self, pid):
        """
        通过进程ID查找窗口句柄
        
        Args:
            pid: 进程ID
            
        Returns:
            窗口句柄列表
        """
        result = []
        
        def callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                _, found_pid = win32process.GetWindowThreadProcessId(hwnd)
                if found_pid == pid:
                    result.append(hwnd)
            return True
        
        win32gui.EnumWindows(callback, None)
        return result
    
    def activate_existing_window(self, pid):
        """
        激活已有的窗口实例
        
        Args:
            pid: 进程ID
            
        Returns:
            是否成功激活
        """
        try:
            # 找到属于该进程的所有窗口
            window_handles = self.find_window_by_pid(pid)
            
            # 遍历所有窗口，寻找我们的主窗口
            for hwnd in window_handles:
                window_title = win32gui.GetWindowText(hwnd)
                if "输液管理系统" in window_title or "IV Management" in window_title:
                    # 显示并激活窗口
                    if win32gui.IsIconic(hwnd):  # 检查窗口是否最小化
                        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    else:
                        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    win32gui.SetForegroundWindow(hwnd)
                    return True
            
            # 未找到特定窗口，尝试激活任何该进程的窗口
            if window_handles:
                hwnd = window_handles[0]
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                else:
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                win32gui.SetForegroundWindow(hwnd)
                return True
            
            return False
        except Exception as e:
            print(f"激活窗口错误: {e}")
            return False

    def cleanup_lock(self):
        """清理锁文件"""
        if self.lock_file:
            self.lock_file.close()
            try:
                os.remove(self.lock_file_path)
            except:
                pass

    def show_existing_instance(self, window_activated):
        """显示已有实例提示"""
        # 显示信息框，通知用户已有实例在运行
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("程序已在运行")
        
        if window_activated:
            msg_box.setText("输液单管理系统已在运行中。")
            msg_box.setInformativeText("已将现有窗口置于前台。")
        else:
            msg_box.setText("输液单管理系统已在运行中。")
            msg_box.setInformativeText("请检查您的任务栏或系统托盘。")
        
        msg_box.exec_()


def main():
    """应用程序主入口函数"""
    app = SingleInstanceApp(sys.argv)
    window = InfusionForm()

    # 设置系统托盘图标
    icon_path = get_resource_path("resources/assets/icon.png")
    tray = QSystemTrayIcon(QIcon(icon_path))
    tray.setToolTip("输液单管理系统")

    # 创建托盘菜单
    tray_menu = QMenu()

    open_action = QAction("打开")
    open_action.triggered.connect(window.showNormal)
    tray_menu.addAction(open_action)

    exit_action = QAction("退出")
    exit_action.triggered.connect(app.quit)
    tray_menu.addAction(exit_action)

    tray.setContextMenu(tray_menu)
    tray.activated.connect(lambda reason: window.showNormal() if reason == QSystemTrayIcon.Trigger else None)
    tray.show()

    window.setWindowIcon(QIcon(icon_path))
    window.show()

    # 覆盖关闭事件，使窗口最小化到托盘
    def close_event(event):
        if tray.isVisible():
            window.hide()
            event.ignore()

    window.closeEvent = close_event

    sys.exit(app.exec_())


if __name__ == '__main__':
    main() 