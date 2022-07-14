import os, sys, json, asyncio
from datetime import date, datetime
from pathlib import Path
import requests
from playwright.async_api import async_playwright

os.chdir( Path( sys.argv[0]).parent )
from customers import Customer
from getPaymentNotice import *
import paymentNotices, sendPaymentNotice

dirs = ( 'json', 'pdf', 'html', 'last_known_good' )
for d in dirs:
    if not Path( d ).exists():
        os.mkdir( Path('.').resolve() / Path( d ) )

async def printPDF( customer ):
    with open('setting.json','r') as file:
        setting = json.load( file )
        url = setting['Url']

    with requests.Session() as session:
        quickPay, data, allPayTradeNo = addShippingAddress( url, session, customer )
        action_url, data = doAutoSubmitForm( quickPay, data, session )
        action_url, data = aioCheckout( action_url, data, session )
        action_url, data = rtnPaymentType( action_url, data, session, customer )
        base_PathUrl = barcodePaymentInfo( action_url, data, session )
        BarCodePaymentInfo_Print = session.get( base_PathUrl )
        logger.info( "payment notice for %s is generating...", customer.name )

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto( BarCodePaymentInfo_Print.url )
        filename = ( f'pdf/'
                     f'{allPayTradeNo}_'
                     f'{customer.order["CName"]}.pdf' )
        await page.pdf( path=filename )
        await browser.close()
        sendPaymentNotice.send( f"'{customer.name}' payment notice generated.",
                                filename,
                                sender_token = setting['token'],
                                receiver_id = setting['receiver_id']
                                )

async def main():
    await asyncio.gather(
        *( printPDF( customer ) for customer in Customer.instances
            if customer.billday == date.today() )
        )

asyncio.run( main() )
