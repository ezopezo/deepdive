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
        if contains in data_row[0].lower(): # lambda
            target.send(data_row)       # target == output == save_data

            

def process_data(output):               # controller
    data = data_parser()                # data source
    
    output = save_data(output)          # save data to file
    
    filter_third = filter_data('carlo', output)
    filter_second = filter_data('landau', filter_third)
    filter_first = filter_data('chevrolet', filter_second)

    for d in data:
        filter_first.send(d)


process_data('output.csv')

