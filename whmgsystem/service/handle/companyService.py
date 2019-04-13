from whmgsystem.utils import strUtils,MD5utils
from whmgsystem.model import *
from flask_login import login_user,login_required,current_user,logout_user
from whmgsystem import db
from whmgsystem.syslog import systemlog
from whmgsystem.conf.setting import STR_SUCCESS,STR_ERROR
from whmgsystem.conf import setting
def add_company(name,company_logo_file,jindee_id):
    '''
    添加公司
    :param name: 公司名称
    :param company_logo_file:logo文件
    :param jindee_id: 金蝶配置id
    :return:
    '''
    message=""
    if strUtils.isLegal(name) is False:
        message = "名称不能空，或含有空格"
        return message
    try:
        #将logo文件名+公司名字 取md5形成新的文件名
        logo_name = MD5utils.getMD5(company_logo_file.filename+name)+'.'+company_logo_file.content_type.split('/')[-1]
        company = Company(name=name,logo_file = logo_name,jindee_id=jindee_id)
        if company_logo_file:
            company_logo_file.save(setting.company_log_path+logo_name)
        db.session.add(company)
        db.session.commit()
        message = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        message = STR_ERROR
    return message

def delete_company(company_id):
    '''
    删除公司
    :param company_id: 公司id
    :return:
    '''
    try:
        company = Company.query.get(int(company_id))
        db.session.delete(company)
        db.session.commit()
        message = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        message = STR_ERROR
    return message

def up_company(company_id,name,company_logo_file,jindee_id):
    '''
    更新公司
    :param company_id: 公司id
    :param name: 新名称
    :param company_logo_file: 新公司logo文件
    :param jindee_id: 新金蝶配置id
    :return:
    '''
    message=STR_ERROR
    if strUtils.isLegal(name) is False:
        message = "名称不能空，或含有空格"
        return message
    try:
        company = Company.query.get(int(company_id))
        if company:
            company.name = name
            if jindee_id:
                company.jindee_id = jindee_id
            if company_logo_file:
                logo_name = MD5utils.getMD5(company_logo_file.filename + name) + '.' + \
                            company_logo_file.content_type.split('/')[-1]
                company.logo_file = logo_name
                company_logo_file.save(setting.company_log_path + logo_name)
            db.session.commit()
            message = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        pass
    return message