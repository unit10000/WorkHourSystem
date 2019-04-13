from whmgsystem.utils import timeUtils
from whmgsystem.model import *
from flask_login import login_user,login_required,current_user,logout_user
def indexData(current_project_id):
    '''
    普通用户首页数据(弃用)
    :param current_project_id:
    :return:
    '''
    data = {}
    my_department = current_user.department
    my_company = my_department.company
    my_projects = current_user.projects
    current_project = Project.query.filter(Project.id == current_project_id).first()
    if not current_project:
        for project in my_projects:
            if project.status == 0:
                current_project = project
                break
    current_work_hours = WorkHour.query.filter(WorkHour.user_id == current_user.id,
                                               WorkHour.time == timeUtils.getTime("%Y-%m-%d")).all()

    data['user'] = current_user
    data['company'] = my_company
    data['department'] = my_department
    data['projects'] = my_projects
    data['work_hours'] = current_work_hours
    data['current_project'] = current_project
    return data
def selectWorkHoursData(current_project_id,starTime,endTime):
    '''
    查询工时数据首页
    :param current_project_id: 需要查询的项目id
    :param starTime: 起始时间
    :param endTime: 结束时间
    :return:
    '''
    data = {}
    my_department = current_user.department
    my_company = current_user.get_company()
    my_projects = current_user.projects
    current_project = Project.query.filter(Project.id == current_project_id).first()
    if not current_project:  # 当前项目为空寻找第一个进行中项目为当前项目
        for project in my_projects:
            if project.status == 0:
                current_project = project
                break
    if starTime == None or starTime == "" or endTime == None or endTime == "":  # 时间区间为空设置当月时间为区间
        starTime = timeUtils.getTime("%Y-%m-") + "01"
        endTime = timeUtils.getTime("%Y-%m-") + timeUtils.getMonthLastDay(timeUtils.getTime("%Y"),
                                                                          timeUtils.getTime("%m"))
    # 根据条件查询工时
    work_hours = []
    if current_project:
        work_hours = WorkHour.query.filter(WorkHour.project_id == current_project.id,
                                           WorkHour.user_id == current_user.id).filter(WorkHour.date >= starTime,
                                                                                       WorkHour.date <= endTime).all()
    data['date_list'] = timeUtils.getDateList(starTime,endTime)
    for item , index in zip(data['date_list'],range(0,len(data['date_list']))):
        if item['date'] == timeUtils.getTime("%Y-%m-%d"):
            data['current_date'] = index+1#得到今天在在日期列表中的索引用于前端标黄
            break;
    data['user'] = current_user
    data['company'] = my_company
    data['department'] = my_department
    data['projects'] = my_projects
    data['work_hours'] = work_hours
    data['current_project'] = current_project
    data['startime'] = starTime
    data['endtime'] = endTime
    return data
def makeBomData(bom_id):
    '''
    bom制作页面数据
    :param bom_id: bom表id
    :return:
    '''
    data = {}
    data['current_bom'] =None
    my_company = current_user.get_company()
    boms = ItemTable.query.filter(ItemTable.user_id==current_user.id).order_by(ItemTable.date.desc(),ItemTable.id.desc()).all()
    #companys = Company.query.filter(Company.status > -1).all()
    # company_all = []
    # if companys:
    #     company_all.append(my_company)
    #     for c in companys:
    #         if c != my_company:
    #             company_all.append(c)
    if bom_id != '' and bom_id!=None:
        #如果有bom_id 则查找此bom数据返回
        item_table_view = ItemTableView.query.get(int(bom_id))
        data['current_bom'] = item_table_view
    if not data['current_bom'] and bom_id!='-1':
        if boms:
            data['current_bom'] = ItemTableView.query.get(int(boms[0].id))
    data['projects'] = current_user.projects
    # data['companys'] = company_all
    data['user'] = current_user
    data['company'] = my_company
    data['bom_list'] = boms
    return data