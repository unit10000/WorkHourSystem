from whmgsystem.service.handle import jindeeService
from flask import Blueprint, render_template, request

from whmgsystem.conf.setting import STR_DATA_ERROR
from whmgsystem.decorators.authorize_required import super_admin_required
from whmgsystem.service.handle import companyService
from whmgsystem.service.handle import userService, jindeeService
from whmgsystem.service.view import superAdminViewService
from flask import Blueprint, render_template, request

from whmgsystem.conf.setting import STR_DATA_ERROR
from whmgsystem.decorators.authorize_required import super_admin_required
from whmgsystem.service.handle import companyService
from whmgsystem.service.handle import userService, jindeeService
from whmgsystem.service.handle import jindeeService
from whmgsystem.service.view import superAdminViewService

super_admin = Blueprint('super_admin',__name__)
@super_admin.route('/', methods=['GET'])
@super_admin.route('/index', methods=['GET'])
@super_admin_required
def index():
    '''
    超级管理员主页
    :return:
    '''
    data = superAdminViewService.index()
    return render_template('superAdmin/index.html',data = data)
@super_admin.route('/admin_manage', methods=['GET'])
@super_admin_required
def admin_manage():
    '''
    项目管理员管理页面
    :return:
    '''
    company_id = request.args.get('company_id')
    data = superAdminViewService.admin_manage(company_id)
    return render_template('superAdmin/admin_manage.html',data=data)
@super_admin.route('/system', methods=['GET'])
@super_admin_required
def system():
    '''
    系统环境页面
    :return:
    '''
    data = superAdminViewService.system_Inf()
    return render_template('superAdmin/system.html',data = data)
@super_admin.route('/jindee', methods=['GET'])
@super_admin_required
def jindee():
    '''
    金蝶配置页面
    :return:
    '''
    data = superAdminViewService.jindee()
    return render_template('superAdmin/jindee.html',data = data)
@super_admin.route('/addcompany', methods=['POST'])
@super_admin_required
def add_company():
    '''
    添加公司
    :return:
    '''
    result = request.form
    try:
        company_name = result['company_name']
        company_logo_file = file=request.files['company_logo_file']
        jindee_id = result['jindee_id']
    except:
        return render_template('alert.html', message=STR_DATA_ERROR)
    message = companyService.add_company(company_name,company_logo_file,jindee_id)
    return render_template('/alert.html',message=message)
@super_admin.route('/delete_company', methods=['get'])
@super_admin_required
def delete_company():
    '''
    删除公司
    :return:
    '''
    company_id = request.args.get('company_id')
    message = companyService.delete_company(company_id)
    return render_template('alert.html', message=message)
@super_admin.route('/up_company', methods=['POST'])
@super_admin_required
def up_company():
    '''
    更新公司
    :return:
    '''
    result = request.form
    try:
        company_id = result['company_id']
        new_name = result['company_name']
    except:
        return render_template('alert.html', message=STR_DATA_ERROR)
    try:
        company_logo_file = file = request.files['company_logo_file']
    except:
        company_logo_file = None
    try:
        jindee_id = int(result['jindee_id'])
    except:
        jindee_id = None
    message = companyService.up_company(company_id,new_name,company_logo_file,jindee_id)
    return render_template('alert.html', message=message)

@super_admin.route('/register_admin', methods=['POST'])
@super_admin_required
def register_admin():
    '''
    添加项目管理员
    :return:
    '''
    result = request.form
    try:
        user_name= result['user']
        user_pass = result['pass']
        company_id = result['company_id']
    except:
        return render_template('alert.html', message=STR_DATA_ERROR)
    message = userService.register(user_name,user_pass,-1,company_id,100)
    return render_template('alert.html', message=message)
@super_admin.route('/up_user_status', methods=['get'])
@super_admin_required
def up_user_status():
    '''
    更新用户状态-1禁用0正常100项目管理员
    :return:
    '''
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    message = userService.up_user_status(user_id,status)
    return render_template('alert.html', message=message)

@super_admin.route('/add_jindee_config', methods=['POST'])
@super_admin_required
def add_jindee_config():
    '''
    添加金蝶配置
    :return:
    '''
    result = request.form
    try:
        config_name= result['name']
        userName = result['userName']
        userPw = result['userPw']
        DBAddress = result['DBAddress']
        DBName = result['DBName']
    except:
        return render_template('alert.html', message=STR_DATA_ERROR)
    message = jindeeService.add_jindee_config(config_name, userName, userPw, DBAddress, DBName)
    return render_template('alert.html', message=message)
@super_admin.route('/delejindee', methods=['get'])
@super_admin_required
def delejindee():
    '''
    删除金蝶配置
    :return:
    '''
    jindee_id = request.args.get('jindee_id')
    message = jindeeService.delete_jindee(jindee_id)
    return render_template('alert.html', message=message)