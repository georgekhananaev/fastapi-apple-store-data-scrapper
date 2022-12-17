from datetime import datetime, timedelta
import json
import os

# time now
now = datetime.now()


# temporary memory for top100 items, once built can be used several times without sending new requests.
top_hundred_free_memory = {}
top_hundred_paid_memory = {}
top_hundred_detailed_free_memory = {}
top_hundred_detailed_paid_memory = {}


# if key LastUpdate is larger than 1 day return true
def check_date_in_dictionary(dct) -> bool:
    try:
        if datetime.now() - dct['LastUpdate'] > timedelta(days=1):
            return True
        else:
            return False
    except Exception as Err:
        print(Err)
        return True


# check if file is older than 30 days (for caching system)
def check_if_expired(file, days=30) -> bool:
    today = datetime.today()
    modified_date = datetime.fromtimestamp(os.path.getmtime(file))
    duration = today - modified_date
    return duration.days > days


# finding if specific words located in dictionaries.
def find_if_value_exist(input_value, input_multi_dict) -> bool:
    try:
        for key, value in input_multi_dict.items():
            if input_value in value.lower():
                return True
            else:
                return False
    except Exception as Er:
        print(Er)
        return False


# converting list into dictionary with lambda
def Convert(lst) -> dict:
    res_dct = map(lambda i: (lst[i], lst[i + 1]), range(len(lst) - 1)[::2])
    return dict(res_dct)


