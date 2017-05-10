import database
import pprint
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import pymongo
from datetime import datetime

db_inserts, db_extended = database.init()

datatypes = ['GPS Tracking', 'Accelerometer Tracking', 'Step Tracking', 'TrainingHR', 'Sleep Tracking', 'Cooldown']

def validateEmail( email ):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def run(name):
    collection_name = name + '_measure'
    result = {}
    for type in datatypes:
        temp_count = db_extended.db_base._db[collection_name].find({'category.coding.display' : type}).count()
        result[type] = temp_count
    return result

def test(name, datetime, tag):
    result = []
    cursor = db_extended.db_base._db['%s_measure'%name].find({'category.coding.display': tag,
                                               'effectiveDateTime': {'$gte': datetime }}).sort('effectiveDateTime',pymongo.ASCENDING)
    for data in cursor:
        id = data['value_ids'][0]
        value = db_extended.db_base._db[name].find_one({'_id' : id})
        result.append(value['valueQuantity']['value'])
    return result

if __name__ == '__main__':
    names = db_extended.db_base._db.collection_names()
    response = {}
    users = []
    for name in names:
        if validateEmail(name):
            users.append(name)
    for name in users:
        global_counter = 0
        res = run(name)
        response[name] = res
    pprint.pprint(response)
    # test = test('ralfbleymehl@gmail.com', datetime.strptime('03.05.2017', '%d.%m.%Y'), 'Step Tracking')
    # for i in range(len(test)-1):
    #     if (i<len(test)) and (test[i] < test[i+1]-50):
    #         print('Missing values:',test[i],test[i+1])
    print(test)


