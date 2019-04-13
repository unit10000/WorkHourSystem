# from whmgsystem.conf import setting
# from whmgsystem.syslog import systemlog
# from whmgsystem.utils import  timeUtils
#
# def selectAll(company_id):
#     sql = 'SELECT * FROM t_department where type>-1 and company_id = ?'
#     return setting.dbpool_util.execute_query(sql,(company_id,))
#
# def add(name,company_id):
#     sql = '''INSERT INTO t_department(name,regtime,company_id) VALUES (?,?,?)'''
#     ret = setting.dbpool_util.execute_iud(sql,(name,timeUtils.getTime('%Y-%m-%d'),company_id))
#     return True if ret > 0 else False
#
# def setType(id,type):
#     sql = '''
#     UPDATE t_department
#     SET type = ?
#     WHERE
#         id =?
#     '''
#     ret = setting.dbpool_util.execute_iud(sql,(type,id))
#     return True if ret > 0 else False
#
# def dele(id):
#     sql = '''
#         DELETE FROM t_department WHERE id = ?
#         '''
#     ret = setting.dbpool_util.execute_iud(sql, (id, ))
#     return True if ret > 0 else False