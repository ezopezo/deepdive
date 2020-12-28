from collections import namedtuple
import re
import datetime

###helpers functions###
def unit(car):
    '''Replaces , between doublequotes'''
    if '"' in car:
        car = re.sub(r'"[^"]*"', lambda m: m.group(0).replace(',', ''), car)
        car = car.replace('"', '')
    return car


def cast(data_type, value):
    '''Cast data from file'''
    if data_type == 'Summons_Number':
        return int(value)
    elif data_type == 'Issue_Date':
        value = value.split('/')
        value = [int(value[i]) for i in [2, 0, 1]]
        x = datetime.datetime(*value)
        return x
    elif data_type == 'Violation_Code':
        return int(value)
    else:
        return value


def cast_row(data_type, value):
    return [cast(data_type, value) for data_type, value in zip(data_type, value)]
#####################

###main
def read_data(): #create header, named tuple and pass data into named tuple
    car_list = []
    with open('nyc_parking_tickets_extract.csv') as f:
        header = f.readline().replace(' ', '_').replace('\n', '').split(',')
        Parking = namedtuple('Parking', header)
        for car in f.readlines():
            car = car.replace('\n', '')
            car = unit(car).split(',') # unit() removing commas between doublequotes, spliting to list
            car = cast_row(header, car) #casting value
            car_list.append(Parking(*car))
        return car_list

print(read_data())

###data processing
def number_of_violations():
    number = dict()    
    for vehicle in read_data():
        if vehicle.vehicle_make in number and vehicle.vehicle_make != 'N/A':
            number[vehicle.vehicle_make] += 1 
        else:
            number[vehicle.vehicle_make] = 1
        
    return number

#print(number_of_violations())

