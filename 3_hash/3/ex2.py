import json
import sys

from datetime import date, datetime
from decimal import Decimal
from functools import singledispatch

### Classes
class Stock:
    def __init__(self, symbol, date, open_, high, low, close, volume):
        self.symbol = symbol
        self.date = date
        self.open_ = open_
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    def __repr__(self):         #added for better representation in CLI
        return f'Stock({self.symbol}, {self.date}, {self.open_}, {self.high}, {self.low}, {self.close}, {self.volume})'
    
    def to_dict(self):          #created for better comparison 
        return dict(symbol  = self.symbol,
                    date    = self.date,
                    open_   = self.open_,
                    high    = self.high,
                    low     = self.low,
                    close   = self.close,
                    volume  = self.volume
                    )

    def __eq__(self, other):    #comparison of primary data with encoded/decoded data
        return isinstance(other, Stock) and self.to_dict() == other.to_dict()


class Trade:
    def __init__(self, symbol, timestamp, order, price, volume, commission):
        self.symbol = symbol
        self.timestamp = timestamp
        self.order = order
        self.price = price
        self.volume = volume
        self.commission = commission

    def __repr__(self):
        return f'Trade({self.symbol}, {self.timestamp}, {self.order}, {self.price}, {self.commission}, {self.volume})'

    def to_dict(self):
        return dict(symbol      = self.symbol,
                    timestamp   = self.timestamp,
                    order       = self.order,
                    price       = self.price,
                    volume      = self.volume,
                    commission  = self.commission)

    def __eq__(self, other):
        return isinstance(other, Trade) and self.to_dict() == other.to_dict()
###


### Data instance
activity = {
    "quotes": [
        Stock('TSLA', date(2018, 11, 22), 
              Decimal('338.19'), Decimal('338.64'), Decimal('337.60'), Decimal('338.19'), 365_607),
        Stock('AAPL', date(2018, 11, 22), 
              Decimal('176.66'), Decimal('177.25'), Decimal('176.64'), Decimal('176.78'), 3_699_184),
        Stock('MSFT', date(2018, 11, 22), 
              Decimal('103.25'), Decimal('103.48'), Decimal('103.07'), Decimal('103.11'), 4_493_689)
    ],
    
    "trades": [
        Trade('TSLA', datetime(2018, 11, 22, 10, 5, 12), 'buy', Decimal('338.25'), 100, Decimal('9.99')),
        Trade('AAPL', datetime(2018, 11, 22, 10, 30, 5), 'sell', Decimal('177.01'), 20, Decimal('9.99'))
    ]
}
###

###Schema of data for better orientation
schema = '''
    "key:" [
            Object(string, date, decimal, integer), 
            Object(string, date, decimal, integer), 
            Object(string, date, decimal, integer)
            ]
    "key:" [
            Object(string, date, decimal, integer), 
            Object(string, date, decimal, integer)
            ]
'''
###

### ENCODING DATA #####################################################
### First approach
class CustomJSONEncoder(json.JSONEncoder):      
    def default(self, arg):                     # overloading default function for creating custom decoding schema
        if isinstance(arg, datetime):
            return {
                    "objecttype": "datetime", 
                    "value": arg.isoformat()
                    }
        elif isinstance(arg, date):
            return {
                    "objecttype": "date", 
                    "value": [int(i) for i in str(arg).split('-')] # list of Y/m/d int-s for later decoding
                    }
        elif isinstance(arg, Decimal):
            return {
                    "objecttype": "Decimal", 
                    "value": str(arg)
                    }
        else: 
            try:
                return {                                   # general way for encoding objects
                    "objecttype": type(arg).__name__,      # setting object name as key
                    "attributes": vars(arg)                # setting attributes as value
                    }
            except TypeError:
                return str(arg)
###


