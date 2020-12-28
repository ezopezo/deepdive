# project 5
from collections import namedtuple
from contextlib import contextmanager
from itertools import islice
import csv

#goal 1
class ctx_manager:
    def __init__(self, fname):
        self._fname = fname     # storage of file name
        self._f = None          # file object

    ### Iterator protocol
    def __iter__(self):
        return self

    def __next__(self):
        row = next(self._f)                                                   # eager eval!!!
        row = row.strip(self.dialect.lineterminator).split(self.dialect.delimiter)
        return self.Data(*row)
    ###

    ### Context manager protocol
    def __enter__(self):                                                      # opening file and doing additional utilities for iteration and processing data
        self._f = open(self._fname, 'r')
        sample = self._f.read(1000)
        self.dialect = csv.Sniffer().sniff(sample)                            # detecting dialect
        self._f.seek(0)
        self.header = next(self._f).strip(self.dialect.lineterminator).split(self.dialect.delimiter) # figuring out header in entring
        self.Data = namedtuple('Data', self.header)                           # preparing namedtuple
        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        if not self._f.closed:
            self._f.close()
        else:
            raise StopIteration
        return False
    ###
'''
with ctx_manager('cars.csv') as d:
    for i in d:
        print(i)
'''

#goal 1 refactor after solution
class ctx_manager_ref:
    def __init__(self, fname):
        self._fname = fname     # storage of file name
        self._f = None          # file object

    ### Iterator protocol
    def __iter__(self):
        return self

    def __next__(self):                                   
        return self.Data(*next(self._reader))
    ###

    ### Context manager protocol
    def __enter__(self):                                                      # opening file and doing additional utilities for iteration and processing data
        self._f = open(self._fname, 'r')
        sample = self._f.read(1000)
        self.dialect = csv.Sniffer().sniff(sample)                            # detecting dialect
        self._f.seek(0)
        self._reader = csv.reader(self._f, self.dialect)
        self.header = next(self._reader)                                      # figuring out header
        self.Data = namedtuple('Data', self.header)                           # preparing namedtuple
        return self

    def __exit__(self, exc_type, exc_value, exc_trace):
        if not self._f.closed:
            self._f.close()
        else:
            raise StopIteration
        return False
    ###

with ctx_manager_ref('cars.csv') as d:
    for i in islice(d, 5):
        print(i)


#goal 2
def detect_dialect(f):
    sample = f.read(1000)
    dialect = csv.Sniffer().sniff(sample)
    f.seek(0)
    return dialect

@contextmanager
def opener(fname, mode='r'):
    f = open(fname, mode)
    try:                                                       
        yield f
    finally:
        f.close()

def yielder_gen():
    with opener('personal_info.csv', 'r') as d:
        dialect = detect_dialect(d)
        Data = namedtuple('Data', next(d).strip(dialect.lineterminator).split(dialect.delimiter))
        for record in d:
            yield Data(*record.strip(dialect.lineterminator).split(dialect.delimiter))

'''
product = yielder_gen()

for i in range(10):
    print(next(product))
'''


#goal 2 - refactor after solution
def detect_dialect_ref(f):
    sample = f.read(1000)
    dialect = csv.Sniffer().sniff(sample)
    f.seek(0)
    return dialect

@contextmanager
def opener_ref(fname, mode='r'):
    f = open(fname, mode)
    try:  
        ltr = detect_dialect_ref(f).lineterminator                      # everything should be inside try block to check every operation on file passed #unused csv.reader again - good/bad?
        dlm = detect_dialect_ref(f).delimiter
        Data = namedtuple('Data', next(f).strip(ltr).split(dlm))
        yield (Data(*record.strip(ltr).split(dlm)) for record in f)                                                     
    finally:
        f.close()

'''
with opener_ref('cars.csv', 'r') as d:
    for i in islice(d, 5):
        print(i)
 '''