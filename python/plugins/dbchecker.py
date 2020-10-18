# -*- coding: utf-8 -*-

import db
from .detectbase import DetectorBase

class DbChecker(DetectorBase):
    """check the urls in DB"""   
    def __init__(self, chkall=False):
        super(DbChecker, self).__init__()
        self.checkAll = chkall

    def getItems(self):
        dbItems = []
        DB = db.DataBase()
        sql = 'SELECT * FROM %s' % DB.table
        if not self.checkAll:
            sql += ' WHERE online = 0'

        result = DB.query(sql)
        for r in result:
            dbItems.append(DB.fmtDbData(r))
        return dbItems
