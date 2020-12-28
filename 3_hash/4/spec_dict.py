### ex 1 copied from first set of excercises
### - find common keys in both dictionaires and produce third with tuples contains both values
from collections import defaultdict, Counter, ChainMap
from random import seed, choices
from pprint import pprint
from itertools import zip_longest

import json
import sys

d1 = {'python': 10, 'java': 3, 'c#': 8, 'javascript': 15}
d2 = {'java': 10, 'c++': 10, 'c#': 4, 'go': 9, 'python': 6}
d3 = {'erlang': 5, 'haskell': 2, 'python': 1, 'pascal': 1}

# A
def join_dicts_default(*dx):
    all_keys = {key for dict_ in dx for key in dict_} # iterating in tuple of dicts and creating set comprehension of keys of every dict

    report = defaultdict(int)
    for key in all_keys:                    # iterating keys 
        for dict_ in dx:                    # iterating every dict_ in tuple
            if key in dict_:                # probing if key exist in dict 
                report[key] += dict_[key]   # adding value to defaultdict
    
    return dict(sorted(report.items(), reverse=True, key=lambda p: p[1])) # sorting and returning

#print(join_dicts_default(d1, d2, d3))

# B
def join_dicts_counter(*dx):
    report = Counter()
    for dict_ in dx:
        report += Counter(dict_)
    return report

#print(join_dicts_counter(d1, d2, d3))


### ex 2 return dictionary of count of eye colors of people. If eye color form collection not occured, return zero value in dict.
eye_colors = ("amber", "blue", "brown", "gray", "green", "hazel", "red", "violet")

class Person:
    def __init__(self, eye_color):
        self.eye_color = eye_color

seed(0)
persons = [Person(color) for color in choices(eye_colors[2:], k = 50)]

def eye_color_count(persons, eye_colors):
    report = defaultdict(int)
    for person in persons:              # iterating gover collection of Person objects
        report[person.eye_color] += 1   # counting persons with particular eye color
    
    for color in eye_colors:            # iterating gover collection of eye colors
        if color not in report:         # if not found in created defaultdict, added as zero value 
            report[color] = 0

    return dict(sorted(report.items(), reverse=True, key=lambda p: p[1])) # sorting and returning

#print(eye_color_count(persons, eye_colors))


### ex3 function that has a single argument (the environment name) and returns the "combined" dictionary 
# that merges the two dictionaries together, with the environment specific settings overriding any common settings already defined

def load_config_files():
    config_file = sys.argv[1]
    
    # basic settings
    with open('common.json', 'r') as f:
        common = json.load(f)

    # choosen settings with validation
    with open(f'{config_file}.json', 'r') as f:
        environment = json.load(f)

    return environment, common


def configuration(environment, common, chain=ChainMap()):
    for env, com in zip_longest(environment.items(), common.items(), fillvalue=(0, {})):
        if isinstance(env[1], dict) and isinstance(com[1], dict):
            if env[0]: # if key not from fillvalue (not False)
                chain[env[0]] = configuration(env[1], com[1], ChainMap(env[1], com[1])) # if key in environment use it and associate it with returning value - chain which is actually ChainMap(env[1], com[1])
            else:
                chain[com[0]] = configuration(env[1], com[1], ChainMap(env[1], com[1])) # else key is only in common settings use it and again associate with returning value in this case env or com would be empty dict (chain map we use just for reading config settings it should be ok if empry dict child)

    return chain

def main():
    environment, common = load_config_files()
    return configuration(environment, common)

if __name__ == '__main__':
    print(main())