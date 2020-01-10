#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib

def outputMD5(info):
    md5 = hashlib.md5()
    md5.update(info.encode('utf-8'))
    return md5.hexdigest()

if __name__ == '__main__':
    print(outputMD5('heihei'))
