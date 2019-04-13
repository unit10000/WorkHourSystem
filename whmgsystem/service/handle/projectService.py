from whmgsystem.utils import strUtils
from whmgsystem.model import *
from flask_login import login_user,login_required,current_user,logout_user
from whmgsystem import db
from whmgsystem.syslog import systemlog
from whmgsystem.conf.setting import STR_SUCCESS,STR_ERROR
def add(project_id,project_name,department_id,u_id):
    '''
    添加项目
    :param project_id: 项目id
    :param project_name: 项目名称
    :param department_id: 部门id
    :param u_id: 负责人id
    :return:
    '''
    data = {}
    if strUtils.isLegals([project_id, department_id, u_id]) == False:
        data['message'] = "项目id不能含有空格或为空！"
        data['reurl'] = ''
    else:
        try:
            project = Project(id=project_id, name=project_name, department_id=department_id, super_user_id=u_id)
            db.session.add(project)
            db.session.commit()
            data['message'] = STR_SUCCESS
            data['reurl'] = "/admin/project?project_id=" + project_id
        except Exception as e:
            systemlog.log_error(e)
            data['reurl'] = ''
            data['message'] = STR_ERROR
    return data
def add_project_user(project_id,users):
    '''
    添加项目用户
    :param project_id: 项目id
    :param users: 用户id列表
    :return:
    '''
    try:
        project = Project.query.get(project_id)
        for u_id in users:
            user = User.query.get(int(u_id))
            project.users.append(user)
        db.session.commit()
        message = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        message = STR_ERROR
    return message
def get_not_in_user(project_id,department_id):
    '''
    获取某部门未加入某项目的用户
    :param project_id: 项目id
    :param department_id: 部门id
    :return:
    '''
    current_project = Project.query.filter(Project.id == project_id).first()
    current_department = Department.query.get(int(department_id))
    retuser = []
    if current_project and current_department:
        users = current_department.get_not_project_user(current_project)
        for u in users:
            user = {}
            user['id'] = u.id
            user['name'] = u.user
            retuser.append(user)
    return retuser
def delete(project_id):
    '''
    删除项目
    :param project_id: 项目id
    :return:
    '''
    try:
        project = Project.query.get(project_id)
        print(project)
        db.session.delete(project)
        db.session.commit()
        message = STR_SUCCESS
    except Exception as e:
        print(1111)
        systemlog.log_error(e)
        message = STR_ERROR
    return message
def delete_user(project_id,user_id):
    '''
    移除项目用户
    :param project_id: 项目id
    :param user_id: 用户id
    :return:
    '''
    if user_id == None or user_id == "" or project_id == None or project_id == "":
        message ='项目id和用户ID不能为空'
    else:
        try:
            project = Project.query.get(project_id)
            user =  User.query.get(user_id)
            project.users.remove(user)
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message
def up_project_status(project_id,type):
    '''
    更新项目状态
    :param project_id: 项目id
    :param type: 项目状态
    :return:
    '''
    if project_id == None or project_id == "" or type==None or type == "":
        message='参数有误'
    else:
        try:
            project = Project.query.get(project_id)
            project.status = int(type)
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message
def up_project_name(project_id,new_name):
    '''
    更新项目名称
    :param project_id: 项目id
    :param new_name: 新项目名称
    :return:
    '''
    if project_id == None or project_id == "" or new_name==None or new_name == "":
        message ="参数有误！"
    else:
        try:
            project = Project.query.get(project_id)
            project.name = new_name
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message