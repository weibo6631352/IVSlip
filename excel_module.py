import os
import shutil
import xlwings as xw

def save_to_excel(filepath, name, gender, age, drugs, date_str, price):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # 拷贝Excel模板
    template_path = './输液单.xlsx'
    shutil.copy(template_path, filepath)

    app = xw.App(visible=False)
    workbook = app.books.open(filepath)

    # 更新打印页
    print_sheet = workbook.sheets['打印页']
    print_sheet.range('B4').value = name
    print_sheet.range('D4').value = gender
    print_sheet.range('F4').value = age

    print_sheet.range('B7').value = name
    print_sheet.range('D7').value = gender
    print_sheet.range('F7').value = age

    print_sheet.range('B10').value = name
    print_sheet.range('D10').value = gender
    print_sheet.range('F10').value = age

    print_sheet.range('B13').value = name
    print_sheet.range('D13').value = gender
    print_sheet.range('F13').value = age

    print_sheet.range('E15').value = date_str
    print_sheet.range('A15').value = price  # 更新总计价格

    for i in range(4):
        details = ' ;; '.join([f"{drug}" for drug in drugs[i] if drug])
        if i == 0:
            print_sheet.range('A5').value = details
        elif i == 1:
            print_sheet.range('A8').value = details
        elif i == 2:
            print_sheet.range('A11').value = details
        elif i == 3:
            print_sheet.range('A14').value = details

    # 更新数据页
    data_sheet = workbook.sheets['数据页']
    data_sheet.range('B1').value = '姓名'
    data_sheet.range('C1').value = name
    data_sheet.range('B2').value = '性别'
    data_sheet.range('C2').value = gender
    data_sheet.range('B3').value = '年龄'
    data_sheet.range('C3').value = age
    data_sheet.range('B4').value = '打印日期'
    data_sheet.range('C4').value = date_str
    data_sheet.range('B5').value = '总计价格'
    data_sheet.range('C5').value = price

    for i in range(4):
        col_start = 2 + i * 3  # 每联开始的列，间隔3列
        data_sheet.range((6, col_start)).value = f'第{i + 1}联'
        for j in range(len(drugs[i])):
            data_sheet.range((7 + j, col_start)).value = drugs[i][j]

    workbook.save(filepath)
    workbook.close()
    app.quit()

def load_from_excel(filepath):
    app = xw.App(visible=False)
    workbook = app.books.open(filepath)
    data_sheet = workbook.sheets['数据页']
    name = data_sheet.range('C1').value
    gender = data_sheet.range('C2').value
    age = data_sheet.range('C3').value
    date_str = data_sheet.range('C4').value
    price = data_sheet.range('C5').value
    drugs = [[] for _ in range(4)]
    for i in range(4):
        col_start = 2 + i * 3  # 每联开始的列，间隔3列
        row = 7
        for _ in range(50):
            drug = data_sheet.range((row, col_start)).value
            if drug:
                drugs[i].append(drug)
            row += 1
    workbook.close()
    app.quit()
    return name, gender, age, drugs, price