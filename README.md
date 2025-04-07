# 输液单管理系统

输液单管理系统是一个用于诊所管理患者输液单的桌面应用程序。

## 启动方式

两种启动方式：

1. 双击 `start.bat` - 显示主菜单，可以选择不同的操作
2. 命令行：`start.bat run` - 直接启动应用程序，不显示菜单

## 项目结构

```
.
├── README.md                  # 项目说明文档
├── start.bat                  # 启动批处理文件
├── requirements.txt           # 依赖列表
│
├── ivmanager/                 # 主包目录
│   ├── __init__.py            # 包初始化文件
│   ├── __main__.py            # 主入口点
│   ├── run.py                 # 启动脚本
│   ├── core/                  # 核心功能模块
│   ├── ui/                    # 用户界面模块
│   ├── utils/                 # 工具函数
│   └── resources/             # 资源文件
│
└── scripts/                   # 脚本目录
    └── build/                 # 构建脚本
        ├── build.bat          # 构建批处理文件
        ├── ivmanager.spec     # PyInstaller规范文件
        └── setup.py           # 安装脚本
```

## 依赖项

- Python 3.8+
- PyQt5
- openpyxl
- pywin32
- psutil

## 安装

```bash
start.bat
```

然后选择 "安装依赖" 选项，或者直接运行：

```bash
pip install -r requirements.txt
```

## 运行

开发环境下运行:

```bash
start.bat run
```

或者通过菜单运行：

```bash
start.bat
```

然后选择 "启动应用程序" 选项

## 构建可执行文件

```bash
start.bat
```

然后选择 "构建应用" 选项，或者直接运行：

```bash
scripts/build/build.bat
```

构建后的文件位于 `dist` 目录中。

## 系统要求

- Windows 7/10/11
- 64位操作系统

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
- Ctrl+A：添加行
- Ctrl+D：删除行
- Alt+1/2/3/4：切换表格
- F1：帮助 