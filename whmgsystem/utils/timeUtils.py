import time
import datetime
import json ,requests
#"%Y-%m-%d %H:%M:%S"
import calendar
num_to_ch_dic = { 0:'一', 1:'二', 2:'三', 3:'四', 4:'五',5:'六',6:'日'}
def getTime(s):
    '''
    获取str时间
    :param s:
    :return:
    '''
    return time.strftime(s)
def getDateList(starTime,endTime,weekday=True):
    '''
    获取起始日期到结束日期的全部日期
    :param starTime: 起始日期
    :param endTime: 结束日期
    :param weekday: 是否获取星期信息
    :return:
    '''
    datestart = datetime.datetime.strptime(starTime, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(endTime, '%Y-%m-%d')
    dateList=[]
    if weekday:
        dateList.append({'date':datestart.strftime('%Y-%m-%d'),'weekday':num_to_ch_dic[datestart.weekday()]})
    else:
        dateList.append(starTime)
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        if weekday:
            dateList.append({'date':datestart.strftime('%Y-%m-%d'),'weekday':num_to_ch_dic[datestart.weekday()]})
        else:
            dateList.append(datestart.strftime('%Y-%m-%d'))
    return dateList
def getMonthLastDay(year,month):
    '''
    获取某月最后一天
    :param year: 年
    :param month: 月
    :return:
    '''
    return str(calendar.monthrange(int(year), int(month))[1])
def getWeekend(date_array):
    '''
    获取节假日信息（弃用）
    :param date_array:
    :return:
    '''
    r = requests.post(url='http://tool.bitefu.net/jiari/', data={'d':date_array},
                      headers={'Content-Type': 'application/x-www-form-urlencoded'})
    return r.text
if __name__ == '__main__':
    # print(getMonthLastDay('2018',2))
    # print ((getTime("%Y-%m-%d")))
    # a = getWeekend('20130101,20190102')
    # print(a)
    print(getDateList('2019-01-01','2019-01-08'))