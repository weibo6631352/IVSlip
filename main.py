import sys
import os
import portalocker
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon

from ui_module import InfusionForm  # Ensure this is the correct path to your InfusionForm class


class SingleInstanceApp(QApplication):
    def __init__(self, *args, **kwargs):
        super(SingleInstanceApp, self).__init__(*args, **kwargs)
        self.setQuitOnLastWindowClosed(False)
        self.lock_file = None
        self.check_single_instance()

    def check_single_instance(self):
        lock_file_path = os.path.expanduser("~/.infusion_app.lock")
        self.lock_file = open(lock_file_path, "w")
        try:
            portalocker.lock(self.lock_file, portalocker.LOCK_EX | portalocker.LOCK_NB)
        except portalocker.LockException:
            sys.exit("另一个实例已经在运行。")


def main():
    app = SingleInstanceApp(sys.argv)
    window = InfusionForm()

    # Set up system tray icon
    tray = QSystemTrayIcon(QIcon("icon.png"))
    tray.setToolTip("输液管理系统")

    # Create tray menu
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

    window.setWindowIcon(QIcon("icon.png"))
    window.show()

    # Override close event to minimize to tray
    def close_event(event):
        if tray.isVisible():
            window.hide()
            event.ignore()

    window.closeEvent = close_event

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
