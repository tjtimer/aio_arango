# aio_arango constants
# created: 05.07.18
# Author: Tim "tjtimer" Jedro
# Email: tjtimer@gmail.com
import enum


class Role(enum.Enum):
    admin = 0
    anonymus = 1
    member = 2
    editor = 3
    test = 667
