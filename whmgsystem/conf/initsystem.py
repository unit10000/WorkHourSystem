import os, platform
from whmgsystem.conf import setting
from whmgsystem.utils import DBUtils
from whmgsystem.model import *
from whmgsystem.dao import projectDao
def init_system():
    #初始化系统
    init_work_path()
    init_db()
def init_work_path():
    '''
    用于初始化工作路径
    :return:
    '''
    directory = os.path.abspath('.')  # 获得当前工作目录
    syst = platform.system()
    if 'Windows' in syst:
        directory += '\\'
        company_log_path = directory+'whmgsystem\\static\\images\\logo\\'
    else:
        directory += '/'
        company_log_path = directory + 'whmgsystem/static/images/logo//'
    print('work path:' + directory)
    setting.WORK_PATH = directory
    setting.company_log_path = company_log_path
def init_db():
    '''
    用于初始化数据库
    :return:
    '''
    DBUtils.init_db()
    #setting.dbpool_util = DbPoolUtil(config_file=setting.WORK_PATH + setting.JDBC_NAME)
