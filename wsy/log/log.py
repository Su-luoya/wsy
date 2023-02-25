# -*- coding: utf-8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-20 11:34:28
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-25 14:40:34
import os
import sys
from random import choice
from typing import TextIO

import pretty_errors
from icecream import ic
from termcolor import cprint


def wprint(content, color=None) -> None:
    """
    Print colorize text.
    --------
    Args:
    --------
        content (_type_): Anything you want to print.
        color (str): Choose from ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan'].
                            Nothing passed in → Random Color.
    Usages:
    --------
        >>> wprint("Anything you want to print.")
        >>> wprint("Anything you want to print.", color="red")
    """
    color_list: list[str] = [
        "grey",
        "red",
        "green",
        "yellow",
        "blue",
        "magenta",
        "cyan",
    ]
    cprint(
        text=content,
        color=choice(color_list) if color not in color_list else color,
        attrs=["bold"],
    )


class HidePrint:
    """
    Hide Print
    --------
    Usages:
    --------
        >>> with HidePrint():
        >>>     print("Text that needs to be hidden.")
    """

    def __enter__(self) -> None:
        self._original_stdout: TextIO = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        sys.stdout.close()
        sys.stdout = self._original_stdout


if __name__ == "__main__":
    wprint(123, "red")
    wprint(123)
    wprint(123, "grey")
    with HidePrint():
        print(111)
    ic(__name__)
