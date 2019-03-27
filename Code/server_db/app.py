# coding: utf-8
#########################################
# Author         : Haibo Zhu             
# Email          : haibo.zhu@hotmail.com 
# created        : 2018-11-05 16:54 
# Last modified  : 2018-11-08 15:13
# Filename       : app.py
# Description    :                       
#########################################
from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
import random
from db_init import db
import os
import DaPy as dp

dp.io.encode('utf-8')

db_path = os.path.abspath('.') + "\Archery.db"
def create_app():
  app = Flask(__name__)

  from flask_bootstrap import Bootstrap
  Bootstrap(app)

  app.config['WTF_CSRF_SECRET_KEY'] = 'mysecretkey1234567890'
  app.config['SECRET_KEY'] = 'mysecretkey1234567890'
  app.config['DEBUG'] = False
  app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + db_path
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)

  from flask_sqlite_web.core import sqliteAdminBlueprint
  sqliteAdminBP = sqliteAdminBlueprint(title=u'成绩查询',h1=u'2018中国大学生射箭（射艺）锦标赛-实时成绩查询',dbPath = db_path)
  app.register_blueprint(sqliteAdminBP, url_prefix='/ucac/score')
  app.debug = False
  return app

def setup_database(app):
  with app.app_context():
    db.create_all()
    Example.generate(100)

if __name__ == '__main__':
  app  = create_app()
  if not os.path.isfile(db_path):
    setup_database(app)
  app.run(host='0.0.0.0', port='5000')
