from customers import Customer
from datetime import date
import calendar as cal


today = date.today()
lastday_month = cal.monthrange(today.year, today.month)[1]

days = dict( ( day, date(today.year, today.month, day) )
    for day in range( 1, lastday_month+1 ) )

month = today.month if today.month in range(2, 13, 3) else 8
quarterly8 = date(today.year, month, 8)

#for _ in range(3):
#    Customer('max188', 'Maxx', base=2, billday=quarterly8 )

Customer('gorich1688', '阿勇', base=4, billday=days[21])
Customer('grace', 'Grace', adv=1, billday=days[10])
Customer('hamburger', 'Hamburger', base=1, adv=2, billday=days[15])
Customer('ding', 'Ding', base=2, billday=days[1])
#Customer('gao', 'Gao', base=1, billday=days[6])
#Customer('autobilling_test', '自動繳費單測試', base=1, adv=1, billday=today)
