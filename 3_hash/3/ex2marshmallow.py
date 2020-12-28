# ex2.3 marshmallow

import json, simplejson

from marshmallow import Schema, fields, post_load
from datetime import date, datetime
from decimal import Decimal


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

    def __repr__(self):
        return f'Stock({self.symbol}, {self.date}, {self.open_}, {self.high}, {self.low}, {self.close}, {self.volume})'

    def to_dict(self):
        return dict(symbol  = self.symbol,
                    date    = self.date,
                    open_   = self.open_,
                    high    = self.high,
                    low     = self.low,
                    close   = self.close,
                    volume  = self.volume
                    )

    def __eq__(self, other):
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
        return f'Trade({self.symbol}, {self.timestamp}, {self.order}, {self.price}, {self.volume}, {self.commission})'

    def to_dict(self):
        return dict(symbol      = self.symbol,
                    timestamp   = self.timestamp,
                    order       = self.order,
                    price       = self.price,
                    commission  = self.commission,
                    volume      = self.volume
                    )

    def __eq__(self, other):
        return isinstance(other, Trade) and self.to_dict() == other.to_dict()
###

### Data
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

### Marshmallow schemas
class StockSchema(Schema):
    symbol  = fields.Str()
    date    = fields.Date()
    open_   = fields.Decimal(as_string=True)
    high    = fields.Decimal(as_string=True)
    low     = fields.Decimal(as_string=True)
    close   = fields.Decimal(as_string=True)
    volume  = fields.Int()

    @post_load
    def make_stock_object(self, data, **kwargs):
        return Stock(**data)


class TradeSchema(Schema):
    symbol      = fields.Str()
    timestamp   = fields.DateTime()
    order       = fields.Str()
    price       = fields.Decimal(as_string=True)
    commission  = fields.Decimal(as_string=True)
    volume      = fields.Int()

    @post_load
    def make_trade_object(self, data, **kwargs):
        return Trade(**data)


class ActivitySchema(Schema):
    quotes = fields.Nested(StockSchema, many=True)
    trades = fields.Nested(TradeSchema, many=True)
###


def main(activity):
    encoded = ActivitySchema().dumps(activity)
    decoded = ActivitySchema().loads(encoded)

    print(activity == decoded)


if __name__ == '__main__':
    main(activity)
