#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
系统环境检查工具
用于检查运行环境是否满足要求
"""

import os
import sys
import importlib
import platform
import subprocess

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_python_version():
    """检查Python版本"""
    print(f"Python版本: {platform.python_version()}")
    if sys.version_info < (3, 6):
        print("警告: 推荐使用Python 3.6或更高版本")
        return False
    return True


def check_dependencies():
    """检查依赖项"""
    required_packages = ["PyQt5", "openpyxl", "win32com"]
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"依赖项: {package} - 已安装")
        except ImportError:
            print(f"依赖项: {package} - 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n缺少以下依赖项:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\n请运行以下命令安装依赖项:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def check_files():
    """检查必要文件是否存在"""
    required_files = [
        "app.py", 
        "src/core/main.py",
        "src/ui/ui_module.py",
        "src/utils/excel_module.py",
        "src/utils/suggestion_module.py",
        "src/assets/icon.png",
        "data/templates/输液单.xlsx",
        "src/config/suggestions.json"
    ]
    
    missing_files = []
    
    # 获取脚本所在目录的上一级目录（项目根目录）
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    for file_path in required_files:
        full_path = os.path.join(root_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("\n缺少以下必要文件:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    else:
        print("所有必要文件检查通过")
    
    return True


def check_excel():
    """检查Excel组件"""
    try:
        import win32com.client
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Quit()
        print("Excel组件检查通过")
        return True
    except Exception as e:
        print(f"Excel组件检查失败: {e}")
        return False


def main():
    """主函数"""
    print("正在检查系统环境...\n")
    
    python_ok = check_python_version()
    dependencies_ok = check_dependencies()
    files_ok = check_files()
    excel_ok = check_excel()
    
    print("\n系统检查结果:")
    print(f"Python版本检查: {'通过' if python_ok else '警告'}")
    print(f"依赖项检查: {'通过' if dependencies_ok else '失败'}")
    print(f"文件检查: {'通过' if files_ok else '失败'}")
    print(f"Excel组件检查: {'通过' if excel_ok else '失败'}")
    
    if python_ok and dependencies_ok and files_ok and excel_ok:
        print("\n恭喜！系统环境检查通过，可以正常运行程序。")
        return 0
    else:
        print("\n系统环境检查未通过，请解决上述问题后再运行程序。")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 