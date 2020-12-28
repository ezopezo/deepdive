# dict excercises
from collections import defaultdict, Counter

### ex 1 - sort dict by value
'''
composers = {'Johann': 65, 'Ludwig': 56, 'Frederic': 39, 'Wolfgang': 35}

# A
composers = {i:v for i,v in sorted(composers.items(), key=lambda p: p[1])}
print(composers)

# B
composers = dict(sorted(composers.items(), key=lambda p: p[1]))
print(composers)
'''

### ex 2 - find common keys in both dictionaires and produce third with tuples contains both values
'''
d1 = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
d2 = {'b': 20, 'c': 30, 'y': 40, 'z': 50}

def intersect_dict(d1, d2):
    inter_keys = set(d1.keys()) & set(d2.keys())
    inter = {key: (d1[key], d2[key]) for key in inter_keys} 
    return inter


print(intersect_dict(d1, d2))
'''

'''
### ex 3 - join multiple dicts and sum values of common keys

d1 = {'python': 10, 'java': 3, 'c#': 8, 'javascript': 15}
d2 = {'java': 10, 'c++': 10, 'c#': 4, 'go': 9, 'python': 6}
d3 = {'erlang': 5, 'haskell': 2, 'python': 1, 'pascal': 1}

# A
def join_dicts(*dx):
    all_keys = set()
    for i in range(len(dx)):                # obtaining all keys
        all_keys = all_keys|dx[i].keys()
    
    final = defaultdict(int)
    for key in all_keys:                    # iterating keys 
        for dict_ in dx:                    # iterating every dict_ in tuple
            if key not in dict_:            # probing if key exist in dict 
                pass
            else:
                final[key] += dict_[key]    # adding value to deflautdict
    
    return dict(sorted(final.items(), reverse=True, key=lambda p: p[1])) # sortring and returning

#print(join_dicts(d1, d2, d3))

# B
def join_dicts_count(*dx):
    add_c = Counter()
    for dict_ in dx:
        add_c += Counter(dict_)
    return add_c

#print(join_dicts_count(d1, d2))

# C lector way

def merge(*dx):
    unsorted = {}
    for d in dx:
        for k, v in d.items():
            unsorted[k] = unsorted.get(k, 0) + v # if not key presented yet create it and set it to 0
    return dict(sorted(unsorted.items(), reverse=True, key=lambda p: p[1]))

#print(merge(d1, d2, d3))
'''

n1 = {'employees': 100, 'employee': 5000, 'users': 10, 'user': 100}
n2 = {'employees': 250, 'users': 23, 'user': 230}
n3 = {'employees': 150, 'users': 4, 'login': 1000}


def imbalanced_load_diag(n1, n2, n3):
    inter = set(n1.keys()) & set(n2.keys()) & set(n3.keys())
    all_keys = set(n1.keys()) | set(n2.keys()) | set(n3.keys())
    imbalanced = all_keys - inter
    
    diagnose = {}
    for key in imbalanced:
        diagnose[key] = diagnose.get(key, (n1.get(key, 0), n2.get(key, 0), n3.get(key, 0)))

    return diagnose 


print(imbalanced_load_diag(n1, n2, n3))