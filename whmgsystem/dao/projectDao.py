#
# from whmgsystem.syslog import systemlog
# from  whmgsystem.utils import timeUtils
# from whmgsystem.conf import setting
# def selectAll(company_id):
#     sql = "SELECT * FROM t_project , t_department WHERE t_department.company_id = ? and t_project.department_id = t_department.id"
#     return setting.dbpool_util.execute_query(sql,(company_id,))
# def selectAllForUser(user_Id):
#     sql = "SELECT * FROM t_project ,t_department WHERE  t_project.id in (SELECT  project_id FROM t_project_user WHERE user_id = ?) and t_project.department_id=t_department.id"
#     return setting.dbpool_util.execute_query(sql,(user_Id,))
# def getProjectWorkTime(project_id,starTime,endTime):
#     sql='''
#         SELECT
#             *,sum(worktime),COUNT(worktime)
#         FROM
#             t_project_user
#         LEFT JOIN t_work_record ON t_project_user.user_id = t_work_record.user_id
#         AND t_project_user.project_id = t_work_record.project_id
#         And t_work_record.date >= ?
#         AND t_work_record.date <= ?
#         left join t_user on t_user.id = t_project_user.user_id
#         WHERE t_project_user.project_id=?
#         and t_user.id>0
#         GROUP BY
#             t_project_user.user_id
#         ORDER BY
#             COUNT(worktime)
#         '''
#     return setting.dbpool_util.execute_query(sql,(starTime,endTime,project_id))
#
# def getProjectInf(project_id):
#     sql = '''
#         SELECT
#             t_project.*, t_department.*, t_user.user
#         FROM
#             t_project,
#             t_department,
#             t_project_user,
#             t_user
#         WHERE
#             t_project.department_id = t_department.id
#         AND t_project.id = t_project_user.project_id
#         AND t_project_user.status = 2
#         AND t_user.id = t_project_user.user_id
#         AND t_project.id = ?
#     '''
#     return setting.dbpool_util.execute_query_single(sql, (project_id, ))
# def getProjectUser(project_id):
#     sql='''SELECT
#             *
#         FROM
#             t_user,
#             t_project_user,
#             t_department
#         WHERE
#             t_project_user.project_id = ?
#         AND t_user.id = t_project_user.user_id
#         AND t_user.department_id = t_department.id
#         ORDER BY
#         t_project_user.status DESC'''
#     return setting.dbpool_util.execute_query(sql, (project_id, ))
#
# def add(project_id , name, department_id,u_id):
#     sql = '''
#         INSERT INTO t_project (
#             id,
#             name,
#             regtime,
#             department_id
#         )
#         VALUES
#             (?, ?, ?, ?)
#     '''
#     sql2='''
#     INSERT INTO t_project_user (
#                     user_id,
#                     project_id,
#                     status,
#                     addtime
#                 )
#                 VALUES
#                     (?, ?, ?, ?)
#
#     '''
#     isTrue = False
#     conn = setting.dbpool_util.getConn()
#     cur = conn.cursor()
#     try:
#         cur.execute("PRAGMA foreign_keys=ON")
#         result = cur.execute(sql, (project_id,name, timeUtils.getTime('%Y-%m-%d'),department_id))
#         ret =result.rowcount
#         if ret > 0:
#             result = cur.execute(sql2, (u_id, project_id,2, timeUtils.getTime('%Y-%m-%d')))
#             ret = result.rowcount
#             if ret>0:
#                 conn.commit()
#                 isTrue= True
#     except Exception as e:
#         systemlog.log_error(e)
#     return isTrue
# def updata(project_id , name, department_id):
#     sql = '''
#            UPDATE t_project
#             SET
#              name = ?,
#              department_id = ?
#             WHERE
#                 id=?
#         '''
#     setting.dbpool_util.execute_iud("PRAGMA foreign_keys=ON")
#     ret = setting.dbpool_util.execute_iud(sql, (name, department_id,project_id))
#     return True if ret > 0 else False
# def addUser(project_id,user_id,type):
#     sql = '''
#                INSERT INTO t_project_user (
#                     user_id,
#                     project_id,
#                     status,
#                     addtime
#                 )
#                 VALUES
#                     (?, ?, ?, ?)
#         '''
#     setting.dbpool_util.execute_iud("PRAGMA foreign_keys=ON")
#     ret = setting.dbpool_util.execute_iud(sql, (int(user_id), project_id,type, timeUtils.getTime('%Y-%m-%d')))
#     return True if ret > 0 else False
# def upProjectUser(user_id , project_id , status):
#     sql = '''
#                UPDATE t_project_user
#                 SET status = ?
#                 WHERE
#                 user_id = ?
#                 AND project_id = ?
#             '''
#     setting.dbpool_util.execute_iud("PRAGMA foreign_keys=ON")
#     ret = setting.dbpool_util.execute_iud(sql, (status, user_id, project_id))
#     return True if ret > 0 else False
# def setType(id,type):
#     sql = '''
#     UPDATE t_project
#     SET status = ?
#     WHERE
#         id =?
#     '''
#     ret = setting.dbpool_util.execute_iud(sql,(type,id))
#     return True if ret > 0 else False
# def dele(id):
#     sql = '''
#         DELETE FROM t_project WHERE id = ?
#         '''
#     setting.dbpool_util.execute_iud("PRAGMA foreign_keys=OFF")
#     ret = setting.dbpool_util.execute_iud(sql, (id,))
#     return True if ret > 0 else False
# def deleUser(project_id,uid):
#     sql = '''
#             DELETE FROM t_project_user WHERE user_id = ? and project_id=?
#             '''
#     ret = setting.dbpool_util.execute_iud(sql, (uid,project_id ))
#     return True if ret > 0 else False
# def seleLike(like):
#     sql='''SELECT id ,name FROM t_project WHERE id LIKE ?  or name LIKE ?'''
#     return setting.dbpool_util.execute_query(sql, ('%'+like+'%', '%'+like+'%'))
# def up_name(id,name):
#     sql = '''
#                 UPDATE t_project SET name=? WHERE id=?
#                 '''
#     ret = setting.dbpool_util.execute_iud(sql, (name,id))
#     return True if ret > 0 else False