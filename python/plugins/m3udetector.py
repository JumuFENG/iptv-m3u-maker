# -*- coding: utf-8 -*-

from .detectbase import DetectorBase
from .m3uparser import M3uParser

class Source(DetectorBase):
    """ detector for m3u files """
    def getTitleUrl(self):
        sourceUrls = []
        parser = M3uParser()
        parser.decodeM3u('./plugins/m3u_source')
        items = parser.items
        for it in items:
            if 'name' in it and 'url' in it:
                sourceUrls.append((it['name'], it['url']))

        return sourceUrls
