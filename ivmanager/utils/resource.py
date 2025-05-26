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
        base_path = sys._MEIPASS
        resource_path = os.path.join(base_path, relative_path)
        
        # 如果打包后的资源路径不存在，尝试从外部资源目录加载
        if not os.path.exists(resource_path) and os.path.exists('dist'):
            # 可能在构建输出目录中，尝试从同级目录加载
            alt_path = os.path.join(os.path.dirname(sys.executable), relative_path)
            if os.path.exists(alt_path):
                return alt_path
            
            # 最后尝试从dist目录加载
            dist_path = os.path.join(os.path.dirname(sys.executable), 'ivmanager', relative_path)
            if os.path.exists(dist_path):
                return dist_path
        
        return resource_path
    else:
        # 开发环境
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # 不需要转换的路径直接返回
        return os.path.join(base_path, 'ivmanager', relative_path) 