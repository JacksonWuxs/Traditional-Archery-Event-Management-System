#-*- coding: utf-8 -*-
#---------------------------------------------------
#     名称：射箭比赛赛事管理系统(局域网服务版)
# 当前版本：3.0.1[版本年份,内核架构更新, 功能性更新, Bug更新] 中国大学生计算机设计大赛临时授权2019
# 开发人员：吴烜圣
# 启动时间：2017年11月04日
# 最近更新：2019年05月29日
# 竣工时间：
#---------------------------------------------------
import os
import sys
import warnings

from cefpython3 import cefpython as cef

import KitgramPlatform as KP
import global_variables as gb_v

__author__ = 'Xuansheng WU'
__email__ = 'kitgram@163.com'
__platform__ = 'http://www.Kitgram.cn'
__version__ = u'3.0.2'
gb_v.update = '4th Aug, 2019'
gb_v.version = __version__
gb_v.title = '赛事管家（专业版）'


#-- 初始化设置 --#
def Setting():
    stdi,stdo,stde = sys.stdin,sys.stdout,sys.stderr
    reload(sys)                                                 #重新加载sys组件
    sys.stdin, sys.stdout, sys.stderr = stdi, stdo, stde
    sys.setdefaultencoding('utf-8')                             #重新设定默认解码方式
    warnings.filterwarnings('ignore')                           #取消警告
    os.chdir(os.path.split(sys.argv[0])[0])                     #重定向工作目录
    
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        return sys._MEIPASS.decode('cp936')
    # we are running in a normal Python environment
    return os.path.dirname(os.path.abspath(__file__)).decode('cp936')

         
#-- 客户端运行进程 --#
if __name__ == '__main__':
    gb_v.addr_src = Setting().replace('\\', '/')
    gb_v.addr_tmp = (os.environ['TEMP'] + '\\TAEMS').replace('\\', '/')
    gb_v.addr_env = (os.environ['LOCALAPPDATA'] + '\\' + gb_v.title).replace('\\', '/')
    cef.Initialize(settings={})
    app = KP.KitgramApp(None)
    app.MainLoop()
    app.Destroy()
    cef.Shutdown()
