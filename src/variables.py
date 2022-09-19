from datetime import date, datetime, timedelta


import dateutil.relativedelta


today_date = date.today()
today = today_date.strftime("%d.%m.%Y")
Jahr = today_date.strftime("%y")
now = datetime.now()
firstpreviousM = today_date + dateutil.relativedelta.relativedelta(day=1, months=-1)
lastpreviousM = today_date + dateutil.relativedelta.relativedelta(day=31, months=-1)

firstcurrentM = today_date + dateutil.relativedelta.relativedelta(day=1)
lastcurrentM = today_date + dateutil.relativedelta.relativedelta(day=31)


intervalls15 = {'15 Min': 15, '30 Min': 30, '45 Min': 45, '60 Min': 60, '1 Std:15 Min': 75, '1 Std:30 Min': 90,
              '1 Std:45 Min': 105, '2 Std': 120, '2 Std:15 Min': 195, '2 Std:30 Min': 210, '2 Std:45 Min': 225,
              '3 Std': 240, '3 Std:15 Min': 255, '3 Std:30 Min': 270, '3 Std:45 Min': 285, '4 Std': 300,
              '4 Std:15 Min': 315, '4 Std:30 Min': 330, '4 Std:45 Min': 345, '5 Std': 360, '5 Std:15 Min': 375,
              '5 Std:30 Min': 390, '5 Std:45 Min': 405, '6 Std': 420, '6 Std:15 Min': 435, '6 Std:30 Min': 450,
              '6 Std:45 Min': 465, '7 Std:15 Min': 495, '7 Std': 540, '7 Std:30 Min': 510, '7 Std:45 Min': 525,
                '8 Std' : 540}


intervalls6 = {'15 Min': 6, '30 Min': 12, '45 Min': 18, '60 Min': 24, '1 Std:15 Min': 30, '1 Std:30 Min': 36,
               '1 Std:45 Min': 42, '2 Std': 48, '2 Std:15 Min': 54, '2 Std:30 Min': 60, '2 Std:45 Min': 66,
               '3 Std': 72, '3 Std:15 Min': 78, '3 Std:30 Min': 84, '3 Std:45 Min': 90, '4 Std': 96, '4 Std:15 Min': 102,
               '4 Std:30 Min': 108, '4 Std:45 Min': 114, '5 Std': 120, '5 Std:15 Min': 126, '5 Std:30 Min': 132,
               '5 Std:45 Min': 138, '6 Std': 144, '6 Std:15 Min': 150, '6 Std:30 Min': 156, '6 Std:45 Min': 162,
               '7 Std:15 Min': 168, '7 Std': 174, '7 Std:30 Min': 180, '7 Std:45 Min': 186, '8 Std': 192}


# List of working days in current month

def workdays():
    start = firstcurrentM
    end = today_date
    days = []
    excluded = (6, 7)

    while start <= end:
        if start.isoweekday() not in excluded:
            days.append(start)
        start += timedelta(days=1)
    #return days
    daysint = []
    for i in days:
        daysint.append(i.day)

    return daysint
