def sum_work_hours(lists):
    '''
    计算工时模型的工时和
    :param lists:
    :return:
    '''
    sum_hour = 0
    for work_hour in lists:
        sum_hour+=work_hour.worktime
    return sum_hour
def marge_work_hours(work_hours_list,date_list):
    '''
    生成工时和日期对应数据
    :param work_hours_list: 工时list
    :param date_list: 日期list
    :return:
    '''
    ret_map ={}
    for date in date_list:
        ret_map[date['date']] = ''
    for work_hour in work_hours_list:
        ret_map[work_hour.date] = work_hour.worktime
    return ret_map