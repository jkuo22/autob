import re, logging
from bs4 import BeautifulSoup
from functools import partial
htmlParser = partial( BeautifulSoup, features='html.parser' )

logging.basicConfig(
    format="%(asctime)s %(levelname)s:%(name)s: %(message)s",
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
    #stream=sys.stderr,
    filename=f'ecpay-billing.log'
)
logger = logging.getLogger( "ecpay" )
#logging.getLogger("chardet.charsetprober").disabled = True

def cleansing( dictList ):
    data = {}
    for item in dictList:
        try:
            data.update( {item['name'] : item.get('value','0')} )
        except KeyError as e:
            data.update( {item['id'] : item['value']} )
    return data

def simpleCleansing( dictList ):
    return dict(
        ( item['name'], item.get('value','') ) for item in dictList
        )

cleansingStrategy = {
    'detail' : cleansing,
    'simple' : simpleCleansing
    }

def logging_filing_html( function, response ):
    """ logging whether the function get called and write html file. """
    logger.info('"%s" called, getting %s', function.__name__, response.url )
    with open( f'html/{function.__name__}.html', 'w' ) as file:
        file.write( response.text )

def getSoup( url, session, function, data=None ):
    print( '###', function.__name__, '>>>', url )
    response = session.post( url, data, allow_redirects=True ) if data else session.get( url, allow_redirects=True )
    logging_filing_html( function, response )
    return response, htmlParser( response.text )

def addShippingAddress( url, session, customer ):
    respQuickPay, soup = getSoup( url, session, addShippingAddress )
    inputORselect = re.compile( "input|select" )
    tagAttrs = [ tag.attrs for tag in soup.find_all( name=inputORselect) ]

    data = cleansingStrategy['detail']( tagAttrs )
    data.update( {'CheckPayment':'on', 'CheckMember':'on'} )
    data.update( customer.order )
    if 'autobilling' in customer.name:
        data.update( customer.autoBillingData )

    allPayTradeNo = data["AllPayTradeNo"]

    #with open(f'json/addShippingAddress_data_{customer.name}.json','w') as fp:
    #    import json
    #    json.dump( data, fp, indent=4, ensure_ascii=False )
    print( '##### respQuickPay.url', respQuickPay.url )
    return respQuickPay.url, data, allPayTradeNo

def doAutoSubmitForm( url, data, session ):
    response, soup = getSoup( url, session, doAutoSubmitForm, data=data )
    action_url = soup.find(name="form").attrs['action']
    findAll_input = [ tag.attrs for tag in soup.find_all(name="input") ]

    data = cleansingStrategy['detail']( findAll_input )
    #print( '##### action_url:', action_url )
    print( '##### response.url:', response.url )
    return action_url, data

def aioCheckout( url, data, session ):
    #url = "https://payment.ecpay.com.tw/Cashier/AioCheckOut"
    response, soup = getSoup( url, session, aioCheckout, data=data )
    action = soup.find(name='form').attrs['action']
    findAll_input = [ tag.attrs for tag in soup.find_all(name='input') ]

    data = cleansingStrategy['simple']( findAll_input )
    find_script = soup.find(name='script')
    RE = re.compile("var (_\w+) = '(.+)'")
    barCodePaymentID = RE.search(find_script.text).group(2)
    data['paymentName'] = barCodePaymentID

    def find_CurntDomain( tag ):
        return eval( re.search('({.+})', tag.text).group(0)
                        .replace('false', '"false"')
                        .replace('true', '"true"') )

    ecpayData = find_CurntDomain( soup.find(name='script', id="ECPayData") )
    #print( '#### ecpayData', ecpay)
    action_url = ecpayData['CurrentDomain'] + action
    return action_url, data

def rtnPaymentType( url, data, session, customer ):
    response, soup = getSoup( url, session, rtnPaymentType, data=data )
    action_url = soup.find(name='form').attrs['action']
    findAll_input = [ tag.attrs for tag in soup.find_all(name='input') ]

    data = cleansingStrategy['simple']( findAll_input )

    #with open(f'json/rtnPaymentType_data_{customer.name}.json', 'w') as fp:
    #    import json
    #    json.dump( data, fp, indent=4, ensure_ascii=False )
    return action_url, data

def barcodePaymentInfo( url, data, session ):
    response, soup = getSoup( url, session, barcodePaymentInfo, data=data )

    src = soup.find(name="iframe").attrs['src']
    base_url = response.url.strip( response.request.path_url )
    return ''.join( (base_url, src) )
