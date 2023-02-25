# -*- coding: utf-8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-18 10:14:16
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-23 18:23:09
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

mpl.rcParams['font.family'] = 'serif'
plt.style.use('seaborn')
plt.rcParams['font.sans-serif'] = ['Simhei']  # 解决中文显示问题，目前只知道黑体可行
plt.rcParams['axes.unicode_minus'] = False  # 解决负数坐标显示问题

class Plot(object):
    
    def __init__(self, xlabel='x', ylabel='y', title='wsy plot', legend=True):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        if legend:
            plt.legend(loc=0)
    
    def bar(self):
        pass



if __name__ == '__main__':
    p = Plot()
    
      