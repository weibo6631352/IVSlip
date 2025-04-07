#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="ivmanager",
    version="1.0.0",
    description="输液单管理系统",
    author="Author",
    author_email="author@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "PyQt5>=5.15.4",
        "openpyxl>=3.0.9",
        "pywin32>=303",
        "psutil>=5.9.0",
    ],
    entry_points={
        "console_scripts": [
            "ivmanager=ivmanager.core.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ],
) 