#-*- coding: utf-8 -*-
#---------------------------------------------------
#     名称：射箭比赛赛事管理系统(局域网服务版)
# 当前版本：2.1.1[版本年份,内核架构更新, 功能性更新, Bug更新]
# 开发人员：吴烜圣
# 启动时间：2017年11月04日
# 最近更新：2018年09月28日
# 竣工时间：
#---------------------------------------------------
import gc
import os
import random
import re
import shutil
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

__author__ = 'Xuansheng WU'
__email__ = 'kitgram@163.com'
__platform__ = 'http://www.Kitgram.cn'
__version__ = u'2.1.1'
gb_v.update = '25th Mar, 2019'
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
        #获取背景图片大小
        self.bmp = wx.Bitmap(gb_v.addr + '/Source/windows/LoadingBackground.bmp')
        size=self.bmp.GetWidth(),self.bmp.GetHeight()
        wx.Frame.__init__(self,parent,style=wx.DEFAULT_FRAME_STYLE^(wx.CAPTION|wx.CLOSE_BOX|wx.RESIZE_BORDER|wx.SYSTEM_MENU),
                          title=u'赛事管家-Pro',size=size)
        self.Center()
        self.parent = parent
        #设置图标
        icons = wx.Icon(gb_v.addr + '/Source/archery.ico',wx.BITMAP_TYPE_ICO)
        self.SetIcon(icons)
        #绘制图片
        wx.StaticBitmap(self,-1,self.bmp)
        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.Show()
        
        if os.path.isfile('database/registry.bat'):
            self.runner()
        else:
            version = 'Server-'+__version__[7:]
            name = os.path.split(sys.argv[0])[1]

            setup = installer.Setup(self, version, name)
            if setup.register:
                self.desktop = desktop.Desktop(self)
                self.desktop.Show()
                self.Hide()
            else:
                self.Close()
        
    def runner(self):
        #授权检测
        try:
            LocalDiskNo = AF.Accredit(gb_f.DiskInfo()[0].ID)[0]
        except:
            wx.MessageBox('授权验证出错，请确认校检文件正常并且未插入未知U盘。', '赛事管家-Pro', wx.ICON_ERROR)
            self.Close()
        else:
            AppNo = AF.Encode_StableDic(self.CheckLocalAuthorization())

        if AppNo == '4IA8N35I6':
            wx.MessageBox('您正在通过临时授权码使用本软件, 本授权请勿删除：database/register.bat文件！', '赛事管家-Pro')
            
        elif LocalDiskNo != AppNo:
            wx.MessageBox('检测到您在未被授权的电脑上使用本软件！','赛事管家-Pro',wx.ICON_ERROR)
            self.Close()
            
        #重载数据库
        if not (gb_f.CopyDB('database/DB.bat', 'database/Archery.db', True) or gb_f.CopyDB('database/CopyDB.bat','database/Archery.db',True)):
            wx.MessageBox('重载数据库失败，请确认数据文件安全。', '赛事管家-Pro', wx.ICON_ERROR)
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

    #-- 检查本地注册信息 --#
    def CheckLocalAuthorization(self):
        try:
            #连接数据库提取本地注册信息
            if gb_f.CopyDB('database/registry.bat','database/registry.db',True):  
                conn = sql.connect('database/registry.db')
                cur = conn.cursor()
                cur.execute('SELECT AppNo,DateEnd FROM app_Info WHERE LocalID=0')
                AppNo = cur.fetchone()
                conn.close()
                os.remove('database/registry.db')
                date = list(map(int, AppNo[1].split('-')))
                if date[0] >= time.localtime()[0] and date[1] >= time.localtime()[1] and date[2] > time.localtime()[2]:
                    wx.MessageBox('你的授权已过期！','赛事管家-Pro',wx.ICON_ERROR)       
                    return 'False'      
                return str(AppNo[0][:-4])
            else:
                wx.MessageBox('注册信息读取异常！','赛事管家-Pro',wx.ICON_ERROR)
                return 'False'
        except:
            return 'False'
                         
#############################################################################################################################

#-- 客户端运行进程 --#
if __name__ == '__main__':
    gb_v.addr = Setting().replace('\\', '/')
    app = wx.App(None)
    runner = MainRunner(None)
    gb_v.windows_desktop = runner
    app.MainLoop()
    app.Destroy()
