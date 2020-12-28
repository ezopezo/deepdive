from timeit import timeit
from collections import OrderedDict
'''
def create_dict(n=100):
    d = dict()
    for i in range(n):
        d[i] = i
    return d


def create_ordered_dict(n=100):
    d = OrderedDict()
    for i in range(n):
        d[i] = i
    return d

def popitem(d, last=True):
    if last:
        return d.popitem()
    else:
        first_key = next(iter(d.keys()))
        return first_key, d.pop(first_key)


#timeit('create_dict(10_000)', globals=globals(), number=1_000)
#print(timeit('create_ordered_dict(10_000)', globals=globals(), number=1_000))


#d1 = create_dict(10_000)
#d2 = create_ordered_dict(10_000)
#print(timeit('d1[9_999]', globals=globals(), number=100_000))
#print(timeit('d2[9_999]', globals=globals(), number=100_000))

#n = 1_000_000
#d1 = create_dict(n)
#print(timeit('d1.popitem()', globals = globals(), number=n))


#n = 1_000_000
#d2 = create_ordered_dict(n)
#print(timeit('d2.popitem(last=True)', globals = globals(), number=n))

#n = 100_000
#d1 = create_dict(n)
#print(timeit('popitem(d1, last=False)', globals = globals(), number=n))

#n = 100_000
#d2 = create_ordered_dict(n)
#print(timeit('d2.popitem(last=False)', globals = globals(), number=n))

###You can try the other methods (move_to_end and equality testing) yourself - if you do, please post your results in the Q&A section! Or maybe you can come up with more efficient alternatives to what we have here for pop, move, etc.


### move to end
def move_to_end(d, key, *, last=True):
    d[key] = d.pop(key)
    
    if not last:
        for key in list(d.keys())[:-1]:
            d[key] = d.pop(key)

n = 10_000
d1 = create_dict(n)
print(timeit('move_to_end(d1, 1, last=False)', globals = globals(), number=n))

d2 = create_ordered_dict(n)
print(timeit('move_to_end(d1, 1, last=False)', globals = globals(), number=n))


### equality testing
#n = 10_000
#d1 = create_dict(n)
#d2 = create_dict(n)
#print(timeit('d1 == d2', globals = globals(), number=n))

#d3 = create_ordered_dict(n)
#d4 = create_ordered_dict(n)
#print(timeit('d3 == d4', globals = globals(), number=n))
'''

# Dicts

#pop first/last item
#move key to beginning/end of dictionary
#equality (==) that takes key order into account


def create_dict(n=100):
    d = dict()
    for i in range(n):
        d[i] = i
    return d


dd = create_dict(10_000)


# my solution
def move_to_end_my(d, key, *, last=True):
    if key in d:
        for _ in range(len(d)-1):
            iterator = iter(d.keys())   
            first_key = next(iterator)

            if first_key == key:
                first_key = next(iterator)

            d[first_key] = d.pop(first_key)


def move_to_end(d, key, *, last=True):
    d[key] = d.pop(key)
    
    if not last:
        for key in list(d.keys())[:-1]:
            d[key] = d.pop(key)

#print(move_to_end_my(dd, '7', last=False))

#print(timeit('move_to_end_my(dd, 9999)', globals=globals(), number=100))

print(timeit('move_to_end(dd, 9999, last=False)', globals=globals(), number=100))
