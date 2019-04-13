# 导入:
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from whmgsystem.conf.setting import DB_BASE_MODEL
from sqlalchemy import text
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func
from whmgsystem.conf import setting,initsystem
from whmgsystem.model import *
from whmgsystem.utils import DBFactory
#初始化测试环境
initsystem.init_system()
# 创建对象的基类:
# 定义User对象:
if __name__ == '__main__':
    session = DBFactory.getSession()
    # user = session.query(User).filter(User.id == 1).filter(WorkHour.date=='2018-08-02').one()
    # print (user.user)
    # for w in user.workHours:
    #     print(w.date)
    # for work in workHour:
    #     print (work.date)

    workHour = session.query(WorkHour).filter(WorkHour.user_id == 1).filter(WorkHour.project_id == ' TPO181101').filter(WorkHour.date<'2018-08-08').all()
    for work in workHour:
        print (work.date)
        print (work.worktime)
    # project=session.query(Project).filter(Project.id == ' TPO181605').one()
    # print (len(project.users))
    # for row in session.query(Company).filter(Company.id==1).all():
    #     print ('\n'+row.name+">>>>>>>>>>>>>>>>>>>>>>>>:\n")
    #     for department in row.departments:
    #         print ('\n' + department.name + ">>>>>>>:\n")
    #         for project in department.prjects:
    #             print (project.name)
    #             for user in project.users:
    #                 print(user.user)
    #

    # project =  session.query(Project).filter(Project.id == ' TPO181605').one()
    # print (project.name)
    # for u in project.users:
    #     print (u.user)
    # session.commit()
    # session.close()