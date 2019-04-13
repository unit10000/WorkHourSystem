import json

from flask import Blueprint, request

from whmgsystem.decorators.authorize_required import api_required
from whmgsystem.service.handle import departmentService, userService, jindeeService
from whmgsystem.service.handle import projectService
from whmgsystem.syslog import systemlog
from whmgsystem.utils import timeUtils

api = Blueprint('api',__name__)

@api.route('/get_user', methods=['POST'])
@api_required
def get_user():
    '''
    获取用户列表
    :return:
    '''
    isTrue = False
    data = {}
    result = request.form
    try:
        department_id = result['department_id']
        reqtype = result['type']
    except Exception as e:
        systemlog.log_error(e)
        data['message'] = "部门id错误，或查询类型错误"
        data['status'] = isTrue
        return json.dumps(data)
    if reqtype =='1':
        retuser = userService.get_user_by_department(department_id)
        data['user'] = retuser
    elif reqtype=='2':
        try:
            p_id = result['project_id']
        except Exception as e:
            systemlog.log_error(e)
            data['message'] = "项目id错误"
            data['status'] = isTrue
            return json.dumps(data)
        retuser = projectService.get_not_in_user(p_id, department_id)
        data['user'] = retuser
    else:
        data['message'] = "查询类型错误"
        data['status'] = isTrue
        return json.dumps(data)
    isTrue = True
    data['status'] = isTrue
    return json.dumps(data)
@api.route('/get_department', methods=['POST'])
@api_required
def get_department():
    '''
    获取部门列表
    :return:
    '''
    data={}
    isTrue = False
    result = request.form
    try:
        company_id = result['company_id']
    except Exception as e:
        systemlog.log_error(e)
        data['message'] = "公司id错误"
        data['status'] = isTrue
        return json.dumps(data)
    data['departments'] = departmentService.get_department_by_company(company_id)
    data['status'] = True
    return json.dumps(data)

@api.route('/select_icitem', methods=['POST'])
@api_required
def select_icitem():
    '''
    根据类型搜索物料
    :return:
    '''
    ret_data={}
    isTrue = False
    result = request.form
    try:
        #company_id = result['company_id']
        type = result['type']
        data = result['data']
    except Exception as e:
        systemlog.log_error(e)
        ret_data['message'] = "参数错误！"
        ret_data['status'] = isTrue
        return json.dumps(ret_data)
    ret_data['items'] = jindeeService.like_ICItem(data, type)
    ret_data['status'] = True
    return json.dumps(ret_data)
@api.route('/select_icitems', methods=['POST'])
@api_required
def select_icitems():
    '''
    根据物料id批量搜索物料
    :return:
    '''
    ret_data={}
    isTrue = False
    result = request.form
    try:
        #company_id = result['company_id']
        #type = result['type']
        data = result['select_data']
        install_num =result['install_num']
        item_num=result['item_num']
        select_type=result['select_type']
    except Exception as e:
        systemlog.log_error(e)
        ret_data['message'] = "参数错误！"
        ret_data['status'] = isTrue
        return json.dumps(ret_data)
    ret_data = jindeeService.select_ICItems(data, install_num, item_num, select_type)
    return json.dumps(ret_data)
@api.route('/get_jiari', methods=['POST'])
@api_required
def get_jiari():
    '''
    获取节假日api（根据三方api 以弃用）
    :return:
    '''
    result = request.form
    ret_data={}
    isTrue = False
    try:
        #company_id = result['company_id']
        #type = result['type']
        days = result['days']
    except Exception as e:
        systemlog.log_error(e)
        ret_data['message'] = "参数错误！"
        ret_data['status'] = isTrue
        return json.dumps(ret_data)
    ret_data = timeUtils.getWeekend(days)
    return ret_data