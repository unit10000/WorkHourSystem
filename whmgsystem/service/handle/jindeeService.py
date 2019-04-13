from whmgsystem.dao import jindeeDao
from whmgsystem.utils import DbPoolUtil
from flask_login import login_user,login_required,current_user,logout_user
from whmgsystem.model import *
from whmgsystem import db
from whmgsystem.conf.setting import STR_DATA_ERROR,STR_ERROR,STR_SUCCESS
from whmgsystem.syslog import systemlog
import time
def like_ICItem(data,types,like=True):
    '''
    根据类型模糊搜索物料
    :param data: 模糊检索数据
    :param types: 类型
    :return: 所有检索结果集
    '''
    dbpool = DbPoolUtil.get_dbpool(str(current_user.get_company().jindee_id))
    if not dbpool:
        systemlog.log_error(current_user.department.company.name+"：未找到金蝶数据库")
        return []
    if like:
        rows = jindeeDao.like_ICItem(dbpool,data,types)
    else:
        rows = jindeeDao.select_ICItem(dbpool, data, types)
    ret_list = rows if type(rows)==list else []
    for row  in  ret_list:
        if not row['FQty']==None:
            row['FQty'] = float(row['FQty'])
    return ret_list
def select_ICItems(data,install_num,item_num,type):
    '''
    批量检索物料
    :param data:检索物料关键词
    :param install_num:安装位号
    :param item_num:物料数量
    :param type:检索类型
    :return:
    '''
    ret_list=[]
    ret_data = {}
    item_s = data.split("\n")
    install_nums = install_num.split("\n")
    item_nums = item_num.split("\n")
    input_number = len(item_s)
    if input_number > 200:
        ret_data['status'] = False
        ret_data['message'] = '一次最多只可导入200条！'
        return ret_data
    for i,index in zip(item_s , range(0,len(item_s))):
        if i=='':
            continue
        select_list = like_ICItem(i,type,like=False)
        item_dict={}
        item_dict["jieguo"] = select_list
        item_dict['select_data'] = i
        if len(install_nums)>index:
            item_dict['install_num']=install_nums[index]
        else:
            item_dict['install_num'] = ""
        if len(item_nums) > index and item_nums[index]!="":
            item_dict['item_num'] = item_nums[index]
        else:
            item_dict['item_num'] = "1"
        ret_list.append(item_dict)
    ret_data['status'] = True
    ret_data['items'] = ret_list
    ret_data['input_number'] = input_number
    ret_data['out_number'] = len(ret_list)
    return ret_data
def save_ic_table(table_id,jsonObj):
    '''
    保存bom列表
    :param table_id:bom表id
    :param jsonObj:bom表json数据
    :return:操作结果
    '''
    ret_message = STR_ERROR
    item_id = None
    try:
        #根据bom_id查询bom
        itemTable = ItemTable.query.get(int(table_id))
    except Exception as e:
        systemlog.log_error(e)
        itemTable =None
    if itemTable:#bom表存在则先全部删除
        item_id = itemTable.id
        if delete_item_table(itemTable.id)==False:
            return ret_message, None
    itemTable = ItemTable(project_id=jsonObj['project_id'], file_name=jsonObj['file_name'],
                          file_id=jsonObj['file_id'],
                          item_num=jsonObj['item_num'], version=jsonObj['version'],
                          user_id=current_user.id, auditing=jsonObj['auditing'],
                          proofreading=jsonObj['proofreading'], approval=jsonObj['approval'],
                          signer=jsonObj['signer'], date=jsonObj['date'])
    if item_id:
        itemTable.id=item_id
    try:#进行添加
        db.session.add(itemTable)
        db.session.commit()
        items = []
        for item in jsonObj['items']:
            it = ItemDetail(index=item['index'], item_number=item['item_number'], name=item['name'],
                            model=item['model'], note=item['note'], install_number=item['install_number'],
                            unit=item['unit'], number=item['number'], remark=item['remark'], ic_item_header_id=itemTable.id)
            items.append(it)
        db.session.add_all(items)
        db.session.commit()
        ret_message = STR_SUCCESS
    except Exception as e:#出现异常全部滚回
        systemlog.log_error(e)
        if itemTable:
            delete_item_table(itemTable.id)
    if itemTable:
        bom_id = itemTable.id
    else:
        bom_id=None
    return ret_message,bom_id
def copy_ic_table(jsonObj):
    '''
    复制bom表
    :param jsonObj: bomjson数据
    :return:
    '''
    ret_message = STR_ERROR
    itemTable = ItemTable(project_id=jsonObj['project_id'],file_name=jsonObj['file_name'],file_id=jsonObj['file_id'],
                          item_num=jsonObj['item_num'],version=jsonObj['version'],
                          user_id=current_user.id,auditing=jsonObj['auditing'],
                          proofreading=jsonObj['proofreading'],approval=jsonObj['approval'],
                          signer=jsonObj['signer'],date=jsonObj['date'])
    try:#进行添加
        db.session.add(itemTable)
        db.session.commit()
        items = []
        for item in jsonObj['items']:
            it = ItemDetail(index=item['index'], item_number=item['item_number'], name=item['name'],
                            model=item['model'], note=item['note'], install_number=item['install_number'],
                            unit=item['unit'], number=item['number'], remark=item['remark'], ic_item_header_id=itemTable.id)
            items.append(it)
        db.session.add_all(items)
        db.session.commit()
        ret_message = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)#出现异常全部滚回
        if itemTable.id:
            delete_item_table(itemTable.id)
    if itemTable.id:
        bom_id = itemTable.id
    else:
        bom_id=None
    return ret_message,bom_id
def delete_item_table(table_id):
    '''
    删除bom表
    :param table_id: bom表id
    :return:
    '''
    isTrue = False
    try:
        itemTable = ItemTable.query.get(int(table_id))
        sql = 'DELETE FROM ' + ItemDetail.__tablename__ + ' WHERE  ic_item_header_id = ' + str(itemTable.id)
        db.session.execute(sql)
        db.session.commit()
        db.session.delete(itemTable)
        db.session.commit()
        isTrue = True
    except Exception as e:
        systemlog.log_error(e)
    return isTrue

def delete_bom(bom_id):
    '''
    删除bom表
    :param bom_id: bomid
    :return:
    '''
    delete_item_table(bom_id)
    return STR_SUCCESS
def add_jindee_config(name,userName,userPw,DBAddress,DBName):
    '''
    添加金蝶配置
    :param name: 名称
    :param userName: 数据库用户名
    :param userPw: 数据库密码
    :param DBAddress: 数据库地址
    :param DBName: 数据库名称
    :return:
    '''
    try:
        jindee = Jindee(name=name, userName=userName, userPw=userPw, DBAddress=DBAddress, DBName=DBName)
        db.session.add(jindee)
        db.session.commit()
        message = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        message = STR_ERROR
    return message
def delete_jindee(jindee_id):
    '''
    删除金蝶配置
    :param jindee_id: 金蝶配置id
    :return:
    '''
    try:
        jindee = Jindee.query.get(int(jindee_id))
        db.session.delete(jindee)
        db.session.commit()
        message = STR_SUCCESS
    except Exception as e:
        systemlog.log_error(e)
        message = STR_ERROR
    return message
if __name__ == '__main__':
    data='''
    027.01.0160
027.02.0010
027.01.0154

    '''
    print(select_ICItems(data,"FNumber"))