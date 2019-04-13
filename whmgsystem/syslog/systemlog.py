# -*- coding: utf-8 -*-

#######################################################
# FileName: systemlog.py
# Description: 系统日志相关的API函数
#######################################################

import logging

from whmgsystem import app
from whmgsystem.conf import setting


#初始化日志管理
def log_init():
    logHandler = logging.FileHandler(setting.LOG_NAME, encoding='UTF-8')
    log_setLevel(logHandler)
    log_setFormat(logHandler)
    return logHandler

#设置日志级别
def log_setLevel(logHandler):
    logHandler.setLevel(logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

#设置日志格式
def log_setFormat(logHandler):
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s'
        )
    logHandler.setFormatter(logging_format)

#Info级别的日志
def log_info(msg):
    app.logger.info(msg)

#Debug级别的日志
def log_debug(msg):
    app.logger.debug(msg)

#Warning级别的日志
def log_warning(msg):
    app.logger.warning(msg)

#Error级别的日志
def log_error(msg):
    app.logger.error(msg)