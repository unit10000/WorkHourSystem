# from whmgsystem.conf import setting
# from whmgsystem.syslog import systemlog
# from whmgsystem.utils import  timeUtils
# def selectAll():
#     sql = 'SELECT * FROM t_company where status>-1 '
#     return setting.dbpool_util.execute_query(sql)
# def selectOneCompany(id):
#     sql = 'SELECT * FROM t_company where  id=? '
#     return setting.dbpool_util.execute_query(sql,(id,))