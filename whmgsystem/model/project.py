from whmgsystem import db
from whmgsystem.model.middleTable import project_user_table
from whmgsystem.model.workhour import WorkHour
from whmgsystem.utils import timeUtils
class Project(db.Model):
    __tablename__ = 't_project'
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    status = db.Column(db.Integer,default=0)
    regtime = db.Column(db.String(20),default=timeUtils.getTime('%Y-%m-%d'))
    department_id = db.Column(db.Integer, db.ForeignKey('t_department.id'))
    super_user_id = db.Column(db.Integer, db.ForeignKey('t_user.id'))
    users= db.relationship('User', secondary=project_user_table)
    #work_hours = db.relationship('WorkHour', backref=db.backref('project', order_by=id))
    def get_work_hours(self,start_time,end_time):
        return WorkHour.query.filter(WorkHour.project_id == self.id,WorkHour.date>=start_time,WorkHour.date<=end_time,WorkHour.status==1).all()
    def get_valid_users(self):
        return [u for u in self.users if u.status >-1]