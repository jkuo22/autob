from customers import Customer
from datetime import date
import calendar as cal
import json


today = date.today()
lastday_month = cal.monthrange(today.year, today.month)[1]
days = dict(
    ( day, date(today.year, today.month, day) )
    for day in range( 1, lastday_month+1 )
    )


with open('payers.json', 'r') as jsonf:
    loadPayers = json.load( jsonf )

def appendPayer( rotation, name, orderName, base, adv, billday ):
    bday = days.get( billday, today )
    if bday.month in rotation:
        Customer( name, orderName, base=base, adv=adv, billday=bday )

for payer in loadPayers:
    if payer['charge']:
        appendPayer( payer['rotation'], payer['name'], **payer['order'] )
