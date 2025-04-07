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
from ivmanager.utils.resource import get_resource_path


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
        font = QFont()
        font.setPointSize(10)
        
        # 创建基本信息部分
        infoGroupBox = QGroupBox("患者信息")
        infoGroupBox.setFont(font)
        infoLayout = QHBoxLayout()
        
        # 姓名输入
        leftLayout = QVBoxLayout()
        nameLabel = QLabel('姓名(Alt+N)：')
        nameLabel.setFont(font)
        self.nameEdit = QLineEdit()
        self.nameEdit.setFixedHeight(40)
        self.nameEdit.setFont(font)
        self.nameEdit.setPlaceholderText("请输入患者姓名")
        self.nameEdit.setToolTip("按Alt+N快速访问姓名输入框")
        
        # 添加快捷键
        nameShortcut = QShortcut(QKeySequence("Alt+N"), self)
        nameShortcut.activated.connect(lambda: self.nameEdit.setFocus())
        
        leftLayout.addWidget(nameLabel)
        leftLayout.addWidget(self.nameEdit)
        
        # 性别选择
        middleLayout = QVBoxLayout()
        genderLabel = QLabel('性别(Alt+G)：')
        genderLabel.setFont(font)
        
        # 创建更大、更易点击的性别选择按钮组
        genderLayout = QHBoxLayout()
        self.genderGroup = QButtonGroup(self)
        
        # 使用大按钮替代单选按钮
        self.maleButton = QPushButton('男')
        self.maleButton.setFont(font)
        self.maleButton.setCheckable(True)
        self.maleButton.setChecked(True)
        self.maleButton.setFixedHeight(40)
        self.maleButton.setStyleSheet("""
            QPushButton:checked {
                background-color: #4a86e8;
                color: white;
            }
            QPushButton:!checked {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #cccccc;
            }
        """)
        
        self.femaleButton = QPushButton('女')
        self.femaleButton.setFont(font)
        self.femaleButton.setCheckable(True)
        self.femaleButton.setFixedHeight(40)
        self.femaleButton.setStyleSheet("""
            QPushButton:checked {
                background-color: #E91E63;
                color: white;
            }
            QPushButton:!checked {
                background-color: #f0f0f0;
                color: black;
                border: 1px solid #cccccc;
            }
        """)
        
        # 连接按钮切换事件
        self.maleButton.clicked.connect(lambda: self.femaleButton.setChecked(False))
        self.femaleButton.clicked.connect(lambda: self.maleButton.setChecked(False))
        
        # 添加性别快捷键
        genderShortcut = QShortcut(QKeySequence("Alt+G"), self)
        genderShortcut.activated.connect(self.toggleGender)
        
        genderLayout.addWidget(self.maleButton)
        genderLayout.addWidget(self.femaleButton)
        
        middleLayout.addWidget(genderLabel)
        middleLayout.addLayout(genderLayout)
        
        # 年龄输入
        rightLayout = QVBoxLayout()
        ageLabel = QLabel('年龄(Alt+A)：')
        ageLabel.setFont(font)
        self.ageEdit = QLineEdit()
        self.ageEdit.setFixedHeight(40)
        self.ageEdit.setFont(font)
        self.ageEdit.setPlaceholderText("请输入年龄")
        self.ageEdit.setValidator(QDoubleValidator(0, 150, 0))  # 只允许输入0-150的整数
        self.ageEdit.setToolTip("按Alt+A快速访问年龄输入框")
        
        # 添加快捷键
        ageShortcut = QShortcut(QKeySequence("Alt+A"), self)
        ageShortcut.activated.connect(lambda: self.ageEdit.setFocus())
        
        rightLayout.addWidget(ageLabel)
        rightLayout.addWidget(self.ageEdit)
        
        # 将三部分添加到信息布局
        infoLayout.addLayout(leftLayout)
        infoLayout.addLayout(middleLayout)
        infoLayout.addLayout(rightLayout)
        
        infoGroupBox.setLayout(infoLayout)
        self.layout.addWidget(infoGroupBox)
        
        # 创建药品输入表格
        self.createTables()
        
        # 添加价格输入区域
        priceGroupBox = QGroupBox("费用信息")
        priceGroupBox.setFont(font)
        
        priceGroupBoxLayout = QHBoxLayout(priceGroupBox)
        
        priceLabel = QLabel('总计价格(Alt+P)：')
        priceLabel.setFont(font)
        self.priceEdit = QLineEdit()
        self.priceEdit.setFixedHeight(40)
        self.priceEdit.setFont(font)
        self.priceEdit.setPlaceholderText("请输入总金额")
        self.priceEdit.setToolTip("按Alt+P快速访问总计价格输入框")
        
        # 添加快捷键
        priceShortcut = QShortcut(QKeySequence("Alt+P"), self)
        priceShortcut.activated.connect(lambda: self.priceEdit.setFocus())
        
        # 只允许输入数字和小数点
        self.priceEdit.setValidator(QDoubleValidator(0, 10000, 2))

        priceGroupBoxLayout.addWidget(priceLabel)
        priceGroupBoxLayout.addWidget(self.priceEdit)
        self.layout.addWidget(priceGroupBox)

        # 操作按钮区域
        buttonsGroupBox = QGroupBox("操作区")
        buttonsGroupBox.setFont(font)
        buttonsGroupBoxLayout = QVBoxLayout(buttonsGroupBox)
        
        # 表格行操作
        moreLessLayout = QHBoxLayout()
        
        # 获取图标路径
        icon_path = get_resource_path("resources/assets/icon.png")
        
        moreButton = QPushButton('添加更多药品行 (Ctrl+A)')
        moreButton.setFixedHeight(40)
        moreButton.setFont(font)
        moreButton.setIcon(QIcon(icon_path))
        moreButton.setIconSize(QSize(20, 20))
        moreButton.clicked.connect(self.addMoreRows)
        moreButton.setToolTip("按Ctrl+A添加更多药品行")
        
        lessButton = QPushButton('减少药品行 (Ctrl+D)')
        lessButton.setFixedHeight(40)
        lessButton.setFont(font)
        lessButton.setIcon(QIcon(icon_path))
        lessButton.setIconSize(QSize(20, 20))
        lessButton.clicked.connect(self.removeRows)
        lessButton.setToolTip("按Ctrl+D减少药品行")
        
        moreLessLayout.addWidget(moreButton)
        moreLessLayout.addWidget(lessButton)
        buttonsGroupBoxLayout.addLayout(moreLessLayout)
        
        # 文件操作按钮
        fileButtonsLayout = QHBoxLayout()
        
        saveButton = QPushButton('保存 (Ctrl+S)')
        saveButton.setFixedHeight(40)
        saveButton.setFont(font)
        saveButton.setIcon(QIcon(icon_path))
        saveButton.setIconSize(QSize(20, 20))
        saveButton.clicked.connect(self.saveForm)
        saveButton.setToolTip("按Ctrl+S保存表单")
        
        printButton = QPushButton('打印 (Ctrl+P)')
        printButton.setFixedHeight(40)
        printButton.setFont(font)
        printButton.setIcon(QIcon(icon_path))
        printButton.setIconSize(QSize(20, 20))
        printButton.clicked.connect(self.printForm)
        printButton.setToolTip("按Ctrl+P打印表单")
        
        resetButton = QPushButton('重置 (Ctrl+R)')
        resetButton.setFixedHeight(40)
        resetButton.setFont(font)
        resetButton.setIcon(QIcon(icon_path))
        resetButton.setIconSize(QSize(20, 20))
        resetButton.clicked.connect(self.resetForm)
        resetButton.setToolTip("按Ctrl+R重置表单数据")
        
        importButton = QPushButton('导入 (Ctrl+O)')
        importButton.setFixedHeight(40)
        importButton.setFont(font)
        importButton.setIcon(QIcon(icon_path))
        importButton.setIconSize(QSize(20, 20))
        importButton.clicked.connect(self.importForm)
        importButton.setToolTip("按Ctrl+O导入已有表单")
        
        helpButton = QPushButton('帮助 (F1)')
        helpButton.setFixedHeight(40)
        helpButton.setFont(font)
        helpButton.setIcon(QIcon(icon_path))
        helpButton.setIconSize(QSize(20, 20))
        helpButton.clicked.connect(self.showHelp)
        helpButton.setToolTip("按F1查看键盘操作帮助")
        
        fileButtonsLayout.addWidget(saveButton)
        fileButtonsLayout.addWidget(printButton)
        fileButtonsLayout.addWidget(resetButton)
        fileButtonsLayout.addWidget(importButton)
        fileButtonsLayout.addWidget(helpButton)
        
        buttonsGroupBoxLayout.addLayout(fileButtonsLayout)
        self.layout.addWidget(buttonsGroupBox)

        self.setWindowTitle('输液单管理系统')
        self.resize(1200, 700)

    def createTables(self):
        """创建药品表格"""
        # 创建四联药品表格
        tablesGroupBox = QGroupBox("药品信息")
        font = QFont()
        font.setPointSize(10)
        tablesGroupBox.setFont(font)
        
        tablesLayout = QVBoxLayout()
        tableHeadersLayout = QHBoxLayout()
        
        # 创建四个表头标签
        for i in range(4):
            label = QLabel(f"第{i+1}联 (Alt+{i+1})")
            label.setFont(font)
            label.setAlignment(Qt.AlignCenter)
            tableHeadersLayout.addWidget(label)
        
        tablesLayout.addLayout(tableHeadersLayout)
        
        # 创建表格区域
        tablesHLayout = QHBoxLayout()
        
        for i in range(4):
            table = QTableWidget()
            table.setColumnCount(1)
            table.setRowCount(10)  # 开始时10行
            table.setHorizontalHeaderLabels(['药品名称'])
            
            # 设置表格属性
            table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
            table.verticalHeader().setVisible(False)
            table.setSelectionMode(QAbstractItemView.SingleSelection)
            table.setSelectionBehavior(QAbstractItemView.SelectItems)
            table.setAlternatingRowColors(True)
            
            # 设置表格标识
            table.setProperty("table_index", i)
            
            # 填充药品输入单元格
            for row in range(table.rowCount()):
                self.set_item_completer(table, row, 0)
            
            # 添加到列表和布局
            self.tables.append(table)
            tablesHLayout.addWidget(table)
        
        tablesLayout.addLayout(tablesHLayout)
        tablesGroupBox.setLayout(tablesLayout)
        self.layout.addWidget(tablesGroupBox)

    def set_item_completer(self, table, row, col):
        """设置表格单元格的自动补全"""
        line_edit = QLineEdit()
        line_edit.setCompleter(self.completer)
        line_edit.setAlignment(Qt.AlignCenter)
        
        # 设置样式
        line_edit.setStyleSheet("border:none; background-color: #ffffff;")
        
        # 设置字体
        font = QFont()
        font.setPointSize(10)
        line_edit.setFont(font)
        
        # 安装事件过滤器以处理回车键
        line_edit.installEventFilter(self)
        
        # 设置辅助功能标识
        line_edit.setAccessibleName(f"药品输入框 {row+1}")
        
        # 设置单元格数据
        line_edit.setProperty("table_index", table.property("table_index"))
        line_edit.setProperty("row", row)
        line_edit.setProperty("col", col)
        
        table.setCellWidget(row, col, line_edit)

    def toggleGender(self):
        """切换性别选择"""
        if self.maleButton.isChecked():
            self.maleButton.setChecked(False)
            self.femaleButton.setChecked(True)
        else:
            self.maleButton.setChecked(True)
            self.femaleButton.setChecked(False)
    
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
        if not self.validateForm():
            return
        self.statusBar.showMessage("正在保存...", 3000)
        self.save_and_print(print_out=False)
    
    def printForm(self):
        """打印表单"""
        if not self.validateForm():
            return
        self.statusBar.showMessage("正在准备打印...", 3000)
        self.save_and_print(print_out=True)
    
    def resetForm(self):
        """重置表单"""
        reply = QMessageBox.question(
            self, '确认重置', 
            '确定要重置表单吗? 所有数据将被清空。',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.nameEdit.clear()
            self.maleButton.setChecked(True)
            self.femaleButton.setChecked(False)
            self.ageEdit.clear()
            self.priceEdit.clear()
            
            for table in self.tables:
                for row in range(table.rowCount()):
                    line_edit = table.cellWidget(row, 0)
                    if line_edit:
                        line_edit.clear()
            
            self.statusBar.showMessage("表单已重置", 3000)
    
    def importForm(self):
        """导入表单"""
        filepath, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "d:/输液单/", "Excel Files (*.xlsx)")
        if filepath:
            try:
                name, gender, age, drugs, price = load_from_excel(filepath)
                self.nameEdit.setText(name)
                if gender == '男':
                    self.maleButton.setChecked(True)
                    self.femaleButton.setChecked(False)
                else:
                    self.maleButton.setChecked(False)
                    self.femaleButton.setChecked(True)
                self.ageEdit.setText(str(age))
                self.priceEdit.setText(str(price))
                # 将 drugs 分成 4 组填入每个表格
                for i, table in enumerate(self.tables):
                    group_drugs = drugs[i]
                    # 确保表格有足够的行
                    if len(group_drugs) > table.rowCount():
                        table.setRowCount(len(group_drugs))
                        for row in range(table.rowCount()):
                            if not table.cellWidget(row, 0):
                                self.set_item_completer(table, row, 0)
                    
                    # 填充数据
                    for row in range(table.rowCount()):
                        line_edit = table.cellWidget(row, 0)
                        if row < len(group_drugs):
                            line_edit.setText(group_drugs[row])
                        else:
                            line_edit.setText('')
                self.statusBar.showMessage(f"导入成功: {filepath}", 3000)
            except Exception as e:
                self.statusBar.showMessage(f"导入失败: {str(e)}", 5000)
                QMessageBox.critical(self, "导入错误", f"导入文件时发生错误: {e}")
    
    def addMoreRows(self):
        """添加更多行"""
        for table in self.tables:
            currentRowCount = table.rowCount()
            table.setRowCount(currentRowCount + 10)
            for row in range(currentRowCount, currentRowCount + 10):
                self.set_item_completer(table, row, 0)
        self.statusBar.showMessage("已添加更多药品行", 3000)
    
    def removeRows(self):
        """移除行"""
        for table in self.tables:
            currentRowCount = table.rowCount()
            if currentRowCount > 10:
                table.setRowCount(currentRowCount - 10)
        self.statusBar.showMessage("已减少药品行", 3000)
    
    def focus_table(self, index):
        """聚焦到指定表格"""
        if 0 <= index < len(self.tables):
            self.table_in_focus = index
            table = self.tables[index]
            if table.rowCount() > 0:
                first_cell = table.cellWidget(0, 0)
                if first_cell:
                    first_cell.setFocus()
                    self.statusBar.showMessage(f"已切换到第{index+1}联", 2000)
    
    def validateForm(self):
        """验证表单输入"""
        # 验证姓名
        if not self.nameEdit.text().strip():
            QMessageBox.warning(self, "输入错误", "请输入患者姓名")
            self.nameEdit.setFocus()
            return False
        
        # 验证年龄
        if not self.ageEdit.text().strip():
            QMessageBox.warning(self, "输入错误", "请输入患者年龄")
            self.ageEdit.setFocus()
            return False
        
        # 验证至少有一个药品
        has_drug = False
        for table in self.tables:
            for row in range(table.rowCount()):
                widget = table.cellWidget(row, 0)
                if widget and widget.text().strip():
                    has_drug = True
                    break
            if has_drug:
                break
                
        if not has_drug:
            QMessageBox.warning(self, "输入错误", "请至少输入一种药品")
            if self.tables and self.tables[0].rowCount() > 0:
                first_cell = self.tables[0].cellWidget(0, 0)
                if first_cell:
                    first_cell.setFocus()
            return False
            
        return True
    
    def save_and_print(self, print_out):
        """保存并打印表单"""
        name = self.nameEdit.text()
        gender = '男' if self.maleButton.isChecked() else '女'
        age = self.ageEdit.text()
        price = self.priceEdit.text()
        drugs = [[] for _ in range(4)]

        for i, table in enumerate(self.tables):
            for row in range(table.rowCount()):
                drugItem = table.cellWidget(row, 0)
                if drugItem:
                    text = drugItem.text().strip()
                    if text:
                        drugs[i].append(text)

        nowtime = datetime.datetime.now()
        date_str = nowtime.strftime("%Y-%m-%d")

        # 确保目录存在
        save_dir = f"d:/输液单/{nowtime.strftime('%Y')}/{nowtime.strftime('%m')}/{nowtime.strftime('%d')}"
        os.makedirs(save_dir, exist_ok=True)

        # 存储Excel文件
        timestamp = nowtime.strftime("%Y-%m-%d_%H-%M-%S")
        filepath = f"{save_dir}/{timestamp}_{name}.xlsx"
        
        try:
            save_to_excel(filepath, name, gender, age, drugs, date_str, price)
            
            if print_out:
                # 打印Excel
                self.statusBar.showMessage(f"正在打印...", 3000)
                print_excel(filepath)
            else:
                self.statusBar.showMessage(f"保存成功: {filepath}", 5000)
                QMessageBox.information(self, "保存成功", f"输液单已保存到: {filepath}")
        except Exception as e:
            self.statusBar.showMessage(f"操作失败: {str(e)}", 5000)
            QMessageBox.critical(self, "错误", f"操作失败: {str(e)}")
    
    def showHelp(self):
        """显示帮助"""
        help_text = """
<h3>键盘操作帮助</h3>
<table border='1' cellspacing='0' cellpadding='5'>
  <tr><th>快捷键</th><th>功能</th></tr>
  <tr><td>Tab</td><td>移动到下一个输入框</td></tr>
  <tr><td>Shift+Tab</td><td>移动到上一个输入框</td></tr>
  <tr><td>Enter</td><td>在表格中移动到下一行</td></tr>
  <tr><td>Alt+N</td><td>聚焦到姓名输入框</td></tr>
  <tr><td>Alt+G</td><td>切换性别选择</td></tr>
  <tr><td>Alt+A</td><td>聚焦到年龄输入框</td></tr>
  <tr><td>Alt+P</td><td>聚焦到价格输入框</td></tr>
  <tr><td>Alt+1,2,3,4</td><td>切换到对应表格</td></tr>
  <tr><td>Ctrl+S</td><td>保存表单</td></tr>
  <tr><td>Ctrl+P</td><td>打印表单</td></tr>
  <tr><td>Ctrl+R</td><td>重置表单</td></tr>
  <tr><td>Ctrl+O</td><td>导入表单</td></tr>
  <tr><td>Ctrl+A</td><td>添加更多药品行</td></tr>
  <tr><td>Ctrl+D</td><td>减少药品行</td></tr>
  <tr><td>F1</td><td>显示此帮助</td></tr>
</table>
"""
        QMessageBox.information(self, "键盘操作帮助", help_text)
    
    def eventFilter(self, obj, event):
        """事件过滤器，处理特殊键盘事件"""
        if event.type() == event.KeyPress and hasattr(obj, 'property'):
            if obj.property("table_index") is not None:
                # 处理表格中的按键
                if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    table_index = obj.property("table_index")
                    row = obj.property("row")
                    
                    # 移动到下一行
                    if row + 1 < self.tables[table_index].rowCount():
                        next_item = self.tables[table_index].cellWidget(row + 1, 0)
                        if next_item:
                            next_item.setFocus()
                    return True
        
        return super().eventFilter(obj, event) 