from whmgsystem.utils import timeUtils
from whmgsystem.model import *
from flask_login import login_user,login_required,current_user,logout_user
from whmgsystem.syslog import systemlog
def adminData(current_project_id,starTime,endTime):
    '''
    管理员首页返回项目时间范围工时
    :param current_project_id:项目id
    :param starTime:起始时间
    :param endTime:结束时间
    :return:
    '''
    data = {}
    my_department = current_user.department
    my_company = current_user.get_company()
    departments = my_company.get_valid_departments()
    current_project = Project.query.filter(Project.id == current_project_id).first()
    if not current_project:
        for d in departments:
            for p in d.get_valid_projects():
                current_project = p
                break
    if starTime == None or starTime == "" or endTime == None or endTime == "":
        starTime = timeUtils.getTime("%Y-%m-") + "01"
        endTime = timeUtils.getTime("%Y-%m-") + timeUtils.getMonthLastDay(timeUtils.getTime("%Y"),
                                                                          timeUtils.getTime("%m"))
    data['dateList'] =timeUtils.getDateList(starTime,endTime)
    data['start_time'] = starTime
    data['end_time'] = endTime
    data['company'] = my_company
    data['departments'] = departments
    data['current_project'] = current_project
    return data
def projectData(current_project_id):
    '''
    项目管理页面数据，返回项目信息
    :param current_project_id:项目id
    :return:
    '''
    data = {}
    my_department = current_user.department
    my_company = current_user.get_company()
    departments = my_company.get_valid_departments()
    current_project = Project.query.filter(Project.id == current_project_id).first()
    if not current_project:
        for d in departments:
            for p in d.get_valid_projects():
                current_project = p
                break
    companys = Company.query.filter(Company.status > -1).all()
    company_all = []
    if companys:
        company_all.append(my_company)
        for c in companys:
            if c != my_company:
                company_all.append(c)
    data['companys'] = company_all
    data['company'] = my_company
    data['departments'] = departments
    data['current_project'] = current_project
    return data
def manageData(department_id):
    '''
    系统管理页面数据，返回部门信息
    :param department_id: 部门id
    :return:
    '''
    data = {}
    company = current_user.get_company()
    current_department = None
    try:
        current_department = Department.query.get(department_id)
    except Exception as e:
        systemlog.log_error(e)
        pass
    if not current_department:
        for d in company.get_valid_departments():
            current_department = d
            break
    data['company'] = company
    data['current_department'] = current_department
    return data