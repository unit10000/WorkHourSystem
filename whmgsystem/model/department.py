from whmgsystem import db
from whmgsystem.model.project import Project
from whmgsystem.utils import timeUtils
class Department(db.Model):
    # 表的名字:
    __tablename__ = 't_department'
    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    status = db.Column(db.Integer,default=0)
    regtime = db.Column(db.String(20),default=timeUtils.getTime('%Y-%m-%d'))
    company_id = db.Column(db.Integer,db.ForeignKey('t_company.id'))
    users = db.relationship("User", backref=db.backref('department', order_by=id))
    projects = db.relationship("Project", backref=db.backref('department', order_by=id))
    def get_valid_projects(self):
        return Project.query.filter(Project.department_id == self.id,Project.status>-1).all()
    def get_not_project_user(self,project):
        users = project.users
        lists = []
        for user in self.users:
            if user not in users and user.status>-1:
                lists.append(user)
        return lists
    def get_finish_projects(self):
        return Project.query.filter(Project.department_id == self.id, Project.status == -1).all()
    def get_user_number(self):
        return len(self.users)