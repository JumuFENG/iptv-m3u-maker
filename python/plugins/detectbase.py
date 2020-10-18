# -*- coding: utf-8 -*-

import tools
import time
import db
import threading
from .threads import ThreadPool

class DetectorBase(object):
    """the base class for detecting"""
    def __init__(self):
        self.T = tools.Tools()
        self.now = int(time.time() * 1000)

    def getItems(self):
        pass

    def getSource(self):
        sourceItems = self.getItems()
        threads = ThreadPool(20)
        for info in sourceItems:
            threads.add_task(self.checkData, item = info)
        threads.wait_completion()

    def checkData(self, item):
        if 'url' in item and len(item['url']) > 0:
            self.T.logger('正在分析[ %s ]: %s' % (item['name'], item['url']))
            netstat = self.T.chkPlayable(item['url'])
            item['online'] = 1 if netstat > 0 else 0
            item['delay'] = netstat
            item['udTime'] = self.now
            if netstat == 0:
                item['failcount'] += 1
            self.addData(item)

    def addData (self, data) :
        DB = db.DataBase()
        sql = "SELECT * FROM %s WHERE url = '%s'" % (DB.table, data['url'])
        result = DB.query(sql)

        if len(result) == 0 :
            DB.insert(data)
        else :
            id = result[0][0]
            if data['failcount'] >= 10:
                DB.delete(id)
            else:
                DB.edit(id, data)
