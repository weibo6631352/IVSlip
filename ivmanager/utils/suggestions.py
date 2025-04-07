"""
药品建议数据模块
"""

import json
import os
from ivmanager.core.app import get_resource_path


def load_suggestions():
    """
    加载药品名称建议列表
    
    Returns:
        药品名称列表
    """
    config_path = get_resource_path('resources/config/suggestions.json')
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            suggestions = json.load(f)['药品']
        return suggestions
    except Exception as e:
        print(f"加载药品建议数据出错: {e}")
        return []  # 出错返回空列表 