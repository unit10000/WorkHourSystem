from flask_login import current_user,login_required
from flask import render_template, url_for, session, request, redirect, flash
from functools import wraps
import json
def admin_required(func):
    '''
    检查管理员权限装饰器
    :param func:
    :return:
    '''
    #wraps装饰器可以解决view中只能引入一个视图的的错误
    @login_required
    @wraps(func)
    def admin(*args, **kw):
        if current_user.status < 5:
            return render_template('alert.html', message="您的账号没有权限！")
        return func(*args, **kw)
    return admin
def super_admin_required(func):
    '''
    检查超级管理员权限装饰器
    :param func:
    :return:
    '''
    #wraps装饰器可以解决view中只能引入一个视图的的错误
    @login_required
    @wraps(func)
    def super_admin(*args, **kw):
        if current_user.status < 150:
            return render_template('alert.html', message="您的账号没有权限！")
        return func(*args, **kw)
    return super_admin
def api_required(func):
    '''
    api权限装饰器
    :param func:
    :return:
    '''
    @wraps(func)
    def api(*args, **kw):
        if not current_user.is_authenticated:
            str_json = {}
            str_json['status']=False
            str_json['message'] = '请先登陆！'
            return json.dumps(str_json)
        return func(*args, **kw)
    return api