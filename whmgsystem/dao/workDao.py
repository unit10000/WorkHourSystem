# from whmgsystem.conf import setting
# from whmgsystem.syslog import systemlog
# from whmgsystem.utils import timeUtils
# def selectWorkTimeByOneDay(user_id,project_id,date):
#     sql = "SELECT * FROM t_work_record WHERE user_id=? and project_id=? and date=?"
#     return setting.dbpool_util.execute_query_single(sql,(user_id,project_id,date))
# def upWorkTime(user_id , project_id, date , time):
#     ret = selectWorkTimeByOneDay(user_id , project_id , date)
#     isTrue = False
#     count = 0
#     if ret is not None:
#         try:
#             setting.dbpool_util.execute_iud("PRAGMA foreign_keys=ON")
#             sql = "UPDATE t_work_record SET worktime = ? ,time = ? WHERE id = ?"
#             count = setting.dbpool_util.execute_iud(sql, (time,timeUtils.getTime("%Y-%m-%d"),ret[0]))
#         except Exception as e:
#             systemlog.log_error(e)
#     else:
#         try:
#             setting.dbpool_util.execute_iud("PRAGMA foreign_keys=ON")
#             sql = "INSERT INTO t_work_record (user_id,project_id ,worktime,date,time) VALUES (?,?,?,?,?)"
#             count = setting.dbpool_util.execute_iud(sql, (user_id,project_id,time,date,timeUtils.getTime("%Y-%m-%d")))
#         except Exception as e:
#             systemlog.log_error(e)
#     if count > 0 :
#         isTrue=True
#     return isTrue
# def selectWorkTime(starTime,endTime):
#     sql = "SELECT * FROM t_work_record WHERE  date>=? and date<=?"
#     return setting.dbpool_util.execute_query(sql,(starTime,endTime))
# def dele(w_id,u_id):
#     sql = '''
#         DELETE FROM t_work_record WHERE t_work_record.id = ? AND t_work_record.user_id = ?
#     '''
#     ret = setting.dbpool_util.execute_iud(sql, (w_id,u_id))
#     return True if ret > 0 else False