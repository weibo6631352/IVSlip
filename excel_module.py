import os
import openpyxl
import shutil


def save_to_excel(filepath, name, gender, age, drugs, quantities, date_str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    # 拷贝Excel模板
    template_path = './输液单.xlsx'
    shutil.copy(template_path, filepath)

    workbook = openpyxl.load_workbook(filepath)

    # 更新打印页
    print_sheet = workbook['打印页']
    print_sheet['B4'] = name
    print_sheet['D4'] = gender
    print_sheet['F4'] = age

    print_sheet['B7'] = name
    print_sheet['D7'] = gender
    print_sheet['F7'] = age

    print_sheet['B10'] = name
    print_sheet['D10'] = gender
    print_sheet['F10'] = age

    print_sheet['B13'] = name
    print_sheet['D13'] = gender
    print_sheet['F13'] = age

    print_sheet['E15'] = date_str

    for i in range(4):
        details = ';'.join([f"{drugs[i][j]}*{quantities[i][j]}" for j in range(len(drugs[i]))])
        if i == 0:
            print_sheet['A5'] = details
        elif i == 1:
            print_sheet['A8'] = details
        elif i == 2:
            print_sheet['A11'] = details
        elif i == 3:
            print_sheet['A14'] = details

    # 更新数据页
    data_sheet = workbook['数据页']
    data_sheet['B1'] = '姓名'
    data_sheet['C1'] = name
    data_sheet['B2'] = '性别'
    data_sheet['C2'] = gender
    data_sheet['B3'] = '年龄'
    data_sheet['C3'] = age
    data_sheet['B4'] = '打印日期'
    data_sheet['C4'] = date_str

    for i in range(4):
        col_start = 2 + i * 3  # 每联开始的列，间隔3列
        data_sheet.cell(row=6, column=col_start).value = f'第{i + 1}联'
        for j in range(len(drugs[i])):
            data_sheet.cell(row=7 + j, column=col_start).value = drugs[i][j]
            data_sheet.cell(row=7 + j, column=col_start + 1).value = quantities[i][j]

    workbook.save(filepath)
    workbook.close()


def load_from_excel(filepath):
    workbook = openpyxl.load_workbook(filepath)
    data_sheet = workbook['数据页']
    name = data_sheet.cell(row=1, column=3).value
    gender = data_sheet.cell(row=2, column=3).value
    age = data_sheet.cell(row=3, column=3).value
    drugs = [[] for _ in range(4)]
    quantities = [[] for _ in range(4)]
    for i in range(4):
        col_start = 2 + i * 3  # 每联开始的列，间隔3列
        row = 7
        for _ in range(50):
            drug = data_sheet.cell(row=row, column=col_start).value
            quantity = data_sheet.cell(row=row, column=col_start + 1).value
            if drug:
                drugs[i].append(drug)
                quantities[i].append(quantity)
            row += 1
    return name, gender, age, drugs, quantities
