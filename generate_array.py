#!/usr/bin/env python
# -*- coding: utf8 -*-

__author__ = '3eca'
__github__ = 'https://github.com/3eca'


def generate(array: list):
    for file in range(0, len(array), 9):
        yield array[file:file + 9]


if __name__ == '__main__':
    pass
