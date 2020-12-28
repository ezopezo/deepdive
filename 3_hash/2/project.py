from itertools import zip_longest

template = {
    'user_id': int,
    'name': {
        'first': str,
        'last': str
    },
    'bio': {
        'dob': {
            'year': int,
            'month': int,
            'day': int
        },
        'birthplace': {
            'country': str,
            'city': str
        }
    }
}

john = {
    'user_id': 100,
    'name': {
        'first': 'John',
        'last': 'Cleese'
    },
    'bio': {
        'dob': {
            'year': 1939,
            'month': 11,
            'day': 27
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Weston-super-Mare',
            
        },
    }
}

eric = {
    'user_id': 101,
    'name': {
        'first': 'Eric',
        'last': 'Idle'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 3,
            'day': 29
        },
        'birthplace': {
            'country': 'United Kingdom'
        }
    }
}

michael = {
    'user_id': 102,
    'name': {
        'first': 'Michael',
        'last': 'Palin'
    },
    'bio': {
        'dob': {
            'year': 1943,
            'month': 'May',
            'day': 5
        },
        'birthplace': {
            'country': 'United Kingdom',
            'city': 'Sheffield'
        },
        
    }
}

# Custom exceptions
class KeyMismatch(Exception):
    __module__ = 'builtins'


class BadType(Exception):
    __module__ = 'builtins'



# Checkers
def check_base(data, template, tracker): 
    if data[0] == template[0]:
        if not isinstance(data[1], template[1]):
            raise BadType(f'bad type at {tracker + "." + template[0]}; found: {type(data[1]).__name__} needed: {template[1].__name__}')
    else:
        key = data[0] if template[0] is None else template[0]
        raise KeyMismatch(f'mismatched keys at {tracker + "." + key}; provided in data: {data[0]} required: {template[0]}')


# Validator node
def validate(data, template, tracker):
    for data, template in zip_longest(data.items(), template.items(), fillvalue=(None, None)):
        if isinstance(data[1], dict):
            tracker = tracker + '.' + data[0]
            if data[0] == template[0]:
                validate(data[1], template[1], tracker)
                tracker = 'root'
            else:  
                raise KeyMismatch(f'mismatched keys at {tracker}; provided in data: "{data[0]}" required: "{template[0]}"')   
        else:
            check_base(data, template, tracker)      
    return True, ''  

print(validate(michael, template, tracker='root'))