# -*- coding: utf-8 -*-

#######################################################
# FileName: setting.py
# Description: 系统配置变量，全局变量
#######################################################

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# 系统日志文件名
LOG_NAME = "whmg.log"
#表格文件路径
XLSX_NAME = "test.xlsx"
#项目工作路径
WORK_PATH=''
#存放公司log路径
company_log_path=''

STR_SUCCESS ="操作成功！"
STR_ERROR = "操作失败！"
STR_DATA_ERROR = "提交参数错误！"
#金蝶数据库链接配置
dbpool_jindee={}
