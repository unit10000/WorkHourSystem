"""
Routes and views for the flask application.
"""
import json
from urllib.parse import quote

from flask import Blueprint, render_template, url_for, request, redirect
from flask import make_response
from flask_login import login_required, current_user, logout_user

from whmgsystem import app
from whmgsystem.conf.setting import STR_ERROR, STR_SUCCESS, STR_DATA_ERROR
from whmgsystem.service.handle import userService, workhourService
from whmgsystem.service.view import userViewService
from whmgsystem.service.handle import jindeeService
from whmgsystem.syslog import systemlog
from whmgsystem.utils import excelUtils, MD5utils

#登录
user = Blueprint('user',__name__)
@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    '''
    登陆用户
    :return:
    '''
    if request.method == "POST":
        result = request.form
        user_name = result['user']
        user_pass = result['pass']
        ret = userService.login(user_name,user_pass)
        if current_user.is_authenticated:
            if current_user.status>150:
                return redirect(url_for('super_admin.index'))
            else:
                return redirect(url_for('user.index'))
        else:
            return render_template('alert.html', message=ret['alert'])
    elif not current_user.is_authenticated:
        if userService.is_init():
            return render_template('login.html')
        else:
            return redirect(url_for('init_system'))
    else:
        if current_user.status > 150:
            return redirect(url_for('super_admin.index'))
        else:
            return redirect(url_for('user.index'))
@user.route('/index', methods=['GET'])
@login_required
def index():
    '''
    普通用户首页
    :return:
    '''
    # current_project_id = request.args.get('project_id')
    # data = userViewService.indexData(current_project_id)
    # return render_template('user/index.html',data = data )
    return redirect(url_for('user.selectworktime'))
@user.route('/upworktime', methods=['POST'])
@login_required
def upworktimes():
    '''
    更新工时
    :return:
    '''
    data = {}
    data['status']=False
    result = request.form
    try:
        project_id = result['project_id']
        worktime = float(result['worktime'])
        date = result['date']
    except Exception as e:
        systemlog.log_error(e)
        data['message'] = STR_ERROR
        return json.dumps(data)
    if project_id is None or project_id=='' or date is None or date =='':
        message = STR_DATA_ERROR
    else:
        message = workhourService.updata(project_id,date,worktime)
    if message==STR_SUCCESS:
        data['status'] = True
        data['message'] = date+"  更新成功！"
    else:
        data['message'] = date +"  "+ message
    return json.dumps(data)
@app.route('/alert/<message>', methods=['GET'])
def alert(message):
    '''
    显示提示信息页面
    :param message:
    :return:
    '''
    return render_template('alert.html', message=message,reurl="/index")
@app.route('/register', methods=['POST', 'GET'])
def register():
    '''
    注册用户
    :return:
    '''
    if request.method == "POST":
        result = request.form
        try:
            user_name= result['user']
            user_pass = result['pass']
            department_id = result['department_id']
        except:
            return render_template('alert.html', message=STR_DATA_ERROR)
        message = userService.register(user_name,user_pass,department_id,current_user.company_id,0)
        return render_template('alert.html', message=message)
    return render_template('index.html')
@user.route('/delework', methods=['GET'])
@login_required
def delework():
    '''
    删除工时
    :return:
    '''
    data = {}
    work_id = request.args.get('work_id')
    date = request.args.get('date')
    project_id = request.args.get('project_id')
    if work_id!=None and work_id!="":
        mess = workhourService.deleteByID(work_id)
    elif date!=None and date!="" and project_id!=None and project_id!="" :
        mess = workhourService.delete(project_id,date,current_user.id)
    else:
        mess=STR_DATA_ERROR
    if mess == STR_SUCCESS:
        data['message'] = date+"  删除成功！"
        data['status'] = True
    else :
        data['message'] = date+"  "+mess
        data['status'] = False
    return json.dumps(data)
@user.route('/loginout', methods=['GET'])
@login_required
def user_loginout():
    '''
    用户登出
    :return:
    '''
    logout_user()
    return render_template('alert.html', message='退出成功!' )
