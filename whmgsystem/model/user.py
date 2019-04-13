from whmgsystem import db
from whmgsystem import login_manager
from whmgsystem.model.middleTable import project_user_table
from flask_login import UserMixin
from whmgsystem.model.workhour import WorkHour
from whmgsystem.model.company import Company
from whmgsystem.utils import timeUtils
class User(UserMixin,db.Model):
    # 表的名字:
    __tablename__ = 't_user'
    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(20))
    pw = db.Column(db.String(20))
    status = db.Column(db.Integer,default=0)
    regtime = db.Column(db.String(20),default=timeUtils.getTime('%Y-%m-%d %H:%M:%S'))
    department_id = db.Column(db.Integer,db.ForeignKey('t_department.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('t_company.id'))
    projects = db.relationship('Project', secondary=project_user_table)
    super_projects = db.relationship("Project", backref=db.backref('super_user', order_by=id))
    work_hours = db.relationship('WorkHour', backref=db.backref('user', order_by=id),lazy='dynamic')
    boms = db.relationship("ItemTableView", backref=db.backref('user', order_by=id))
# 登录认证的回调，写在user model中
    def get_work_hours(self,project_id):
        return WorkHour.query.filter(WorkHour.user_id == self.id , WorkHour.project_id == project_id,WorkHour.status==1).all()
    def get_work_hours(self,project_id,start_time,end_time):
        return WorkHour.query.filter(WorkHour.user_id == self.id, WorkHour.project_id == project_id,WorkHour.date>=start_time,WorkHour.date<=end_time,WorkHour.status==1).all()
    def get_company(self):
        return Company.query.get(int(self.company_id))
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))