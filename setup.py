# -*- coding: utf-8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-18 00:56:50
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-23 23:12:18
import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wsy",
    version="1.0.0",
    author="昵称有六个字",
    author_email="1931960436@qq.com",
    maintainer="昵称有六个字",
    maintainer_email="1931960436@qq.com",
    description="A package for wsy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Su-luoya",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "statsmodels",
        "matplotlib",
        "plotly",
        "tqdm",
        "pretty_errors",
        "pprint",
        "icecream",
    ],
)
