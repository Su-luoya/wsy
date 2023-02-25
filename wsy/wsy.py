# -*- coding: utf-8 -*-
# @Author: 昵称有六个字
# @Date:   2022-10-18 01:02:30
# @Last Modified by:   昵称有六个字
# @Last Modified time: 2023-02-23 18:20:46
from pprint import pprint

import pretty_errors
from icecream import ic

ic.configureOutput(prefix="")


def welcome():
    ic("Welcome to use wsy!")


if __name__ == "__main__":
    welcome()
