#!/usr/bin/python
# -*- coding: utf-8 -*-

__all__ = ['UNKNOWN', 'INFORMATION', 'WARNING', 'ERROR']

# Error levels
UNKNOWN = 0
INFORMATION = 1
WARNING = 2
ERROR = 3

def singleton(cls):
    instances = {}
    def get_instance(*args):
        if cls not in instances:
            instances[cls] = cls(*args)
        return instances[cls]
    return get_instance
