import database
import pprint
import S3_extract_dataset

db_inserts, db_extended = database.init()

printer = pprint.PrettyPrinter(indent=4)

dynamic_programming = {}
res = {}

to_delete = []

global_counter = 0

def run(username):
     tags = ['TrainingHR', 'Cooldown', 'Step Tracking']
    sorted_measures = filter_measures_by_tag(measures)
    for measures in sorted_measures:
        print('Currently analysing:', measures)
        idx_glob = 1
        clusters = []
        sorted_measures[measures] = sorted(sorted_measures[measures], key=lambda entry: entry['effectiveDateTime'])
        while len(sorted_measures[measures])>0:
            measure_one = sorted_measures[measures][0]
            dct = {str(idx_glob) + '_cluster' : [{'head' : {'amount' : len(measure_one['value_ids']), '_id' : measure_one['_id'], 'uploaded at' : measure_one['effectiveDateTime'].strftime("%d.%m.%Y_%H:%M:%S")}}]}
            del sorted_measures[measures][0]
            idx2 = 0
            while len(sorted_measures[measures]) > 0 and idx2 < len(sorted_measures[measures]):
                measure_two = sorted_measures[measures][idx2]
                if measure_one['_id']==measure_two['_id']:
                    continue
                else:
                    compare = same_measure(username, measure_one, measure_two)
                    if compare:
                        dct[str(idx_glob)+'_cluster'].append( {'subordinate': {'amount' : len(measure_two['value_ids']), '_id' : measure_two['_id'], 'uploaded at' : measure_two['effectiveDateTime'].strftime("%d.%m.%Y_%H:%M:%S")}})
                        del sorted_measures[measures][idx2]
                        to_delete.append(measure_two['_id'])
                    else:
                        idx2 += 1
            idx_glob += 1
            clusters.append(dct)
        res[measures] = clusters

def filter_measures_by_tag(measures):
    temp = {}
    for measure in measures:
        if measure['category']['coding'][0]['display'] in temp:
            temp[measure['category']['coding'][0]['display']].append(measure)
        else:
            temp[measure['category']['coding'][0]['display']] = [measure]
    return temp

def same_measure(username, measure_one, measure_two):
    measure_one_val_ids = measure_one['value_ids']
    measure_two_val_ids = measure_two['value_ids']
    if not len(measure_one_val_ids) == len(measure_two_val_ids):
        return False
    for id_one in measure_one_val_ids:
        found = False
        try:
            measure_one = dynamic_programming[id_one]
        except KeyError:
            measure_one = db_extended.db_base._db[str(username)].find_one({'_id': id_one})
            dynamic_programming[id_one] = measure_one
        for id_two in measure_two_val_ids:
            try:
                measure_two = dynamic_programming[id_two]
            except KeyError:
                measure_two = db_extended.db_base._db[str(username)].find_one({'_id':id_two})
                dynamic_programming[id_two] = measure_two
            if (same_datavalue(username, measure_one, measure_two)):
                found = True
                continue
        if not found:
            return False
    return True

def same_datavalue(username, measure_one, measure_two):
    result = measure_one['valueQuantity']['value']==measure_two['valueQuantity']['value'] \
           and measure_one['code']['coding'][0]['display']==measure_two['code']['coding'][0]['display'] \
           and measure_one['valueDateTime']==measure_two['valueDateTime']
    return result

def delete_measure (measure_id, username):
    counter = 0
    measure = db_extended.db_base._db['%s_measure' % username].find_one({'_id': measure_id})
    value_ids = measure['value_ids']
    for id in value_ids:
        db_extended.db_base._db[username].delete_one({'_id': id})
        counter += 1
    db_extended.db_base._db['%s_measure' % username].delete_one({'_id': measure_id})
    counter +=1
    # print('Deleted %s entries' % str(counter), 'of', measure['category']['coding'][0]['display'])
    return counter

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

if __name__ == '__main__':
    names = db_extended.db_base._db.collection_names()
    users = []
    for name in names:
        if validateEmail(name):
            users.append(name)
    for name in users:
        dynamic_programming.clear()
        res.clear()
        del to_delete[:]
        global_counter = 0
        print('Currently filtering:', name)
        run(name)
        # printer.pprint(res)
        for measure_id in to_delete:
            curr_cunter=delete_measure(measure_id, name)
            global_counter+=curr_cunter
        print('Successfully deleted %s entries overall' % str(global_counter))
        if global_counter>0:
            print('Start running S3 data aggregation for user', name)
            S3_extract_dataset.run(name)
            print('Finished data aggregation for user', name)