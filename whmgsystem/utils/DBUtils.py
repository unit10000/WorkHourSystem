from whmgsystem import db
from whmgsystem.model.user import User
from sqlite3 import OperationalError
from flask_sqlalchemy import sqlalchemy
from whmgsystem.syslog import systemlog
def init_db():
    '''
    初始化数据库
    :return:
    '''
    try:
        User.query.filter().first()
    except sqlalchemy.exc.OperationalError:
        systemlog.log_info("未发现数据库...\n")
        systemlog.log_info("准备初始化数据库...\n")
        db.session.execute("PRAGMA foreign_keys = OFF;")
        for sql in sql_List:
            try:
                db.session.execute(sql)
                db.session.commit()
            except Exception as e:
                systemlog.log_error(e)
        systemlog.log_info("数据库初始化完成...")
sql_List = [
    '''CREATE TABLE "t_company" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"name"  TEXT NOT NULL,
"status"  INTEGER NOT NULL DEFAULT 0,
"logo_file"  TEXT,
"jindee_id"  INTEGER,
FOREIGN KEY ("jindee_id") REFERENCES "t_jindee" ("id"),
UNIQUE ("name" ASC)
);''',
    '''CREATE TABLE "t_department" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "name" TEXT NOT NULL,
  "status" INTEGER NOT NULL DEFAULT 0,
  "regtime" TEXT,
  "company_id" INTEGER NOT NULL,
  CONSTRAINT "fkey0" FOREIGN KEY ("company_id") REFERENCES "t_company" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("name" ASC, "company_id" ASC)
);'''
,
    '''CREATE TABLE "t_project" (
  "id" TEXT NOT NULL,
  "name" TEXT NOT NULL,
  "status" INTEGER NOT NULL DEFAULT 0,
  "regtime" TEXT NOT NULL,
  "department_id" INTEGER NOT NULL,
  "super_user_id" INtEGER NOT NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "fkey0" FOREIGN KEY ("department_id") REFERENCES "t_department" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("super_user_id") REFERENCES "t_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("name" ASC, "department_id" ASC),
  UNIQUE ("id" ASC)
);'''
,
    '''CREATE TABLE "t_project_user" (
  "user_id" INTEGER NOT NULL,
  "project_id" TEXT NOT NULL,
  "status" INTEGER DEFAULT 0,
  "addtime" TEXT,
  CONSTRAINT "fkey0" FOREIGN KEY ("user_id") REFERENCES "t_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT "fkey1" FOREIGN KEY ("project_id") REFERENCES "t_project" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("user_id" ASC, "project_id" ASC)
);'''
,
    '''CREATE TABLE "t_user" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "user" TEXT NOT NULL,
  "pw" TEXT NOT NULL,
  "status" INTEGER NOT NULL DEFAULT 0,
  "regtime" TEXT NOT NULL,
  "department_id" INTEGER NOT NULL,
  "company_id" INTEGER DEFAULT 1,
  CONSTRAINT "fkey0" FOREIGN KEY ("department_id") REFERENCES "t_department" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("company_id") REFERENCES "t_company" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  UNIQUE ("user" ASC)
);'''
    ,
    '''CREATE TABLE "t_work_record" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"user_id"  INTEGER NOT NULL,
"project_id"  TEXT NOT NULL,
"worktime"  REAL NOT NULL,
"date"  TEXT NOT NULL,
"time"  TEXT,
"status"  INTEGER NOT NULL DEFAULT 1,
CONSTRAINT "fkey0" FOREIGN KEY ("user_id") REFERENCES "t_user" ("id"),
CONSTRAINT "fkey1" FOREIGN KEY ("project_id") REFERENCES "t_project" ("id"),
UNIQUE ("user_id" ASC, "project_id" ASC, "date" ASC)
);''',
    '''
    CREATE TABLE "t_ic_item_header" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"project_id"  TEXT NOT NULL,
"file_name"  TEXT NOT NULL,
"file_id"  TEXT NOT NULL,
"item_num"  TEXT,
"version"  TEXT NOT NULL,
"user_id"  INTEGER NOT NULL,
"auditing"  TEXT,
"proofreading"  TEXT,
"approval"  TEXT,
"signer"  TEXT,
"date"  TEXT NOT NULL,
CONSTRAINT "fkey0" FOREIGN KEY ("project_id") REFERENCES "t_project" ("id"),
FOREIGN KEY ("user_id") REFERENCES "t_user" ("id")
);
    ''',
    '''
    CREATE TABLE "t_item_detail" (
"id"  INTEGER NOT NULL,
"index"  INTEGER NOT NULL,
"item_number"  TEXT NOT NULL,
"name"  TEXT,
"model"  TEXT NOT NULL,
"note"  TEXT,
"install_number"  TEXT,
"unit"  TEXT NOT NULL,
"number"  INTEGER NOT NULL,
"remark"  TEXT,
"ic_item_header_id"  INTEGER NOT NULL,
PRIMARY KEY ("id" ASC),
FOREIGN KEY ("ic_item_header_id") REFERENCES "t_ic_item_header" ("id"),
UNIQUE ("index" ASC, "ic_item_header_id" ASC)
);
    ''',
    '''
    CREATE TABLE "t_jindee" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"name"  TEXT NOT NULL,
"userName"  TEXT NOT NULL,
"userPw"  TEXT NOT NULL,
"DBAddress"  TEXT NOT NULL,
"DBName"  TEXT NOT NULL
);
    ''',
    '''
    CREATE VIEW "v_item_table" AS SELECT t_ic_item_header.*,t_user.user as user_name ,t_project.name as project_name
FROM t_ic_item_header,t_user,t_project
WHERE t_ic_item_header.user_id = t_user.id and t_ic_item_header.project_id = t_project.id;
    '''
]