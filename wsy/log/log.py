# -*- coding: ut8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-20 11:34:28
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-25 14:59:34
import contextlib
import os
import sys
from random import choice
from typing import Generator

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


@contextlib.contextmanager
def HidePrint() -> Generator[None, None, None]:
    """
    Hide Print
    --------
    Usages:
    --------
        >>> with HidePrint():
        >>>     print("Text that needs to be hidden.")
    """
    try:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = open(os.devnull, "w")
        sys.stderr = open(os.devnull, "w")
        yield
    except Exception as e:
        sys.stdout.close()
        sys.stdout = original_stdout  # type: ignore
        print(e.args[0])
        sys.stdout = open(os.devnull, "w")
    finally:
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = original_stdout  # type: ignore
        sys.stderr = original_stderr  # type: ignore


if __name__ == "__main__":
    wprint(123, "red")
    wprint(123)
    wprint(123, "grey")
    with HidePrint():
        print(111)
        ic(0)
    ic(__name__)
