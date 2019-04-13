from whmgsystem import db

project_user_table = db.Table('t_project_user', db.metadata,
                           db.Column('user_id', db.Integer, db.ForeignKey('t_user.id')),
                           db.Column('project_id', db.Integer, db.ForeignKey('t_project.id'))
                           )