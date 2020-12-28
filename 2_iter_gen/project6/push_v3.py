from contextlib import contextmanager
import csv

 
def coroutine(coro):                    # priming
    def inner(*args, **kwargs):
        gen = coro(*args, **kwargs)
        next(gen)
        return gen
    return inner


def data_parser(file):
    with open(file, 'r') as f:
        dialect = csv.Sniffer().sniff(f.read(2000))
        f.seek(0)
        next(f)                         # skip header row
        yield from csv.reader(f, dialect=dialect)


@coroutine                              # write data to file
def save_data(f_name):
    with open(f_name, 'w', newline='') as f:
        writer = csv.writer(f)
        while True:
            data_row = yield
            writer.writerow(data_row)


@coroutine                              # filter data
def filter_data(contains, target):
    while True:
        data_row = yield
        if contains(data_row): 
            target.send(data_row)       # target == output == save_data

@coroutine
def process_data(output, conditions):               # controller
    
    output = save_data(output)          # save data to file
    
    filter_ = output
    for condition in conditions:
        filter_ = filter_data(lambda row, v=condition: v in row[0], filter_) # help form solution: condition as lambda argument to aviod closure

    while True:
        recieved = yield
        filter_.send(recieved)


@contextmanager
def pipeline(output, conditions):
    p = process_data(output, conditions)
    try:
        yield p
    finally:
        p.close()

with pipeline('output.csv', ('Chevrolet', 'Landau', 'Carlo')) as p:
    for row in data_parser('cars.csv'): #
        p.send(row)

with open('output.csv', 'r') as f: # control of data
    for row in f:
        print(row)