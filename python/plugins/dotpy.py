#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .detectbase import DetectorBase

class Source(DetectorBase):
    """ detector for dotpy_source """
    def getTitleUrl(self):
        sourcePath = './plugins/dotpy_source'
        sourceUrls = []
        with open(sourcePath, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            total = len(lines)

            for i in range(0, total):
                line = lines[i].strip('\n')
                item = line.split(',', 1)
                sourceUrls.append((item[0], item[1]))

        return sourceUrls