@user.route('/selectworktime', methods=['GET'])
@login_required
def selectworktime():
    '''
    查询工时
    :return:
    '''
    current_project_id = request.args.get('project_id')
    starTime = request.args.get('startime')
    endTime = request.args.get('endtime')
    data = userViewService.selectWorkHoursData(current_project_id, starTime, endTime)
    if len(data['date_list'])<2:
        return render_template('alert.html', message='日期间隔错误!')
    return render_template('user/selectworktime.html',data=data)
@app.route('/init_system', methods=['POST','GET'])
def init_system():
    '''
    初始化超级管理员
    :return:
    '''
    if userService.is_init():
        return redirect(url_for('login'))
    if request.method == "POST":
        result = request.form
        try:
            user_name = result['user']
            user_pass = result['pass']
        except:
            return render_template('alert.html', message=STR_DATA_ERROR)
        message = userService.registerSuper(user_name,user_pass,200)
        return render_template('alert.html', message=message)
    else:
        return render_template('init_system.html')
@user.route('/makebom', methods=['GET'])
@login_required
def makebom():
    '''
    制作bom表页面
    :return:
    '''
    current_bom_id = request.args.get('bom_id')
    data = userViewService.makeBomData(current_bom_id)
    return render_template('user/makebom.html',data=data)
@user.route('/download_bom', methods=['post'])
@login_required
def download_bom():
    '''
    下载bom报表
    :return:
    '''
    result = request.form
    try:
        jsonStr = result['json']
        jsonObj = json.loads(jsonStr)
    except:
        return render_template('alert.html', message=STR_DATA_ERROR)
    bom = excelUtils.make_BOM_Ex(jsonObj)
    response = make_response(bom)
    file_name= jsonObj['file_name']+"-"+jsonObj['file_id']+"-"+jsonObj['version']
    file_name = quote(file_name,'utf-8')
    response.headers["Content-Disposition"] = "attachment; filename="+file_name+".xls"
    return response
@user.route('/save_bom', methods=['post'])
@login_required
def save_bom():
    '''
    保存bom表
    :return:
    '''
    result = request.form
    try:
        jsonStr = result['json']
        table_id = result['table_id']
        jsonObj = json.loads(jsonStr)
    except:
        return render_template('alert.html', message=STR_DATA_ERROR)
    message,bom_id = jindeeService.save_ic_table(table_id, jsonObj)
    returl = ''
    if bom_id:
        result = '/user/makebom?bom_id=' + str(bom_id)
    return render_template('alert.html', message=message, reurl=result)
@user.route('/delete_bom', methods=['GET'])
@login_required
def delete_bom():
    '''
    删除bom表
    :return:
    '''
    current_bom_id = request.args.get('bom_id')
    data = jindeeService.delete_bom(current_bom_id)
    return render_template('alert.html', message=data,reurl="makebom")
@user.route('/copy_bom', methods=['post'])
@login_required
def copy_bom():
    '''
    复制bom表
    :return:
    '''
    result = request.form
    try:
        jsonStr = result['json']
        jsonObj = json.loads(jsonStr)
    except:
        return render_template('alert.html', message=STR_DATA_ERROR)
    message,bom_id = jindeeService.copy_ic_table(jsonObj)
    returl=''
    if bom_id:
        result='/user/makebom?bom_id='+str(bom_id)
    return render_template('alert.html', message=message,reurl=result)
@user.route('/up_my_pw', methods=['post'])
@login_required
def up_user_pw():
    '''
    修改用户密码
    :return:
    '''
    result = request.form
    ret_data={}
    isTrue = False
    try:
        old_pw = result['old_pw']
        new_pw1 = result['new_pw1']
        new_pw2 = result['new_pw2']
    except Exception as e:
        systemlog.log_error(e)
        ret_data['message'] = "参数错误！"
        #ret_data['status'] = isTrue
        return render_template('alert.html', message=ret_data['message'])
    message = userService.up_user_pw(current_user.id,MD5utils.getMD5(old_pw),new_pw1,new_pw2)
    return render_template('alert.html', message=message)