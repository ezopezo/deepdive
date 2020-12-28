from contextlib import contextmanager
import csv

 
def coroutine(coro):                    # priming
    def inner(*args, **kwargs):
        gen = coro(*args, **kwargs)
        next(gen)
        return gen
    return inner


def data_parser():
    with open('cars.csv', 'r') as f:
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


def process_data(output, *conditions):               # controller
    data = data_parser()                # data source
    
    output = save_data(output)          # save data to file
    
    filter_ = output
    for condition in conditions:
        filter_ = filter_data(lambda row, v=condition: v in row[0], filter_) # help form solution: condition as lambda argument to aviod closure

    for d in data:              # pulling data - could be done in separate
        filter_.send(d)         # pushing through filters to destination file


process_data('output.csv', 'Chevrolet', 'Landau', 'Carlo')


def

with open('output.csv', 'r') as f: # control of data
    for row in f:
        print(row)