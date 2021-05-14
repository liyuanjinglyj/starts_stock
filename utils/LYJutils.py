import time,datetime
import pandas as pd
#获取一年前的时间
def get_a_year_ago_date():
    now = datetime.datetime.now()
    timeArray = time.strptime(now.strftime("%Y%m%d"), "%Y%m%d")
    timeStamp = (time.mktime(timeArray))  # 转化为时间戳
    end_time = time.strftime('%Y-%m-%d', time.localtime(timeStamp))
    start_year = int(time.strftime('%Y', time.localtime(timeStamp))) - 1
    month_day = time.strftime('%m%d', time.localtime(timeStamp))
    start_time = '{}{}'.format(start_year, month_day)
    return start_time

#获取当前时间前一个月的时间
def get_a_month_ago_date():
    now = datetime.datetime.now()
    monthOldday = datetime.timedelta(days=31)
    dayto=now-monthOldday
    return dayto.strftime("%Y%m%d")

def str_of_num(num):
    '''
    递归实现，精确为最大单位值 + 小数点后三位
    '''
    def strofsize(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return strofsize(num, level)
        else:
            return num, level
    units = ['', '万', '亿']
    num, level = strofsize(num, 0)
    if level > len(units):
        level -= 1
    return '{}{}'.format(round(num, 2), units[level])
'''
#判断今天是否为工作日并且是否为交易时间，如果不是返回上一个工作日
def isWorking_now():
    return get_datetime()


#获取前一个工作日
def get_datetime():
    # 测试使用:添加日期参数,如 2020-04-27
    # today = datetime.strptime(daystr,'%Y-%m-%d').date()
    # 默认按当天日期计算
    today = datetime.date.today()
    # eval()函数 把字符串类型转化为 双引号内类型(int)
    year = eval(str(today).split("-")[0])
    cal = China()
    # 所有节假日日期放入此列表
    holiday_list = []
    for i in cal.holidays(year):
        day = i[0].strftime('%Y-%m-%d')
        holiday_list.append(day)

    for i in range(1, 10):
        days = datetime.timedelta(days=i)
        item_day = today - days
        # 获取日期是周几(0,1,2,3,4,5,6)
        week = item_day.weekday()
        is_work = cal.is_working_day(item_day)
        if (item_day not in holiday_list and is_work == True) or (week not in (5, 6) and is_work == True):
            min_datetime = pd.to_datetime(item_day)
            month_end = (min_datetime + datetime.timedelta(days=0)).strftime("%Y%m%d")
            return month_end
            
'''