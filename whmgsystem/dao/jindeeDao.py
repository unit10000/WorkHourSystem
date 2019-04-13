
def like_ICItem(dbpool ,data,type):
    '''
    模糊查询物料
    :param dbpool: 数据库池
    :param data: 关键词
    :return: 查询结果
    '''
    sql = "select top 20 t_ICItem.FItemID,t_ICItem.FModel,t_ICItem.FName,t_ICItem.FNote,t_ICItem.FNumber,ICInventory.FQty from  t_ICItem  left join ICInventory  on t_ICItem.FItemID = ICInventory.FItemID WHERE "+type+" like '%"+data+"%'"
    result1 = dbpool.execute_query(sql)
    return result1

def select_ICItem(dbpool ,data,type):
    '''
    模糊查询物料
    :param dbpool: 数据库池
    :param data: 关键词
    :return: 查询结果
    '''
    sql = "select top 20 t_ICItem.FItemID,t_ICItem.FModel,t_ICItem.FName,t_ICItem.FNote,t_ICItem.FNumber,ICInventory.FQty from  t_ICItem  left join ICInventory  on t_ICItem.FItemID = ICInventory.FItemID WHERE "+type+" = '"+data+"'"
    result1 = dbpool.execute_query(sql)
    return result1