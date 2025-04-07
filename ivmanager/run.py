#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
输液单管理系统
启动入口文件
"""

import sys
import os

# 确保可以正确导入项目内的模块
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)

# 导入主函数并运行
from ivmanager.core.app import main

if __name__ == '__main__':
    main() 