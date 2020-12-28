import csv
from datetime import datetime
from collections import namedtuple
import itertools

###goal 1 - create lazy iterators for every csv file into named tuple with correct type
def csv_parser(filename):
    with open(filename) as e:
        reader = csv.reader(e, delimiter=',', quotechar='"')
        yield from reader

### data processing
#helpers
def casting(item):
    try:
        return int(item.replace('-', ''))
    except ValueError:
        return item


def casting_date(item):
    try:
        return datetime.strptime(item, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return item

#processers
def process_employment():
    em = csv_parser('employment.csv')
    Empl = namedtuple('Employment', next(em))              # creating header - first row in csv file, passing it as arguments to named tuple
    for row_list in em:                                    # lazily iterating through file
        yield Empl(*(i for i in map(casting, row_list)))   # mapping casting() function to every item in list created prevoiously lazily from row

def process_personal_info():
    inf = csv_parser('personal_info.csv')
    PersIn = namedtuple('Personal_info', next(inf))  
    for row_list in inf:                                    
        yield PersIn(*(i for i in map(casting, row_list)))

def process_update_status():
    up = csv_parser('update_status.csv')
    UpdStat = namedtuple('Update_status', next(up))
    for row_list in up:                                    
        yield UpdStat(*(i for i in map(casting if row_list[0] else casting_date, row_list)))

def process_vehicles():
    veh = csv_parser('vehicles.csv')
    Veh = namedtuple('Vehicles', next(veh))
    for row_list in veh:                                    
        yield Veh(*(i for i in map(casting, row_list)))
#####

for i in process_update_status():
    print(i)