from whmgsystem import db
class ItemDetail(db.Model):
    # 表的名字:
    __tablename__ = 't_item_detail'
    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    item_number = db.Column(db.String(20))
    name = db.Column(db.String(20),default='')
    model = db.Column(db.String(20))
    note = db.Column(db.String(20),default='')
    install_number = db.Column(db.String(20), default='')
    unit = db.Column(db.String(20), default='PCS')
    number=db.Column(db.Integer)
    remark = db.Column(db.String(20), default='')
    ic_item_header_id = db.Column(db.Integer,db.ForeignKey('v_item_table.id'))