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
        try: data.update( {item['name'] : item['value']} )
        except KeyError as e:
            try: data.update( {item['name'] : item.get('value','0')} )
            except KeyError as e:
                data.update( {item['id'] : item['value']} )
        except: raise
    return data

def simpleCleansing( findAll_input ):
    return dict(
        ( item['name'], item.get('value','') ) for item in findAll_input
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

def addShippingAddress( url, session, customer ):
    respQuickPay = session.get( url )
    logging_filing_html( addShippingAddress, respQuickPay )

    inputORselect = re.compile( "input|select" )
    soup = htmlParser( respQuickPay.text )
    tagAttrs = [ tag.attrs for tag in soup.find_all( name=inputORselect) ]

    data = cleansingStrategy['detail']( tagAttrs )
    data.update( {'CheckPayment':'on', 'CheckMember':'on'} )
    data.update( customer.order )
    if 'autobilling' in customer.name:
        data.update( customer.autoBillingData )
    allPayTradeNo = data["AllPayTradeNo"]

    with open(f'json/addShippingAddress_data_{customer.name}.json','w') as file:
        import json
        json.dump( data, file, indent=4, ensure_ascii=False )

    return respQuickPay, data, allPayTradeNo

def doAutoSubmitForm( respQuickPay, data, session ):
    response = session.post( respQuickPay.url, data )
    logging_filing_html( doAutoSubmitForm, response )

    soup = htmlParser( response.text )
    action_url = soup.find(name="form").attrs['action']
    findAll_input = [ tag.attrs for tag in soup.find_all(name="input") ]
    data = cleansingStrategy['detail']( findAll_input )
    return action_url, data

def aioCheckout( action_url, data, session ):
    response = session.post( action_url, data )
    logging_filing_html( aioCheckout, response )

    soup = htmlParser( response.text )
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
    action_url = ecpayData['CurrentDomain'] + action
    return action_url, data

def rtnPaymentType( action_url, data, session, customer ):
    response = session.post( action_url , data )
    logging_filing_html( rtnPaymentType, response )

    soup = htmlParser( response.text )
    action_url = soup.find(name='form').attrs['action']
    findAll_input = [ tag.attrs for tag in soup.find_all(name='input') ]
    data = cleansingStrategy['simple']( findAll_input )

    with open(f'json/rtnPaymentType_data_{customer.name}.json', 'w') as file:
        import json
        json.dump( data, file, indent=4, ensure_ascii=False )

    return action_url, data

def barcodePaymentInfo( action_url, data, session ):
    response = session.post( action_url, data )
    logging_filing_html( barcodePaymentInfo, response )

    soup = htmlParser( response.text )
    src = soup.find(name="iframe").attrs['src']
    base_url = response.url.strip( response.request.path_url )
    return ''.join( (base_url, src) )
