from urllib.parse import quote

from flask import Blueprint, render_template, request, make_response
from flask_login import current_user

from whmgsystem.decorators.authorize_required import admin_required
from whmgsystem.service.view import adminViewService
from whmgsystem.service.handle import projectService, departmentService, userService
from whmgsystem.syslog import systemlog
from whmgsystem.utils import strUtils, timeUtils, excelUtils

admin = Blueprint('admin',__name__)


@admin.route('/', methods=['GET'])
@admin.route('/index', methods=['GET'])
@admin_required
def index():
    '''
    项目管理员首页
    :return:
    '''
    current_project_id = request.args.get('project_id')
    starTime = request.args.get('startime')
    endTime = request.args.get('endtime')
    data = adminViewService.adminData(current_project_id, starTime, endTime)
    return render_template('admin/index.html', data=data)
@admin.route('/project', methods=['GET'])
@admin_required
def project():
    '''
    项目管理页面
    :return:
    '''
    current_project_id = request.args.get('project_id')
    data = adminViewService.projectData(current_project_id)
    return render_template('admin/project.html',data = data)
@admin.route('/dowExcel', methods=['GET'])
@admin_required
def makeExcel():
    '''
    下载工时报表
    :return:
    '''

    try:
        starTime = request.args.get('startime')
        endTime=request.args.get('endtime')
    except:
        pass
    if starTime == None or endTime == "":
        return render_template('alert.html', message="请输入日期范围！")
    dateList = timeUtils.getDateList(starTime,endTime,weekday = False)
    company = current_user.get_company()
    xlsx = excelUtils.make_work_hour_Ex(dateList, company, starTime,endTime)
    response = make_response(xlsx)
    file_name = quote("工时报表", 'utf-8')
    response.headers["Content-Disposition"] = "attachment; filename="+starTime+"&"+endTime+"-"+file_name+"("+timeUtils.getTime('%Y-%m-%d')+").xls"
    return response
@admin.route('/addproject', methods=['POST'])
@admin_required
def addproject():
    '''
    添加项目api
    :return:
    '''
    result = request.form
    try:
        project_id = result['project_id']
        project_name = result['project_name']
        department_id = result['department_id']
        u_id = result['user_id']
    except Exception as e:
        systemlog.log_error(e)
        return render_template('alert.html', message="提交参数错误")
    data = projectService.add(project_id, project_name, department_id, u_id)
    return render_template('alert.html', message=data['message'],reurl=data['reurl'])
@admin.route('/addprojectuser', methods=['GET'])
@admin_required
def addprojectuser():
    '''
    添加项目人员api
    :return:
    '''
    project_id = request.args.get('project_id')
    users = request.args.get('users')
    if not strUtils.isLegals([users]):
        return render_template('alert.html', message="提交参数错误")
    users = users.split(',')
    message = projectService.add_project_user(project_id, users)
    return render_template('alert.html', message=message)

@admin.route('/addepartment', methods=['POST'])
@admin_required
def addepartment():
    '''
    添加部门api
    :return:
    '''
    result = request.form
    try:
        name = result['department_name']
    except Exception as e:
        return render_template('alert.html', '名称不能为空')
    message = departmentService.add(name, current_user.company_id)
    return render_template('alert.html', message=message)
@admin.route('/deledepartment', methods=['GET'])
@admin_required
def deledepartment():
    '''
    删除部门api
    :return:
    '''
    department_id = request.args.get('department_id')
    message = departmentService.delete(department_id)
    return render_template('alert.html', message=message)
@admin.route('/deleproject', methods=['GET'])
@admin_required
def deleproject():
    '''
    删除项目api
    :return:
    '''
    project_id = request.args.get('project_id')
    message = projectService.delete(project_id)
    return render_template('alert.html', message=message)
@admin.route('/manage', methods=['GET'])
@admin_required
def manguser():
    '''
    管理用户页面
    :return:
    '''
    department_id = request.args.get('department_id')
    type = request.args.get('type')
    if type=='user':
        include_htm = 'user'
    else:
        include_htm = 'index'
    data = adminViewService.manageData(department_id)
    return render_template('admin/manage.html', data=data,include_htm=include_htm)
@admin.route('/deleuser', methods=['GET'])
@admin_required
def deleuser():
    '''
    删除用户api
    :return:
    '''
    user_id = request.args.get('user_id')
    message = userService.delete(user_id)
    return render_template('alert.html', message=message)
@admin.route('/deleProUser', methods=['GET'])
@admin_required
def deleProUser():
    '''
    移除项目成员api
    :return:
    '''
    user_id = request.args.get('user_id')
    project_id = request.args.get('project_id')
    message = projectService.delete_user(project_id, user_id)
    return render_template('alert.html', message=message)
@admin.route('/upProjectType', methods=['GET'])
@admin_required
def upProjectType():
    '''
    修改项目状态
    :return:
    '''
    project_id = request.args.get('project_id')
    type = request.args.get('type')
    message = projectService.up_project_status(project_id, type)
    return render_template('alert.html', message=message)
@admin.route('/up_project', methods=['POST'])
@admin_required
def up_project():
    '''
    更新项目信息
    :return:
    '''
    result = request.form
    try:
        project_id = result['project_id']
        new_name = result['project_name']
    except Exception as e:
        return render_template('alert.html', '获取参数异常')
    message =  projectService.up_project_name(project_id, new_name)
    return render_template('alert.html', message=message)
@admin.route('/up_department', methods=['POST'])
@admin_required
def up_department():
    '''
    更新部门信息
    :return:
    '''
    result = request.form
    try:
        project_id = result['department_id']
        new_name = result['new_name']
    except Exception as e:
        return render_template('alert.html', '获取参数异常')
    message = departmentService.up_department_name(project_id, new_name)
    return render_template('alert.html', message=message)


@admin.route('/up_user_department', methods=['POST'])
@admin_required
def up_user_department():
    '''
    修改用户部门api
    :return:
    '''
    result = request.form
    try:
        department_id = result['department_id']
        user_id = result['user_id']
    except Exception as e:
        return render_template('alert.html', '获取参数异常')
    message = userService.up_user_department(department_id,user_id)
    return render_template('alert.html', message=message)

@admin.route('/up_user_status', methods=['GET'])
@admin_required
def up_user_status():
    '''
    修改用户状态
    :return:
    '''
    user_id = request.args.get('user_id')
    status = request.args.get('status')
    message = userService.up_user_status(user_id,status)
    return render_template('alert.html', message=message)


@admin.route('/refreshPW', methods=['GET'])
@admin_required
def refreshPW():
    '''
    重置用户密码
    :return:
    '''
    user_id = request.args.get('user_id')
    message = userService.refresh_user_pw(user_id)
    return render_template('alert.html', message=message)
