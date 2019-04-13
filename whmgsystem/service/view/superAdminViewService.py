from whmgsystem.utils import strUtils,MD5utils
from whmgsystem.model import *
from flask_login import login_user,login_required,current_user,logout_user
from whmgsystem import db
from whmgsystem.syslog import systemlog
from whmgsystem.conf.setting import STR_SUCCESS,STR_ERROR
import platform
import psutil
def system_Inf():
    '''
     mem.total #获取内存总数
     mem.used #获取已使用内存
     mem.free #获取空闲内存
    :return:
    '''
    data = {}
    data['cpu_count_logical'] = psutil.cpu_count(logical=True)  # 查看CPU逻辑个数
    data['cpu_count'] = psutil.cpu_count(logical=False)  # 显示CPU物理个数
    data['virtual_memory'] = psutil.virtual_memory()
    data['system_inf'] = platform.uname()
    data['python_version']=platform.python_version()
    data['menu'] = 'system_menu'
    return data
def index():
    '''
    超级管理员首页数据
    :return:
    '''
    data = {}
    companys = Company.query.filter().all()
    jindees = Jindee.query.filter().all()
    data['companys'] = companys
    data['jindees'] = jindees
    data['menu'] = 'company_menu'
    return data
def admin_manage(company_id):
    '''
    项目管理员管理页面数据
    :param company_id:
    :return:
    '''
    data={}
    data['admins']=[]
    companys = Company.query.filter().all()
    try:
        company = Company.query.get(int(company_id))
    except:
        company=None
    if not company:
        if companys:
            company = companys[0]
    company_all=[]
    if company:
        data['admins'] = company.get_admins()
        company_all.append(company)
        for c in companys:
            if c != company:
                company_all.append(c)
    data['companys'] = company_all
    data['company'] = company
    data['menu'] = 'admin_menu'
    return data
def jindee():
    '''
    金蝶配置管理页面数据
    :return:
    '''
    data={}
    jindees = Jindee.query.filter().all()
    data['menu'] = "jindee_menu"
    data['jindees'] = jindees
    return data

