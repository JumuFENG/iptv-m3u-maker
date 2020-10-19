#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tools
import db
import time
import re
import json
import os
from plugins import base
# from plugins import lista
from plugins import listb
from plugins import m3udetector
from plugins import m3uparser
from plugins import dbchecker

class Iptv (object):

    def __init__ (self) :
        self.T = tools.Tools()
        self.DB = db.DataBase()

    def run(self) :
        self.T.logger("开始抓取", True)

        self.DB.chkTable()

        # Base = base.Source()
        # Base.getSource()

        # dbchk = dbchecker.DbChecker(chkall=False)
        # dbchk.getSource()

        m3u = m3udetector.Source()
        m3u.getSource()

        self.outPut()
        # self.outJson()

        self.T.logger("抓取完成")

    def outPut (self) :
        self.T.logger("正在生成m3u8文件")

        sql = """SELECT * FROM %s 
            WHERE online = 1 and delay < 500 
            ORDER BY level ASC, length(name) ASC, delay ASC 
            """ % (self.DB.table)
        result = self.DB.query(sql)

        items = []
        for r in result :
            item = self.DB.fmtDbData(r)
            if 'title' not in item or item['title'] is None or len(item['title']) == 0:
                className = '其他频道'
                if item['level'] == 1 :
                    className = '中央频道'
                elif item['level'] == 2 :
                    className = '地方频道'
                elif item['level'] == 3 :
                    className = '地方频道'
                elif item['level'] == 7 :
                    className = '广播频道'
                else :
                    className = '其他频道'
                item['title'] = className
            items.append(item)

        self.T.logger("共" + str(len(items)) + "项")
        parser = m3uparser.M3uParser()
        parser.items = items
        parser.write_to_file(os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('python', 'http'), 'iptv.m3u'))

    def outJson (self) :
        self.T.logger("正在生成Json文件")
        
        sql = """SELECT * FROM
            (SELECT * FROM %s WHERE online = 1 ORDER BY delay DESC) AS delay
            GROUP BY LOWER(delay.name)
            HAVING delay.name != '' and delay.name != 'CCTV-' AND delay.delay < 500
            ORDER BY level ASC, length(name) ASC, name ASC
            """ % (self.DB.table)
        result = self.DB.query(sql)

        fmtList = {
            'cctv': [],
            'local': [],
            'other': [],
            'radio': []
        }

        for item in result :
            tmp = {
                'title': item[1],
                'url': item[3]
            }
            if item[4] == 1 :
                fmtList['cctv'].append(tmp)
            elif item[4] == 2 :
                fmtList['local'].append(tmp)
            elif item[4] == 3 :
                fmtList['local'].append(tmp)
            elif item[4] == 7 :
                fmtList['radio'].append(tmp)
            else :
                fmtList['other'].append(tmp)

        jsonStr = json.dumps(fmtList)

        with open( os.path.join(os.path.dirname(os.path.abspath(__file__)).replace('python', 'http'), 'tv.json'), 'w') as f:
            f.write(jsonStr)

if __name__ == '__main__':
    obj = Iptv()
    obj.run()





