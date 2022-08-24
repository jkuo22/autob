from customers import Customer
from datetime import date
import calendar as cal


today = date.today()
lastday_month = cal.monthrange(today.year, today.month)[1]
days = dict(
    ( day, date(today.year, today.month, day) )
    for day in range( 1, lastday_month+1 )
    )

#month = today.month if today.month in range(2, 13, 3) else 8
#quarterly8 = date(today.year, month, 8)
#
#Customer('gorich1688', '阿勇', base=4, billday=days[21])
#Customer('maxxx188', 'MAX', base=6, billday=quarterly8 )
#Customer('grace', 'Grace', adv=1, billday=days[10])
#Customer('hamburger', 'Hamburger', base=1, adv=2, billday=days[15])
#Customer('ding', 'Ding', base=1, billday=days[23])
#Customer('lv', 'LV', adv=1, billday=days[3])
#Customer('autobilling_test', '自動繳費單測試', base=1, adv=1, billday=today)

with open('payers.json', 'r') as jsonf:
    loadPayers = json.load( jsonf )

def appendPayer( rotation, name, orderName, base, adv, billday ):
    bday = days.get( billday, today )
    if bday.month in rotation:
        Customer( name, orderName, base=base, adv=adv, billday=bday )

for payer in loadPayers:
    if payer['charge']:
        appendPayer( payer['rotation'], payer['name'], **payer['order'] )
