"""
输液表单UI模块
"""
import os
import datetime
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QTableWidget, QPushButton, QShortcut, QAction, QGroupBox,
                             QButtonGroup, QRadioButton, QHeaderView, QAbstractItemView,
                             QCompleter, QApplication, QMessageBox, QFileDialog, QStatusBar,
                             QCheckBox)
from PyQt5.QtGui import QFont, QIcon, QKeySequence, QDoubleValidator
from PyQt5.QtCore import Qt, QSize, QStringListModel

from ivmanager.utils.excel import save_to_excel, load_from_excel
from ivmanager.utils.printing import print_excel
from ivmanager.utils.suggestions import load_suggestions
from ivmanager.core.app import get_resource_path


class InfusionForm(QMainWindow):
    """输液管理表单主界面"""
    
    def __init__(self):
        super().__init__()
        
        # 创建中央小部件和主布局
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)
        
        # 设置边距和间距
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        
        # 创建药品名称补全器
        self.completer = QCompleter()
        self.drug_model = QStringListModel()
        self.completer.setModel(self.drug_model)
        
        # 获取药品建议列表
        self.suggestion_list = load_suggestions()
        self.drug_model.setStringList(self.suggestion_list)
        
        self.tables = []
        self.table_in_focus = 0  # 默认第一个表格获取焦点
        
        # 设置应用样式
        self.apply_styles()
        
        # 初始化界面
        self.initUI()
        self.createShortcuts()
        
        # 创建状态栏
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("就绪 - 按下F1获取键盘操作帮助")
        
        # 安装事件过滤器
        self.installEventFilter(self)
    
    def apply_styles(self):
        """应用界面样式"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:pressed {
                background-color: #2a66c8;
            }
            QPushButton:focus {
                border: 2px solid #ffa500;
            }
            QLineEdit {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 2px solid #4a86e8;
            }
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: #ffffff;
                selection-background-color: #e0e0e0;
            }
            QTableWidget QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #cccccc;
                font-weight: bold;
            }
            QRadioButton {
                padding: 5px;
                border-radius: 4px;
            }
            QRadioButton:focus {
                background-color: #e0e0e0;
            }
            QCheckBox {
                padding: 5px;
            }
            QCheckBox:focus {
                background-color: #e0e0e0;
            }
            QComboBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
                min-height: 30px;
            }
            QComboBox:focus {
                border: 2px solid #4a86e8;
            }
            QStatusBar {
                background-color: #f5f5f5;
                color: #333333;
            }
        """)
    
    def initUI(self):
        """初始化用户界面"""
        # 待实现: 根据原有UI代码实现
        pass
    
    def createShortcuts(self):
        """创建快捷键"""
        # 添加快捷键
        self.shortcutSave = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcutSave.activated.connect(self.saveForm)
        
        self.shortcutPrint = QShortcut(QKeySequence("Ctrl+P"), self)
        self.shortcutPrint.activated.connect(self.printForm)
        
        self.shortcutReset = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcutReset.activated.connect(self.resetForm)
        
        self.shortcutImport = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcutImport.activated.connect(self.importForm)
        
        self.shortcutExit = QShortcut(QKeySequence("Alt+F4"), self)
        self.shortcutExit.activated.connect(self.close)
        
        # 表格快捷键
        self.shortcutAddRows = QShortcut(QKeySequence("Ctrl+A"), self)
        self.shortcutAddRows.activated.connect(self.addMoreRows)
        
        self.shortcutRemoveRows = QShortcut(QKeySequence("Ctrl+D"), self)
        self.shortcutRemoveRows.activated.connect(self.removeRows)
        
        # 表格焦点切换快捷键
        self.shortcutTable1 = QShortcut(QKeySequence("Alt+1"), self)
        self.shortcutTable1.activated.connect(lambda: self.focus_table(0))
        
        self.shortcutTable2 = QShortcut(QKeySequence("Alt+2"), self)
        self.shortcutTable2.activated.connect(lambda: self.focus_table(1))
        
        self.shortcutTable3 = QShortcut(QKeySequence("Alt+3"), self)
        self.shortcutTable3.activated.connect(lambda: self.focus_table(2))
        
        self.shortcutTable4 = QShortcut(QKeySequence("Alt+4"), self)
        self.shortcutTable4.activated.connect(lambda: self.focus_table(3))
        
        # 帮助快捷键
        self.shortcutHelp = QShortcut(QKeySequence("F1"), self)
        self.shortcutHelp.activated.connect(self.showHelp)
    
    def saveForm(self):
        """保存表单"""
        # 待实现
        pass
    
    def printForm(self):
        """打印表单"""
        # 待实现
        pass
    
    def resetForm(self):
        """重置表单"""
        # 待实现
        pass
    
    def importForm(self):
        """导入表单"""
        # 待实现
        pass
    
    def addMoreRows(self):
        """添加更多行"""
        # 待实现
        pass
    
    def removeRows(self):
        """移除行"""
        # 待实现
        pass
    
    def focus_table(self, index):
        """聚焦到指定表格"""
        # 待实现
        pass
    
    def showHelp(self):
        """显示帮助"""
        # 待实现
        pass 