from whmgsystem.utils import strUtils
from whmgsystem.model import *
from flask_login import login_user,login_required,current_user,logout_user
from whmgsystem import db
from whmgsystem.syslog import systemlog
from whmgsystem.conf.setting import STR_SUCCESS,STR_ERROR


def get_department_by_company(company_id):
    '''
    根据公司获取部门
    :param company_id:公司id
    :return:
    '''
    data = {}
    retdepartment = []
    try:
        current_departments = Company.query.filter(Company.id == company_id).first().get_valid_departments()
    except Exception as e:
        systemlog.log_error(e)
        return retdepartment
    if not current_departments:
        return retdepartment
    for u in current_departments:
        department = {}
        department['id'] = u.id
        department['name'] = u.name
        retdepartment.append(department)
    return retdepartment
def add(name,company_id):
    '''
    添加部门
    :param name: 部门名称
    :param company_id: 公司id
    :return:
    '''
    if strUtils.isLegals([name]) == False:
        message = '部门名称不能为空'
    else:
        try:

            department =  Department(name=name,company_id =company_id)
            db.session.add(department)
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message
def delete(department_id):
    '''
    删除部门
    :param department_id: 部门id
    :return:
    '''
    if strUtils.isLegals([department_id]) == False:
        message = '部门id不能为空'
    else:
        try:
            department = Department.query.get(int(department_id))
            db.session.delete(department)
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message
def up_department_name(department_id,new_name):
    '''
    更新部门名称
    :param department_id: 部门id
    :param new_name: 新名称
    :return:
    '''
    if strUtils.isLegals([department_id,new_name]) == False:
        message = '不能为空或含有空格'
    else:
        try:
            department = Department.query.get(int(department_id))
            department.name=new_name
            db.session.commit()
            message = STR_SUCCESS
        except Exception as e:
            systemlog.log_error(e)
            message = STR_ERROR
    return message