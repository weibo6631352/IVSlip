# 输液单管理系统

输液单管理系统是一个用于诊所管理患者输液单的桌面应用程序。

## 启动方式

```bash
start.bat          # 显示主菜单
start.bat run      # 直接启动应用程序
```

## 项目结构

```
.
├── README.md                  # 项目说明文档
├── start.bat                  # 启动批处理文件
├── requirements.txt           # 依赖列表
├── ivmanager/                 # 主包目录
│   ├── core/                  # 核心功能模块
│   ├── ui/                    # 用户界面模块
│   ├── utils/                 # 工具函数
│   ├── resources/             # 资源文件
│   ├── run.py                 # 启动脚本
│   └── __init__.py            # 包初始化文件
└── scripts/                   # 脚本目录
    └── build/                 # 构建脚本
        └── build.bat          # 构建批处理文件
```

## 依赖项

- Python 3.8+
- PyQt5
- openpyxl
- pywin32
- psutil

## 安装和运行

1. 安装依赖：
   ```bash
   start.bat  # 选择"2. 安装依赖"
   ```

2. 运行应用：
   ```bash
   start.bat run
   ```

3. 构建可执行文件：
   ```bash
   start.bat  # 选择"3. 构建应用"
   ```

## 主要功能

- 输液单信息录入
- 打印输液单
- 保存输液单数据
- 导入历史输液单

## 快捷键

- Ctrl+S：保存表单
- Ctrl+P：打印表单
- Ctrl+R：重置表单
- Ctrl+O：导入表单
- Alt+1/2/3/4：切换表格
- F1：显示帮助 