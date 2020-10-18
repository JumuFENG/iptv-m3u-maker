# -*- coding: utf-8 -*-

import os
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
            info['level'] = self.T.getLevel(info['name'])
            info['quality'] = self.T.getQuality(info['name'])
            info['cros'] = 1 if self.T.chkCros(info['url']) else 0
            info['online'] = 0
            info['failcount'] = 0
            info['udTime'] = self.now
            m3uItems.append(info)
        return m3uItems

    def onCompleted(self):
        for parent, dirs, files in os.walk('./plugins/playlists'):
            for f in files:
                os.remove(parent + os.sep + f)
