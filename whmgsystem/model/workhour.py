from whmgsystem import db
class WorkHour(db.Model):
    # 表的名字:
    __tablename__ = 't_work_record'
    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.id'))
    project_id = db.Column(db.Integer,db.ForeignKey('t_project.id'))
    worktime = db.Column(db.Float)
    date = db.Column(db.String(20))#工时日期
    time = db.Column(db.String(20))#提交日期
    status = db.Column(db.Integer,default=1)