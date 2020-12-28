from collections import namedtuple
import re
from datetime import datetime
from collections import defaultdict

###helpers functions###
def unit(car):
    '''Replaces , between doublequotes'''
    if '"' in car:
        car = re.sub(r'"[^"]*"', lambda m: m.group(0).replace(',', ''), car)
        car = car.replace('"', '')
    return car


def cast(data_type, value, default):
    '''Cast data from file'''
    if data_type == 'summons_number':
        try:
            return int(value)
        except ValueError:
            return default

    elif data_type == 'issue_date':
        try:
            return datetime.strptime(value, '%m/%d/%Y').date()
        except ValueError:
            return default

    elif data_type == 'violation_code':
        try:
            return int(value)
        except ValueError:
            return default
    
    elif data_type == 'vehicle_make' and value == '':
        return default

    else:
        try:
            value = value.strip()
            if not value:
                return default
            else:
                return value
        except ValueError:
            return default


def cast_row(data_type, value):
    return [cast(data_type, value, default='N/A') for data_type, value in zip(data_type, value)]
#####################

###main
def parse_data(): #create header, named tuple and pass data into named tuple
    with open('nyc_parking_tickets_extract.csv') as f: #
        header = next(f).replace(' ', '_').replace('\n', '').lower().split(',') #
        Parking = namedtuple('Parking', header) #
        for car in f:
            car = car.replace('\n', '')
            car = unit(car).split(',') # unit() removing commas between doublequotes, spliting to list
            car = cast_row(header, car) #casting value
            yield Parking(*car)


def read_data():
    for row in parse_data():
        yield row


###data processing
def number_of_violations():
    number = defaultdict(int)   
    for vehicle in parse_data():
        if vehicle.vehicle_make != 'N/A':
            number[vehicle.vehicle_make] += 1
            
    return  {make: count for make, count in sorted(number.items(), key=lambda t: t[1], reverse=True)}

print(number_of_violations())


