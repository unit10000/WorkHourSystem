from whmgsystem import db
from whmgsystem.model.middleTable import project_user_table
from whmgsystem.model.workhour import WorkHour
from whmgsystem.utils import timeUtils
class Jindee(db.Model):
    __tablename__ = 't_jindee'
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    userName = db.Column(db.String(20))
    userPw = db.Column(db.String(20))
    DBAddress = db.Column(db.String(20))
    DBName = db.Column(db.String(20))
    companys = db.relationship('Company', backref=db.backref('jindee', order_by=id))