import csv
from datetime import datetime
from collections import namedtuple, defaultdict
import itertools


###goal 1 - create lazy iterators for every csv file into named tuple with correct type
def csv_parser(filename):
    with open(filename) as e:
        reader = csv.DictReader(e, delimiter=',', quotechar='"')
        yield from reader

### data processing
def casting(item):
    try:
        return int(item.replace('-', ''))
    except ValueError:
        return item

def casting_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return value

#####

def zipping_data():
    zipped = zip(csv_parser('employment.csv'), csv_parser('personal_info.csv'), csv_parser('update_status.csv'), csv_parser('vehicles.csv'))
    for zipped_rows in zipped: 
        yield zipped_rows

def merging_data():
    zipped = zipping_data()
    for j in zipped:
        yield {**j[0], **j[1], **j[2], **j[3]}

def casting_data():
    merged = merging_data()
    for k in merged:
        yield {key: casting_date(value) if key == 'last_updated' or key == 'created' else casting(value) \
                                                                    for key, value in k.items()}

def converting_to_named_tuple():
    Data = namedtuple('Data', next(casting_data()))
    for k in casting_data():
        if k['last_updated'] > datetime.strptime('2017/03/01 00:00:00', "%Y/%m/%d %H:%M:%S"): #filtering old records according last update
            yield Data(*k.values())


def number_car_by_gender():
    updated = converting_to_named_tuple()
    Gender = namedtuple('Make_by_gender', 'Male Female')
    male = defaultdict(int)
    female = defaultdict(int)
    for record in updated:
        if record[6] == 'Female':
            female[record[10]] += 1
        else:
            male[record[10]] += 1
    yield Gender({k: v for k, v in sorted(male.items(), key=lambda x: x[1], reverse=True)}, \
                {k: v for k, v in sorted(female.items(), key=lambda x: x[1], reverse=True)})

for j in number_car_by_gender():
    print(j)
