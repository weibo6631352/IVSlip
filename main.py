import sys
import os
import portalocker
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QObject
from ui_module import InfusionForm  # 确保这是你的 InfusionForm 类的正确路径

class SingleInstanceApp(QApplication):
    def __init__(self, *args, **kwargs):
        super(SingleInstanceApp, self).__init__(*args, **kwargs)
        self.setQuitOnLastWindowClosed(False)  # 设置在最后一个窗口关闭时不退出应用程序
        self.lock_file = None
        self.check_single_instance()  # 检查单实例

    def check_single_instance(self):
        # 锁文件的路径
        self.lock_file = open(os.path.expanduser("~/.infusion_app.lock"), "w")
        try:
            # 尝试获取文件锁
            portalocker.lock(self.lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
        except portalocker.LockException:
            # 如果锁已经被持有，说明另一个实例正在运行
            sys.exit("另一个实例已经在运行。")

    def show_existing_instance(self):
        # 显示信息框，通知用户已有实例在运行
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("另一个实例已经在运行。")
        msg_box.setInformativeText("点击托盘图标将已有实例显示到前台。")
        msg_box.setWindowTitle("实例已在运行")
        msg_box.exec_()

def main():
    app = SingleInstanceApp(sys.argv)  # 创建应用程序实例
    window = InfusionForm()  # 创建主窗口实例
    app.comm.show_window.connect(window.showNormal)  # 连接信号和槽，显示窗口

    # 设置系统托盘
    tray = QSystemTrayIcon(QIcon("icon.png"))  # 使用适当的图标文件
    tray.setToolTip("输液管理系统")  # 设置托盘提示

    # 创建托盘菜单
    tray_menu = QMenu()
    open_action = QAction("打开")
    open_action.triggered.connect(window.showNormal)  # 连接打开动作和显示窗口
    tray_menu.addAction(open_action)

    exit_action = QAction("退出")
    exit_action.triggered.connect(app.quit)  # 连接退出动作和退出应用
    tray_menu.addAction(exit_action)

    tray.setContextMenu(tray_menu)  # 设置托盘菜单
    tray.activated.connect(lambda reason: window.showNormal() if reason == QSystemTrayIcon.Trigger else None)
    tray.show()  # 显示托盘图标

    window.setWindowIcon(QIcon("icon.png"))  # 设置主窗口图标
    window.show()  # 显示主窗口

    # 重写关闭事件，最小化到托盘
    def close_event(event):
        if tray.isVisible():
            window.hide()  # 隐藏窗口
            event.ignore()  # 忽略关闭事件

    window.closeEvent = close_event  # 连接关闭事件和自定义处理函数

    sys.exit(app.exec_())  # 运行应用程序主循环

if __name__ == '__main__':
    main()
