from whmgsystem.model import *
from flask_login import login_user,login_required,current_user,logout_user
from whmgsystem import db
from whmgsystem.syslog import systemlog
from whmgsystem.conf.setting import STR_SUCCESS,STR_ERROR
from whmgsystem.utils import strUtils,MD5utils
def login(user_name,user_pass):
    '''
    用户登陆
    :param user_name: 用户name
    :param user_pass: 用户密码
    :return:
    '''
    ret = {}
    ret['isTrue'] = False
    strList = []
    strList.append(user_name)
    strList.append(user_pass)
    if strUtils.isLegals(strList) == False:
         ret['alert'] = "账号密码不能为空、含有空字符!"
    else:
        user = User.query.filter(User.user == user_name, User.pw == MD5utils.getMD5(user_pass)).first()
        if user:
            if user.status > -1:
                login_user(user)
                ret['isTrue'] = True
                #return redirect(url_for('index'))
            else:
                ret['alert'] = "账号异常!"
        else:
            ret['alert'] ="账号密码错误"
    return ret
# def register(user_name,user_pass,department_id):
#     strList = []
#     strList.append(user_name)
#     strList.append(user_pass)
#     if int(department_id) < 0:
#         message="注册失败，请选择部门！"
#     elif strUtils.isLegals(strList) == False:
#         message="账号、密码、不能为空、含有空字符"
#     else:
#         try:
#             user = User(user=user_name, pw=MD5utils.getMD5(user_pass), department_id=department_id,company_id=current_user.company_id)
#             db.session.add(user)
#             db.session.commit()
#             message = STR_SUCCESS
#         except:
#             message = STR_ERROR
#     return message
def register(user_name,user_pass,department_id,company_id,status):
    '''
    用户注册
    :param user_name: 用户名称
    :param user_pass: 用户密码
    :param department_id: 用户部门
    :param company_id: 用户公司
    :param status: 用户状态
    :return:
    '''
    strList = []
    strList.append(user_name)
    strList.append(user_pass)
    if int(status) < 10:
        if int(department_id) < 0:
            message="注册失败，请选择部门！"
            return message
    if strUtils.isLegals(strList) == False:
        message="账号、密码、不能为空、含有空字符"
    else:
        try:
            user = User(user=user_name, pw=MD5utils.getMD5(user_pass), department_id=department_id,company_id = company_id,status =status)
            db.session.add(user)
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message

def up_user_status(user_id,status):
    '''
    更新用户状态
    :param user_id: 用户id
    :param status: 用户状态
    :return:
    '''
    try:
        user = User.query.get(int(user_id))
        user.status = status
        db.session.commit()
        message = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        message = STR_ERROR
    return message
def registerSuper(user_name,user_pass,status):
    '''
    注册管理员
    :param user_name: 用户name
    :param user_pass: 用户密码
    :param status: 用户级别
    :return:
    '''
    strList = []
    strList.append(user_name)
    strList.append(user_pass)
    if strUtils.isLegals(strList) == False:
        message="账号、密码、不能为空、含有空字符"
    else:
        try:
            user = User(user=user_name, pw=MD5utils.getMD5(user_pass), status=status,department_id=-1)
            db.session.add(user)
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message
def get_user_by_department(department_id):
    '''
    获取某部门用户列表
    :param department_id:部门id
    :return:
    '''
    users = User.query.filter(User.department_id == department_id).filter(User.status > -1).all()
    retuser = []
    for u in users:
        user = {}
        user['id'] = u.id
        user['name'] = u.user
        retuser.append(user)
    return retuser
def delete(user_id):
    '''
    删除用户
    :param user_id: 用户id
    :return:
    '''
    if user_id == None or user_id == "":
        message = '用户id不能为空'
    else:
        try:
            user = User.query.get(int(user_id))
            print(user)
            db.session.delete(user)
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message
def is_init():
    '''
    系统是否初始化
    :return:
    '''
    isTrue = False
    try:
        user = User.query.filter().first()
        if user:
            isTrue = True
    except Exception as e:
        systemlog.log_error(e)
    return isTrue
def up_user_department(department_id ,user_id):
    '''
    跟新用户部门
    :param department_id:
    :param user_id:
    :return:
    '''
    message = STR_ERROR
    try:
        department = Department.query.get(int(department_id))
        if department:
            user = User.query.get(int(user_id))
            if user:
                user.department_id = department_id
                db.session.commit()
                message  = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
    return message
def up_user_pw(u_id,old_pw,new_pw1,new_pw2):
    '''
    修改用户密码
    :param u_id: 用户id
    :param old_pw: 旧密码
    :param new_pw1: 新密码
    :param new_pw2: 新密码2
    :return:
    '''
    message = STR_ERROR
    if new_pw1==new_pw2 and strUtils.isLegals([new_pw1,new_pw2]):
        user = User.query.filter(User.id==u_id,User.pw==old_pw).first()
        print(user)
        if user:
            user.pw=MD5utils.getMD5(new_pw1)
            db.session.commit()
            message = STR_SUCCESS
    else:
        message="两次密码不一样，或含有空格，请重试！"
    return message
def refresh_user_pw(u_id):
    '''
    修改用户密码
    :param u_id: 用户id
    :return:
    '''
    pw = "000000"
    message = STR_ERROR
    if strUtils.isLegal(u_id):
        user = User.query.get(int(u_id))
        print(user)
        if user:
            user.pw=MD5utils.getMD5(pw)
            db.session.commit()
            message = STR_SUCCESS+" 新密码为："+pw
    else:
        message="两次密码不一样，或含有空格，请重试！"
    return message