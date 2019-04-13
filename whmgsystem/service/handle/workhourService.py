from whmgsystem.utils import timeUtils
from whmgsystem.model import *
from flask_login import login_user,login_required,current_user,logout_user
from whmgsystem import db
from whmgsystem.syslog import systemlog
from whmgsystem.conf.setting import STR_SUCCESS,STR_ERROR
def updata(project_id,date,worktime):
    '''
    更新工时
    :param project_id: 项目id
    :param date: 日期
    :param worktime: 工时
    :return:
    '''
    now_time = timeUtils.getTime("%Y-%m-%d")
    work_hours = WorkHour.query.filter(WorkHour.project_id == project_id, WorkHour.user_id == current_user.id,
                                       WorkHour.date == date).first()
    if work_hours:
        work_hours.worktime = worktime
        work_hours.time = now_time
        work_hours.status = 1
    else:
        work_hours = WorkHour(user_id=current_user.id, project_id=project_id, worktime=worktime, time=now_time,
                              date=date)
        db.session.add(work_hours)
    try:
        db.session.commit()
        ret = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        systemlog.log_error("提交工时出错")
        ret = "提交失败，请检查提交内容并重试"
    return ret
def deleteByID(work_id):
    '''
    根据id删除工时
    :param work_id: 工时id
    :return:
    '''
    work_hours = WorkHour.query.filter(WorkHour.id == work_id).first()
    try:
        db.session.delete(work_hours)
        db.session.commit()
        mess = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        mess = STR_ERROR
    return mess
def delete(project_id,date,u_id):
    '''
    删除工时
    :param project_id: 项目id
    :param date: 日期
    :param u_id: 用户id
    :return:
    '''
    work_hours = WorkHour.query.filter(WorkHour.project_id == project_id,WorkHour.date ==date , WorkHour.user_id ==u_id).first()
    try:
        if not work_hours:
            raise Exception('没有找到该工时：uid：'+u_id+" pid:"+project_id+" date:"+date)
        work_hours.status = -1
        db.session.commit()
        mess = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        mess = STR_ERROR
    return mess