### Second approach
@singledispatch                                  # using registering encoding functions with singledispatch # second way
def custom_JSON_encoder_singledisp(arg):
    try:
        return {
                "objecttype": type(arg).__name__,
                "attributes": vars(arg)      
                }
    except TypeError:
        return str(arg)

@custom_JSON_encoder_singledisp.register(datetime)
def _(arg):
    return {
            "objecttype": "datetime", 
            "value": arg.isoformat()
            }

@custom_JSON_encoder_singledisp.register(date)
def _(arg):
    return {
            "objecttype": "date", 
            "value": [int(i) for i in str(arg).split('-')]
            }

@custom_JSON_encoder_singledisp.register(Decimal)
def _(arg):
    return {
            "objecttype": "Decimal", 
            "value": str(arg)
            }
###


### DECODING DATA #####################################################
### First approach: hook for decoding custom JSON data structure
def custom_JSON_decoder(arg):                      
    if 'objecttype' in arg:
        if arg['objecttype'] == 'datetime':
            return datetime.strptime(arg['value'], '%Y-%m-%dT%H:%M:%S')

        elif arg['objecttype'] == 'date':
            return date(*arg['value'])

        elif arg['objecttype'] == 'Decimal':
            return Decimal(arg['value'])

        elif arg['objecttype'] == 'Trade':
            attributes = [value for value in arg['attributes'].values()] # iterating over values of attributes dictionary into list comprehension
            return Trade(*attributes)                                    # unpacking list of attributes into class constructor

        elif arg['objecttype'] == 'Stock':
            attributes = [value for value in arg['attributes'].values()]
            return Stock(*attributes)

        else:                                       # if objecttype is anything else, return argument
            return arg
    else:                                           # if objecttype not presented
        return arg
###


### Second approach: class with overloaded default method for encoding
class CustomJSONDecoderCLS(json.JSONDecoder):          
    def decode(self, obj):
        data = json.loads(obj)
        return self.decode_recusive(data)


    def parse_obj(self, arg):
        if arg['objecttype'] == 'Trade':
            attributes = [self.decode_recusive(value) for value in arg['attributes'].values()]
            return Trade(*attributes)                                    

        elif arg['objecttype'] == 'Stock':
            attributes = [self.decode_recusive(value) for value in arg['attributes'].values()]
            return Stock(*attributes)


    def parse_attr(self, arg):
        if arg['objecttype'] == 'datetime':
            return datetime.strptime(arg['value'], '%Y-%m-%dT%H:%M:%S')

        elif arg['objecttype'] == 'date':
            return date(*arg['value'])

        elif arg['objecttype'] == 'Decimal':
            return Decimal(arg['value'])

        else:
            return arg

    
    def decode_recusive(self, arg):
        if isinstance(arg, dict):

            if 'objecttype' in arg and 'attributes' in arg: # custom objects
                arg = self.parse_obj(arg)

            elif 'objecttype' in arg and 'value' in arg:    # other objects
                arg = self.parse_attr(arg)

            else:
                for key, value in arg.items():
                    arg[key] = self.decode_recusive(value)

        elif isinstance(arg, list):
            for index, value in enumerate(arg):
                arg[index] = self.decode_recusive(value)

        return arg
###

def main(activity):
    encoder = sys.argv[1]
    decoder = sys.argv[2]

    if encoder == 'enclass':          # encoding using custom JSON Encoder class
        encoded = json.dumps(activity, cls=CustomJSONEncoder)
    elif encoder == 'dispatch':       # encoding using single dispatch for registering functions processing different data types
        encoded = json.dumps(activity, default=custom_JSON_encoder_singledisp)

    if decoder == 'declass':          # decoding using custom JSON decoder class
        decoded = json.loads(encoded, cls=CustomJSONDecoderCLS)
    elif decoder == 'function':       # decoding using plain function as object_hook
        decoded = json.loads(encoded, object_hook=custom_JSON_decoder)


    print(activity == decoded)        # checking equality for source and decoded/encoded data comparison 


if __name__ == '__main__':
    main(activity)