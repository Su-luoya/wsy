# -*- coding: utf-8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-20 11:34:28
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-23 18:22:28
import contextlib
import os
from random import choice

import pretty_errors
from termcolor import colored, cprint


def wprint(content, color=None):
    """Colorful output
    Args:
        content (_type_): Anything you want.
        color (str): Choose from ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan'].
        Nothing passed in → random color.
    """
    color_list = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan"]
    if color not in color_list:
        cprint(text=content, color=choice(color_list), attrs=["bold"])
    else:
        cprint(text=content, color=color, attrs=["bold"])


def hide():
    """Hide text (print in grey)"""
    print(f"\033[0;30;40m", end="")


def show():
    """Show text (back in white)"""
    print(colored("", "white"), end="")


def makedir(path=".", name="wsydir"):
    """Make a empty directory

    Args:
        path (str): Directory Path. Defaults to '.'.
        name (str): Directory Name. Defaults to 'wsydir'.
    """
    with contextlib.suppress(Exception):
        os.mkdir(f"{path}\\{name}")


def checkfile(path):
    """Check File existence
    Args:
        path (str): file path
    Returns:
        Bool: exist → True
    """
    return os.path.isfile(path)


if __name__ == "__main__":
    print(checkfile(r"StockData Cache\stock data\stocks_info.csv"))
    # makedir(path='.', name='dir')
    wprint(123, "red")
    hide()
    print(1)
    show()
    wprint(1)
    print(__name__)
