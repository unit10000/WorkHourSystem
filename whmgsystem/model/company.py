from whmgsystem import db
from whmgsystem.model.department import Department
class Company(db.Model):
    # 表的名字:
    __tablename__ = 't_company'
    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20),unique=True)#unique=True唯一的
    status = db.Column(db.Integer,default=0)
    logo_file = db.Column(db.String(20), default="default.png")  # unique=True唯一的
    jindee_id = db.Column(db.Integer, db.ForeignKey('t_jindee.id'))
    departments = db.relationship("Department", backref=db.backref('company', order_by=id))
    def get_valid_departments(self):
        return Department.query.filter(Department.company_id == self.id,Department.status>-1).all()
    def get_user_number(self):
        departments = Department.query.filter(Department.company_id == self.id,Department.status>-1).all()
        sum = 0
        for d in departments:
            sum = sum + d.get_user_number()
        return sum
    def get_department_number(self):
        departments = self.get_valid_departments()
        return len(departments)
    def get_admins(self):
        from whmgsystem.model.user import User
        return User.query.filter(User.company_id==self.id,User.status==100).all()