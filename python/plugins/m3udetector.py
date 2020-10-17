# -*- coding: utf-8 -*-

from .detectbase import DetectorBase
from .m3uparser import M3uParser

class Source(DetectorBase):
    """ detector for m3u files """
    def getTitleUrl(self):
        sourceUrls = []
        parser = M3uParser()
        parser.decode_all_play_lists('./plugins/playlists')
        items = parser.items
        for it in items:
            if 'name' in it and 'url' in it:
                sourceUrls.append((it['name'], it['url']))

        return sourceUrls
