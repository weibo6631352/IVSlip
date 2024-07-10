from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QTableWidget, QTableWidgetItem, QGroupBox, QCompleter, QRadioButton, QButtonGroup
from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtCore import Qt
import datetime
from excel_module import save_to_excel, load_from_excel
import win32com.client as win32
import json

from suggestion_module import load_suggestions


class InfusionForm(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        font = QFont()
        font.setPointSize(14)

        # 姓名, 性别, 年龄 放在一行
        infoLayout = QHBoxLayout()
        nameLabel = QLabel('姓名：')
        nameLabel.setFont(font)
        self.nameEdit = QLineEdit()
        self.nameEdit.setFixedHeight(40)
        self.nameEdit.setFont(font)

        genderLabel = QLabel('性别：')
        genderLabel.setFont(font)

        self.genderGroup = QButtonGroup(self)
        self.maleRadio = QRadioButton('男')
        self.maleRadio.setFont(font)
        self.maleRadio.setChecked(True)
        self.femaleRadio = QRadioButton('女')
        self.femaleRadio.setFont(font)
        self.genderGroup.addButton(self.maleRadio)
        self.genderGroup.addButton(self.femaleRadio)

        ageLabel = QLabel('年龄：')
        ageLabel.setFont(font)
        self.ageEdit = QLineEdit()
        self.ageEdit.setFixedHeight(40)
        self.ageEdit.setFont(font)
        self.ageEdit.setValidator(QIntValidator(0, 150))

        infoLayout.addWidget(nameLabel)
        infoLayout.addWidget(self.nameEdit)
        infoLayout.addWidget(genderLabel)
        infoLayout.addWidget(self.maleRadio)
        infoLayout.addWidget(self.femaleRadio)
        infoLayout.addWidget(ageLabel)
        infoLayout.addWidget(self.ageEdit)

        self.layout.addLayout(infoLayout)

        # 创建四联
        self.tables = []
        groupBoxLayout = QHBoxLayout()
        self.suggestions = load_suggestions()
        self.completer = QCompleter(self.suggestions)
        for i in range(4):
            groupBox = QGroupBox(f'第{i + 1}联')
            groupBox.setFont(font)
            groupBoxInnerLayout = QVBoxLayout()
            table = QTableWidget(20, 2)  # 初始20行2列
            table.setHorizontalHeaderLabels(['药品', '数量'])

            # 第一列宽度自适应扩展，第二列宽度固定
            table.horizontalHeader().setSectionResizeMode(0, 1)
            table.horizontalHeader().setSectionResizeMode(1, 0)
            table.setColumnWidth(1, 100)

            # 纵向表头不要字体那么明显,新建一种不要加粗的字体，特供纵向表头
            f = table.verticalHeader().font()
            f.setBold(False)
            f.setPointSize(12)
            table.verticalHeader().setFont(f)

            f.setPointSize(14)
            table.setFont(f)
            # 行表头隐藏
            table.verticalHeader().hide()

            # 默认数量列为1，内容居中
            for row in range(table.rowCount()):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 1, item)
                self.set_item_completer(table, row, 0)

            table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
            table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

            groupBoxInnerLayout.addWidget(table)
            groupBox.setLayout(groupBoxInnerLayout)
            groupBoxLayout.addWidget(groupBox)
            self.tables.append(table)
        self.layout.addLayout(groupBoxLayout)

        # 更多按钮
        moreButton = QPushButton('更多')
        moreButton.setFixedHeight(40)
        moreButton.setFont(font)
        moreButton.clicked.connect(self.addMoreRows)

        # 更少按钮
        lessButton = QPushButton('更少')
        lessButton.setFixedHeight(40)
        lessButton.setFont(font)
        lessButton.clicked.connect(self.removeRows)

        moreLessLayout = QHBoxLayout()
        moreLessLayout.addWidget(moreButton)
        moreLessLayout.addWidget(lessButton)
        self.layout.addLayout(moreLessLayout)

        # 打印按钮
        printButton = QPushButton('打印')
        printButton.setFixedHeight(40)
        printButton.setFont(font)
        printButton.clicked.connect(self.printForm)

        # 重置按钮
        resetButton = QPushButton('重置')
        resetButton.setFixedHeight(40)
        resetButton.setFont(font)
        resetButton.clicked.connect(self.resetForm)

        # 导入按钮
        importButton = QPushButton('导入')
        importButton.setFixedHeight(40)
        importButton.setFont(font)
        importButton.clicked.connect(self.importForm)

        # 按钮布局
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(printButton)
        buttonLayout.addWidget(resetButton)
        buttonLayout.addWidget(importButton)

        self.layout.addLayout(buttonLayout)

        self.setLayout(self.layout)
        self.setWindowTitle('史中英诊所输液管理系统')
        self.resize(1440, 860)
        self.show()

    def set_item_completer(self, table, row, col):
        line_edit = QLineEdit()
        line_edit.setCompleter(self.completer)
        line_edit.setAlignment(Qt.AlignCenter)
        # 去掉边框
        line_edit.setStyleSheet("border:none;")
        # 设置14号字体
        font = QFont()
        font.setPointSize(14)
        line_edit.setFont(font)
        table.setCellWidget(row, col, line_edit)

    def addMoreRows(self):
        for table in self.tables:
            currentRowCount = table.rowCount()
            table.setRowCount(currentRowCount + 10)
            for row in range(currentRowCount, currentRowCount + 10):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 1, item)
                self.set_item_completer(table, row, 0)

    def removeRows(self):
        for table in self.tables:
            currentRowCount = table.rowCount()
            if currentRowCount > 10:
                table.setRowCount(currentRowCount - 10)

    def printForm(self):
        name = self.nameEdit.text()
        gender = '男' if self.maleRadio.isChecked() else '女'
        age = self.ageEdit.text()
        drugs = [[] for _ in range(4)]
        quantities = [[] for _ in range(4)]

        for i, table in enumerate(self.tables):
            for row in range(table.rowCount()):
                drugItem = table.cellWidget(row, 0)
                quantityItem = table.item(row, 1)
                if drugItem and quantityItem:
                    drugs[i].append(drugItem.text())
                    quantities[i].append(quantityItem.text())

        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 存储Excel文件
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filepath = f"d:/输液单/{datetime.datetime.now().strftime('%Y-%m')}/{timestamp}_{name}.xlsx"
        save_to_excel(filepath, name, gender, age, drugs, quantities, date_str)

        # 打印Excel中的“打印页”
        self.print_excel(filepath)

    def print_excel(self, filepath):
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(filepath)
        sheet = workbook.Sheets('打印页')
        sheet.PageSetup.PaperSize = 9  # A5
        sheet.PrintOut()
        workbook.Close(False)
        excel.Quit()

    def resetForm(self):
        self.nameEdit.clear()
        self.genderGroup.setExclusive(False)
        self.maleRadio.setChecked(True)
        self.femaleRadio.setChecked(False)
        self.genderGroup.setExclusive(True)
        self.ageEdit.clear()
        for table in self.tables:
            table.clearContents()
            for row in range(table.rowCount()):
                item = QTableWidgetItem('1')
                item.setTextAlignment(Qt.AlignCenter)
                table.setItem(row, 1, item)
                self.set_item_completer(table, row, 0)

    def importForm(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "d:/输液单/", "Excel Files (*.xlsx)")
        if filepath:
            name, gender, age, drugs, quantities = load_from_excel(filepath)
            self.nameEdit.setText(name)
            if gender == '男':
                self.maleRadio.setChecked(True)
            else:
                self.femaleRadio.setChecked(True)
            self.ageEdit.setText(age)
            # 将 drugs 和 quantities 分成 4 组填入每个表格
            for i, table in enumerate(self.tables):
                group_drugs = drugs[i]
                group_quantities = quantities[i]
                for row in range(table.rowCount()):
                    if row < len(group_drugs):
                        line_edit = table.cellWidget(row, 0)
                        line_edit.setText(group_drugs[row])
                        line_edit.setAlignment(Qt.AlignCenter)
                        item = QTableWidgetItem(group_quantities[row])
                        item.setTextAlignment(Qt.AlignCenter)
                        table.setItem(row, 1, item)
                    else:
                        line_edit = table.cellWidget(row, 0)
                        line_edit.setText('')
                        line_edit.setAlignment(Qt.AlignCenter)
                        item = QTableWidgetItem('1')
                        item.setTextAlignment(Qt.AlignCenter)
                        table.setItem(row, 1, item)

