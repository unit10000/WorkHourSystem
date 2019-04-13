from whmgsystem import db
class ItemTableView(db.Model):
    # 表的名字:
    __tablename__ = 'v_item_table'
    # 表的结构:
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.String(20))
    file_name = db.Column(db.String(20))
    file_id = db.Column(db.String(20))
    item_num = db.Column(db.String(20), default='')
    version = db.Column(db.String(20))
    user_id = db.Column(db.Integer,db.ForeignKey('t_user.id'))
    auditing=db.Column(db.String(20), default='')
    proofreading=db.Column(db.String(20), default='')
    approval=db.Column(db.String(20), default='')
    signer  =db.Column(db.String(20), default='')
    date = db.Column(db.String(20), default='')
    user_name = db.Column(db.String(20))
    project_name = db.Column(db.String(20))
    items = db.relationship("ItemDetail", backref=db.backref('itemTableView', order_by=id))