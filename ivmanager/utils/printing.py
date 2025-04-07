"""
打印处理模块
"""

import win32com.client as win32


def print_excel(filepath):
    """
    打印Excel文件
    
    Args:
        filepath: 要打印的Excel文件路径
    """
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
        print(f"正在打印: {filepath}")
    except Exception as e:
        print(f"打印时发生错误: {e}")
    finally:
        try:
            workbook.Close(False)
            excel.Quit()
        except:
            pass 