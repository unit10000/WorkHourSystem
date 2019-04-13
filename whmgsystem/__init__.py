# 增加对pyinstaller生成exe的支持
import os
import sys
from flask import Flask, render_template,Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from whmgsystem.conf import config_db
from whmgsystem.jinja2_fun import get_length,workHour
if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)
#初始化flask_login
login_manager = LoginManager(app)
login_manager.login_view = 'login'#定义登陆路由
#初始化SQLAlchemy
app.config.from_object(config_db)
db = SQLAlchemy(app)
#使用flask对jinja2环境变量操作，来完成jinja2全局函数的配置
app.add_template_global(get_length, 'get_length')
app.add_template_global(workHour.sum_work_hours, 'sum_work_hours')
app.add_template_global(workHour.marge_work_hours, 'marge_work_hours')
#引入view
import whmgsystem.views