"""
资源处理工具模块
"""
import os
import sys


def get_resource_path(relative_path):
    """
    获取资源的绝对路径，支持开发环境和PyInstaller打包后的环境
    
    Args:
        relative_path: 相对于资源目录的路径
        
    Returns:
        绝对路径字符串
    """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller打包后的环境
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # 开发环境
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # 不需要转换的路径直接返回
        return os.path.join(base_path, 'ivmanager', relative_path) 