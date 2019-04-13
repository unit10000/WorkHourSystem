# from whmgsystem.conf import setting
# from whmgsystem.syslog import systemlog
# from whmgsystem.utils import timeUtils
# from whmgsystem.model.user import User
# from whmgsystem.model.company import Company
# def userLogin(user,pw):
#     sql = "SELECT * FROM t_user , t_department , t_company WHERE user=? and pass=? and t_user.department_id = t_department.id and t_department.company_id = t_company.id"
#     ret =setting.dbpool_util.execute_query_single(sql,(user,pw))
#     user = User(**ret)
#     user.company.id = ret['company_id']
#     return user
# def findById(id):
#     sql = "SELECT * FROM t_user , t_department , t_company WHERE t_user.id=? and t_user.department_id = t_department.id and t_department.company_id = t_company.id"
#     ret = setting.dbpool_util.execute_query_single(sql, (id, ))
#     user = User(**ret)
#     user.company.id = ret['company_id']
#     return user
# def userRegister(user,pw,department_id,company_id):
#     sql = "INSERT INTO t_user (user, pass,regtime,department_id,company_id) VALUES (?,?,?,?,?)"
#     ret = setting.dbpool_util.execute_iud(sql, (user, pw,timeUtils.getTime("%Y-%m-%d %H:%M:%S"),department_id,company_id))
#     return True if ret > 0 else False
# def selectUserOnDepartment(d_id):
#     sql = "SELECT t_user.id,t_user.user ,t_user.regtime FROM t_user WHERE department_id=? and type>-1"
#     return setting.dbpool_util.execute_query(sql,(d_id,))
# def selectIndepartmentNotProject(d_id,p_id):
#     sql = '''SELECT
#                 t_user.id,
#                 t_user.user
#             FROM
#                 t_user
#             WHERE
#                 id NOT IN (
#                     SELECT
#                         user_id
#                     FROM
#                         t_project_user
#                     WHERE
#                         project_id = ?
#                 )
#             AND department_id = ?
#             '''
#     return setting.dbpool_util.execute_query(sql, (p_id,d_id))
# def dele(id):
#     sql = "DELETE FROM t_user WHERE id = ?"
#     setting.dbpool_util.execute_iud("PRAGMA foreign_keys=OFF")
#     return setting.dbpool_util.execute_iud(sql, (id,))
# def getWorkInf(p_id,u_id,startTime,endTime):
#     #SELECT * FROM t_work_record WHERE t_work_record.project_id='RA171901' and t_work_record.user_id=33
#     sql = '''
#         SELECT
#             *
#         FROM
#             t_work_record
#         WHERE
#             t_work_record.project_id = ?
#         AND t_work_record.user_id = ?
#         AND t_work_record.date >= ?
#         AND t_work_record.date <= ?
#                 '''
#     return setting.dbpool_util.execute_query(sql, (p_id, u_id,startTime,endTime))
#
# def getToDayWorkInf(u_id):
#     #SELECT * FROM t_work_record WHERE t_work_record.project_id='RA171901' and t_work_record.user_id=33
#     sql = '''
#         SELECT
#             *
#         FROM
#             t_work_record,t_project
#         WHERE
#             t_work_record.user_id = ?
#         AND t_work_record.time = ?
#         AND t_project.id = t_work_record.project_id
#                 '''
#     return setting.dbpool_util.execute_query(sql, ( u_id,timeUtils.getTime("%Y-%m-%d")))
# def setComPany(id,comPany_id):
#     sql = '''
#     UPDATE t_user
#     SET company_id = ?
#     WHERE
#         id =?
#     '''
#     ret = setting.dbpool_util.execute_iud(sql,(comPany_id,id))
#     return True if ret > 0 else False