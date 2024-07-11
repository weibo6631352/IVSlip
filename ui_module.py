from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, \
    QTableWidget, QGroupBox, QCompleter, QRadioButton, QButtonGroup, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import datetime
import win32com.client as win32
from excel_module import save_to_excel, load_from_excel
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
        self.completer = QCompleter(self.suggestions, self)
        self.completer.setFilterMode(Qt.MatchContains)  # 设置过滤模式为包含匹配
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # 设置不区分大小写
        for i in range(4):
            groupBox = QGroupBox(f'第{i + 1}联')
            groupBox.setFont(font)
            groupBoxInnerLayout = QVBoxLayout()
            table = QTableWidget(10, 1)  # 初始20行1列
            table.setHorizontalHeaderLabels(['药品'])

            # 第一列宽度自适应扩展
            table.horizontalHeader().setSectionResizeMode(0, 1)

            # 纵向表头不要字体那么明显,新建一种不要加粗的字体，特供纵向表头
            f = table.verticalHeader().font()
            f.setBold(False)
            f.setPointSize(12)
            table.verticalHeader().setFont(f)

            f.setPointSize(14)
            table.setFont(f)
            # 行表头隐藏
            table.verticalHeader().hide()

            # 内容居中
            for row in range(table.rowCount()):
                self.set_item_completer(table, row, 0)

            table.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
            table.verticalHeader().setDefaultAlignment(Qt.AlignCenter)

            groupBoxInnerLayout.addWidget(table)
            groupBox.setLayout(groupBoxInnerLayout)
            groupBoxLayout.addWidget(groupBox)
            self.tables.append(table)
        self.layout.addLayout(groupBoxLayout)

        # 总计价格
        priceLayout = QHBoxLayout()
        priceLabel = QLabel('总计价格：')
        priceLabel.setFont(font)
        self.priceEdit = QLineEdit()
        self.priceEdit.setFixedHeight(40)
        self.priceEdit.setFont(font)

        priceLayout.addWidget(priceLabel)
        priceLayout.addWidget(self.priceEdit)
        self.layout.addLayout(priceLayout)

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

        # 保存按钮
        saveButton = QPushButton('仅保存')
        saveButton.setFixedHeight(40)
        saveButton.setFont(font)
        saveButton.clicked.connect(self.saveForm)

        moreLessLayout = QHBoxLayout()
        moreLessLayout.addWidget(moreButton)
        moreLessLayout.addWidget(lessButton)
        moreLessLayout.addWidget(saveButton)
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
        self.resize(1440, 720)
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
                self.set_item_completer(table, row, 0)

    def removeRows(self):
        for table in self.tables:
            currentRowCount = table.rowCount()
            if currentRowCount > 10:
                table.setRowCount(currentRowCount - 10)

    def printForm(self):
        self.save_and_print(print_out=True)

    def saveForm(self):
        self.save_and_print(print_out=False)

    def save_and_print(self, print_out):
        name = self.nameEdit.text()
        gender = '男' if self.maleRadio.isChecked() else '女'
        age = self.ageEdit.text()
        price = self.priceEdit.text()
        drugs = [[] for _ in range(4)]

        for i, table in enumerate(self.tables):
            for row in range(table.rowCount()):
                drugItem = table.cellWidget(row, 0)
                if drugItem:
                    drugs[i].append(drugItem.text())

        nowtime = datetime.datetime.now()
        date_str = nowtime.strftime("%Y-%m-%d")

        # 存储Excel文件
        timestamp = nowtime.strftime("%Y-%m-%d_%H-%M-%S")
        filepath = f"d:/输液单/{nowtime.strftime('%Y')}/{nowtime.strftime('%m')}/{nowtime.strftime('%d')}/{timestamp}_{name}.xlsx"
        save_to_excel(filepath, name, gender, age, drugs, date_str, price)

        if print_out:
            # 打印Excel中的“打印页”
            self.print_excel(filepath)
        else:
            QMessageBox.information(self, "保存成功", f"输液单已保存到: {filepath}")

    '''
    xl纸10x14    16    10 英寸x 14 英寸
    xl纸11x17    17    11 英寸x 17 英寸
    xl论文A3    8    A3 （297 毫米 x 420 毫米）
    xlPaperA4 （英语）    9    A4 （210 毫米 x 297 毫米）
    xlPaperA4小    10    A4 小尺寸 （210 mm x 297 mm）
    xlPaperA5 （英语）    11    A5 （148 毫米 x 210 毫米）
    xlPaperB4 （英语）    12    B4 （250 毫米 x 354 毫米）
    xlPaperB5 （英语）    13    A5 （148 毫米 x 210 毫米）
    '''

    def print_excel(self, filepath):
        excel = win32.Dispatch('Excel.Application')
        excel.Visible = False
        workbook = excel.Workbooks.Open(filepath)
        sheet = workbook.Sheets('打印页')
        sheet.PageSetup.PaperSize = 11  # A5
        # 打印边距 0.5cm
        sheet.PageSetup.LeftMargin = 0.5
        sheet.PageSetup.RightMargin = 0.5
        sheet.PageSetup.TopMargin = 0.5
        sheet.PageSetup.BottomMargin = 0.5

        # Try to catch and handle potential errors in the print process
        try:
            sheet.PrintOut()
        except Exception as e:
            QMessageBox.critical(self, "打印错误", f"打印时发生错误: {e}")
            print(f"An error occurred: {e}")
        finally:
            workbook.Close(False)
            excel.Quit()

    def resetForm(self):
        self.nameEdit.clear()
        self.genderGroup.setExclusive(False)
        self.maleRadio.setChecked(True)
        self.femaleRadio.setChecked(False)
        self.genderGroup.setExclusive(True)
        self.ageEdit.clear()
        self.priceEdit.clear()
        for table in self.tables:
            table.clearContents()
            for row in range(table.rowCount()):
                self.set_item_completer(table, row, 0)

    def importForm(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "d:/输液单/", "Excel Files (*.xlsx)")
        if filepath:
            name, gender, age, drugs, price = load_from_excel(filepath)
            self.nameEdit.setText(name)
            if gender == '男':
                self.maleRadio.setChecked(True)
            else:
                self.femaleRadio.setChecked(True)
            self.ageEdit.setText(str(age))
            self.priceEdit.setText(str(price))
            # 将 drugs 分成 4 组填入每个表格
            for i, table in enumerate(self.tables):
                group_drugs = drugs[i]
                for row in range(table.rowCount()):
                    if row < len(group_drugs):
                        line_edit = table.cellWidget(row, 0)
                        line_edit.setText(group_drugs[row])
                        line_edit.setAlignment(Qt.AlignCenter)
                    else:
                        line_edit = table.cellWidget(row, 0)
                        line_edit.setText('')
                        line_edit.setAlignment(Qt.AlignCenter)
