# -*- coding: utf-8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-20 11:34:28
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-25 14:20:34
from random import choice

import pretty_errors
from termcolor import colored, cprint


def wprint(content, color=None) -> None:
    """Colorful output
    Args:
        content (_type_): Anything you want.
        color (str): Choose from ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan'].
        Nothing passed in → random color.
    """
    color_list: list[str] = ["grey", "red", "green", "yellow", "blue", "magenta", "cyan"]
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



if __name__ == "__main__":
    # makedir(path='.', name='dir')
    wprint(123, "red")
    hide()
    print(1)
    show()
    wprint(1)
    print(__name__)
