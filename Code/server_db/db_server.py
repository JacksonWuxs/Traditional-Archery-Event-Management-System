# -*- coding: utf-8 -*-
import threading
import cgi
import DaPy as dp
import sqlite3 as sql
from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

dp.io.encode('utf-8')

class UpdateDB(threading.Thread):
    def __init__(self, addr):
        threading.Thread.__init__(self)
        self._data = dp.read(addr)
        self.start()

    def run(self):
        with sql.connect('Archery.db') as conn:
            cur = conn.cursor()
            for name, sheet in zip(self._data.sheets, self._data.data):
                name = name.split(' ')[0]
                cur.execute(u'DROP TABLE IF EXISTS %s' % unicode(name))
                print name, 
                if u'个人排名赛' in name:
                    print 1
                    cur.execute(('CREATE TABLE %s (编号 INTEGER PRIMARY KEY, 姓名 STRING, 单位 STRING, ' % name+\
                                '远距离总分 INTEGER, 中距离总分 INTEGER, 近距离总分 INTEGER, 全距离总分 INTEGER)'))
                    for record in sheet:
                        cur.execute('INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?)' % name, record)

                elif u'决赛' in name or u'铜牌赛' in name or u'半决赛' in name:
                    if u'个人' in name:
                        print 2
                        cur.execute('CREATE TABLE %s (编号 INTEGER PRIMARY KEY, 姓名 STRING, 第1轮 INTEGER, '% name+\
                                    '第2轮 INTEGER, 第3轮 INTEGER, 第4轮 INTEGER, 第5轮 INTEGER, 结果 STRING)')
                        for record in sheet:
                            cur.execute('INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?)' % name, record)

                    if u'团体' in name:
                        print 3
                        cur.execute('CREATE TABLE %s (单位 STRING PRIMARY KEY, 第1轮 INTEGER, 第2轮 INTEGER, 第3轮 INTEGER, ' % name+\
                                    '第4轮 INTEGER, 第5轮 INTEGER, 结果 STRING')
                        for record in sheet:
                            cur.execute('INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?)' % name, record)
                else:
                    
                    if u'个人' in name:
                        print 4
                        cur.execute('CREATE TABLE %s (编号 INTEGER PRIMARY KEY, 姓名 STRING, 的 INTEGER, ' % name +\
                                    '正 INTEGER, 鹄 INTEGER, 侯 INTEGER, 流矢 INTEGER, 总分 INTEGER, 结果 STRING)')
                        for record in sheet:
                            cur.execute('INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)' % name, record)

                    if u'团体'in name:
                        print 5
                        cur.execute('CREATE TABLE %s (单位 STRING PRIMARY KEY, 的 INTEGER, 正 INTEGER, 鹄 INTEGER, ' % name +\
                                    '侯 INTEGER, 流矢 INTEGER, 总分 INTEGER, 结果 STRING)')
                        for record in sheet:
                            cur.execute('INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?, ?, ?)' % name, record)
        print 'Recieve File!'
        
###-- 网络接收文件（线程） --### LEVEL:3
class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        
    def run(self):
        server = HTTPServer(('0.0.0.0', 8000), PostHandler)
        while True:
            server.handle_request()

###-- 网络接受（线程） --###  LEVEL:3
class PostHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            msg = '<html><head><title>赛事管家-主页</title></head><h1 style="text-align:center"> 赛事管家-主页 </h1><body><p style="text-align:center"> 赛事管家服务器已准备就绪...</p><p style="text-align:center"> 请通过软件进行文件传输。</p><br><br><hr /><p style="text-align:center"> Copyright (c) 2018 Xuansheng Wu. All rights reserved.</P><p style="text-align:center"> For more details, see: <a href="https://github.com/JacksonWuxs">HomePage of Author</a></p></body></html>'
            self.wfile.write(msg)
        except IOError:
            self.send_error(404, 'HomePage Not Found.')
        
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type']})
        
        self.send_response(200)
        self.end_headers()
        Infom_List = form.keys()
        with open(form['addr'].value, 'wb') as f:
            f.write(form['data'].value)
        self.wfile.write('RECEIVE')
        UpdateDB(form['addr'].value)

if __name__ == '__main__':
    s = Server()
    s.join()
