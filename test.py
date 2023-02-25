# -*- coding: utf-8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-18 10:38:30
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-25 00:42:48

from typing import Callable

import pandas as pd
from icecream import ic


def apply_function(func: Callable[..., int]) -> str:
    """
    Applies a function to an integer and returns the result.

    :param func: The function to apply.
    :param x: The integer to apply the function to.
    :return: The result of applying the function to the integer.
    """
    return f"{func()}"


def double() -> int:
    """
    Doubles an integer.

    :param x: The integer to double.
    :return: The doubled integer.
    """
    return 1


result = apply_function(double)
print(result)  # Output: 10
