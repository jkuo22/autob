import re
RE = re.compile('\d+')

class Subscription:
    def __init__(self, base:int=0, adv:int=0, billday=''):
        self.base = base
        self.adv = adv
        self.billday = billday
        self.order = {
            "InfoModel.ListQuickPayDetail[0].ItemNo": "771755",
            "InfoModel.ListQuickPayDetail[0].ItemName": "基本方案",
            "InfoModel.ListQuickPayDetail[0].SubTotal": "3000",
            "InfoModel.ListQuickPayDetail[0].BuyQty": "0",
            "InfoModel.ListQuickPayDetail[1].ItemNo": "771756",
            "InfoModel.ListQuickPayDetail[1].ItemName": "進階方案",
            "InfoModel.ListQuickPayDetail[1].SubTotal": "5000",
            "InfoModel.ListQuickPayDetail[1].BuyQty": "0",
            "InfoModel.ListQuickPayDetail[2].ItemNo": "771757",
            "InfoModel.ListQuickPayDetail[2].ItemName": "流量超出增購",
            "InfoModel.ListQuickPayDetail[2].SubTotal": "10",
            "InfoModel.ListQuickPayDetail[2].BuyQty": "0",
            "InfoModel.ListQuickPayDetail[3].ItemNo": "771758",
            "InfoModel.ListQuickPayDetail[3].ItemName": "硬碟容量增購",
            "InfoModel.ListQuickPayDetail[3].SubTotal": "20",
            "InfoModel.ListQuickPayDetail[3].BuyQty": "0",
            "InfoModel.ListQuickPayDetail[4].ItemNo": "771759",
            "InfoModel.ListQuickPayDetail[4].ItemName": "設定費",
            "InfoModel.ListQuickPayDetail[4].SubTotal": "1000",
            "InfoModel.ListQuickPayDetail[4].BuyQty": "0",
            "InfoModel.ListQuickPayDetail[5].ItemNo": "771760",
            "InfoModel.ListQuickPayDetail[5].ItemName": "補差價",
            "InfoModel.ListQuickPayDetail[5].SubTotal": "100",
            "InfoModel.ListQuickPayDetail[5].BuyQty": "0",
            "hidCargoCnt": "0",
            "InfoModel.QuickPay.ShipComapnyCode": "",
            "InfoModel.QuickPay.ShipFee": "0",
            "InfoModel.QuickPay.TradeAMT": "0",
            "InfoModel.QuickPay.TradeSubAMT": "0",
            'CellPhone': '0912345678',
            'Email': '2svpn@gmail.com',
            'ShippingCellPhone': '0912345678',
            'ShippingEmail': '2svpn@gmail.com',
            'Remark': '感謝你的購買，會盡速開通你的權益',
            }

class Customer( Subscription ):

    autoBillingData = {
    'CName': '自動繳費單測試',
    'ShippingCName': '自動繳費單測試',
    'CellPhone': '0912345678',
    'Email': 'jkuo22@gmail.com',
    'ShippingCellPhone': '0912345678',
    'ShippingEmail': 'jkuo22@gmail.com',
    }
    orderQtyMap = {
    "base": "InfoModel.ListQuickPayDetail[0].BuyQty",
    "adv": "InfoModel.ListQuickPayDetail[1].BuyQty",
    "amount": "InfoModel.QuickPay.TradeAMT",
    "subamount": "InfoModel.QuickPay.TradeSubAMT",
    }

    telegram_id = 1649016499
    instances = []

    def __init__(self, name, orderName, **kwargs ):
        assert not RE.search( orderName ), f"digit in orderName not allowed."
        super().__init__( **kwargs )
        self.name = name
        self.__class__.instances.append(self)
        self.order.update( {'CName': orderName, 'ShippingCName': orderName} )
        self.dataUpdate()

    def dataUpdate( self ):
        if self.base > 0:
            self.order.update( {self.orderQtyMap['base'] : str(self.base)} )
        if self.adv > 0:
            self.order.update( {self.orderQtyMap['adv'] : str(self.adv)} )

        amount = ( int(self.order["InfoModel.ListQuickPayDetail[0].SubTotal"]) *
                   self.base +
                   int(self.order["InfoModel.ListQuickPayDetail[1].SubTotal"]) *
                   self.adv )

        self.order.update( {self.orderQtyMap['amount'] : str(amount)} )
        self.order.update( {self.orderQtyMap['subamount'] : str(amount)} )
