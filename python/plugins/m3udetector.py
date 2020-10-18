# -*- coding: utf-8 -*-

from .detectbase import DetectorBase
from .m3uparser import M3uParser

class Source(DetectorBase):
    """ detector for m3u files """
    def getItems(self):
        m3uItems = []
        parser = M3uParser()
        parser.decode_all_play_lists('./plugins/playlists')
        for info in parser.items:
            info['delay'] = 0
            info['level'] = self.T.getLevel(it['name'])
            info['quality'] = self.T.getQuality(it['name'])
            info['cros'] = 1 if self.T.chkCros(it['url']) else 0
            info['online'] = 0
            info['failcount'] = 0
            info['udTime'] = self.now
            m3uItems.append(info)
        return m3uItems
