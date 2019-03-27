#-*- coding: utf-8 -*-
#---------------------------------------------------
#     名称：射箭比赛赛事管理系统(局域网服务版)
# 当前版本：1.4.1[版本年份,内核架构更新, 功能性更新, Bug更新]
# 开发人员：吴烜圣
# 启动时间：2017年11月 4日
# 最近更新：2018年05月11日
# 竣工时间：
#---------------------------------------------------
import gc
import os
import random
import sqlite3 as sql
import sys
import threading
import time
import warnings

import wx
import wx.lib.buttons as buttons

import accredit_functions as AF
import desktop
import global_functions as gb_f
import global_variables as gb_v
import installer
import L3_Dialog as L3
import L4_Dialog as L4
import threads
import win32api

__version__ = u'2.1.0'
gb_v.update = '6th Mar, 2019'
gb_v.version = __version__
#############################################################################################################################
#-- 初始化设置 --#
def Setting():
    stdi,stdo,stde = sys.stdin,sys.stdout,sys.stderr
    reload(sys)                                                 #重新加载sys组件
    sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde
    sys.setdefaultencoding('utf-8')                             #重新设定默认解码方式
    warnings.filterwarnings('ignore')                           #取消警告
    os.chdir(os.path.split(sys.argv[0])[0])                     #重定向工作目录
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    return bundle_dir.decode('cp936')
##############################################################################################################################
#############################################################################################################################
#############################################################################################################################        
#-- 登入界面（界面 & 线程） --# LEVEL:0
class MainRunner(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self,parent,style=wx.DEFAULT_FRAME_STYLE^(wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU),
                          title='赛事管家-Lite')
        self.CenterOnScreen()
        #设置图标
        icons = wx.Icon(gb_v.addr + '/Source/archery.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(icons)
        
        if os.path.isfile('database/registry.bat'):
            self.runner()
        else:
            version = 'Lite-'+__version__[7:]
            name = os.path.split(sys.argv[0])[1]
            setup = installer.Setup(self, version, name)
            if setup.register:
                self.desktop = desktop.Desktop(self)
                self.desktop.Show()
                self.Hide()
            del setup
        
    def runner(self):
        #重载数据库
        if not (gb_f.CopyDB('database/DB.bat', 'database/Archery.db', True) or gb_f.CopyDB('database/CopyDB.bat','database/Archery.db',True)):
            wx.MessageBox('重载数据库失败，请确认数据文件安全。', '赛事管家-Lite', wx.ICON_ERROR)
            return
        
        #用户登入界面
        self.Login()
        
        #启动主界面
        if gb_v.LOGIN:
            self.desktop = desktop.Desktop(self)
            self.desktop.Show()
            self.Hide()
        else:
            self.Close()
    def OnClose(self,evt):
        evt.Skip()
        
    #-- 登陆系统页面 --#
    def Login(self):
        dlg = desktop.LoginWindow(self)
        dlg.ShowModal()
        dlg.Destroy()

                         
#############################################################################################################################

#-- 客户端运行进程 --#
if __name__ == '__main__':
    gb_v.addr = Setting().replace('\\', '/')
    app = wx.App(None)
    runner = MainRunner(None)
    gb_v.windows_desktop = runner
    app.MainLoop()
    app.Destroy()
