
# my solution 
class Counter:
    def __init__(self, counter):
        self.counter = counter.items()

    def elements(self):
        for key, value in self.counter:
            for _ in range(value): 
                yield key

   

inst = Counter({1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10})

for i in inst.elements():
    print(i)



# Fred's solution
class CounterInstructor:
    def __init__(self, **kwargs):
        self.d = kwargs                 # kw arguments are dict

    def __setitem__(self, key, value):  # setting value on particular key
        self.d[key] = value

    def __getitem__(self, key):         # getting item from key, if key not presented settong key and default value
        self.d[key] = self.d.get(key, 0)
        return self.d[key]
    
    def elements(self):
        for key, frequency in self.d.items():
            for _ in range(frequency): 
                yield key


ci = CounterInstructor(a=3, b=4, c=6)