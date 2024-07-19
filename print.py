import sys
import os
import win32com.client as win32
from PyQt5.QtWidgets import QApplication, QFileDialog


def print_excel(filepath):
    excel = win32.Dispatch('Excel.Application')
    excel.Visible = False
    try:
        workbook = excel.Workbooks.Open(filepath)
        sheet = workbook.Sheets(1)  # 打印第一页
        sheet.PageSetup.PaperSize = 11  # A5纸张
        sheet.PageSetup.LeftMargin = 0.5  # 设置打印边距
        sheet.PageSetup.RightMargin = 0.5
        sheet.PageSetup.TopMargin = 0.5
        sheet.PageSetup.BottomMargin = 0.5

        sheet.PrintOut()  # 打印
    except Exception as e:
        print(f"打印时发生错误: {e}")
    finally:
        workbook.Close(False)
        excel.Quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    if len(sys.argv) < 2:
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Excel Files (*.xlsx)")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        # 默认目录d:/输液单/
        file_dialog.setDirectory('d:/输液单/')
        if file_dialog.exec_():
            file_paths = file_dialog.selectedFiles()
            if file_paths:
                filepath = file_paths[0]
            else:
                print("未选择文件")
                sys.exit(1)
        else:
            print("未选择文件")
            sys.exit(1)
    else:
        filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print(f"文件不存在: {filepath}")
        sys.exit(1)

    if not filepath.lower().endswith('.xlsx'):
        print("请提供一个Excel文件 (*.xlsx).")
        sys.exit(1)

    print_excel(filepath)
    print("打印完成.")
    sys.exit(0)