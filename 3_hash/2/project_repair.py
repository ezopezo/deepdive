
from collections import OrderedDict

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
            'city': 'Weston-super-Mare'
        }
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
        }
    }
}

def match_keys(data, template, path):
    data_keys = data.keys()
    valid_keys = template.keys()
 
    additional = data_keys - valid_keys
    missing = valid_keys - data_keys

    if missing or additional:
        extra_msg = 'extra keys: ' + ','.join({path + '.' + str(key) for key in additional}) if additional else ''
        missing_msg = 'missing keys: ' + ','.join({path + '.' + str(key) for key in missing}) if missing else ''
        return ' '.join((missing_msg, extra_msg))
    else:
        return None

def match_types(data, template, path):
    for key, val in template.items():
        if isinstance(val, dict):
            template_type = dict
        else:
            template_type = val
        data_value = data.get(key, object())
        if not isinstance(data_value, template_type):
            err_msg = 'incorrect type at: ' + path + '.' + key + '  ' + type(data_value).__name__ + ' recieved ' + template_type.__name__ + ' expected. '
            return err_msg
    return None

def recurse_validate(data, template, path):
    err_msg = match_keys(data, template, path)
    if err_msg:
        return err_msg

    err_msg = match_types(data, template, path)
    if err_msg:
        return err_msg
    
    dictionary_type_keys = {key for key, value in template.items()
                           if isinstance(value, dict)}

    for key in dictionary_type_keys:
        sub_path = path + '.' + str(key)
        sub_template = template[key]
        sub_data = data[key]
        err_msg = recurse_validate(sub_data, sub_template, sub_path) # err_msg is return below!!!
        if err_msg:
            return err_msg

    return None

err_msg = recurse_validate(michael, template, '')
print(err_msg)