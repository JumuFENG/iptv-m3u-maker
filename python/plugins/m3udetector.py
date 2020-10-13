# -*- coding: utf-8 -*-

from .detectbase import DetectorBase

class m3uSource(DetectorBase):
    """ detector for m3u files """
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
