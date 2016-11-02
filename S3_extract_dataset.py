"""
This extracts all the dct available in structured format from the raw
dct of the athletes
"""

from datetime import datetime, timedelta
import re
import numpy as np
from scipy.optimize import minimize
from pymongo import MongoClient
import database
from datawrapper import correl_wrapper


db_inserts, db_extended = database.init()


# functions to get daily values
def Day(day, values, usr):
    result = {'Day of week':day.weekday()}
    return result


def RestingHR(day, values, usr):
    
    result = {'Morning HR':None, 'Evening HR':None}
    
    hrM = [val.val0 for val in values if val.type == 21 and val.time_stamp.hour < 11 ]
    
    if len(hrM) > 0:
        result['Morning HR'] = np.min(hrM)*1.0

    hrE = [val.val0 for val in values if val.type == 21 and val.time_stamp.hour > 20 ]
    
    if len(hrE) > 0:
        result['Evening HR'] = np.min(hrE)*1.0
    
    return result

def FittedCurve(day, values, usr):
    
    result = {'A':None, 'T':None, 'C':None, 'Load':None}
    
    # filter the values for 1024
    if usr == '1024' and day < datetime.strptime("2016-02-04", "%Y-%m-%d"):
        return result
    else:
        hr = [val for val in values if val.type == 21 ]

    if len(hr) < 2:
        return result

    # find max idx
    mx, _ = max(enumerate(hr), key = lambda p: p[1].val0)
    
    if hr[mx].val0 < 110:
        return result;
    
    cd = [hr[mx]]
    mx = mx + 1;
    
    while ( (hr[mx].time_stamp - hr[mx-1].time_stamp) < timedelta(minutes = 500) ):
        cd.append(hr[mx])
        mx += 1
        if mx >= len(hr):
            break;
    
    if len(hr) < 5:
        return result
    
    # convert to x, y
    x = []
    y = []
    
    start = cd[0].time_stamp
    
    for h in cd:
        diff = (h.time_stamp - start).seconds
        x.append(diff)
        y.append(h.val0)

    x = np.array(x)*1.0
    y = np.array(y)

    start_hr = 180.0

    def fnc(x, p):
        return (start_hr - p[2]) * np.exp( -(x - p[0]) / p[1] ) + p[2]
        
    def obj(p):
        return np.mean( ( fnc(x,p)  - y )**2 )
    
    p0 = np.array([0.0, 100.0, 50.0])
    sol = minimize(obj, p0)
    p = sol.x


    sc = p[1]*p[2]
    if sc > 25000 or sc < 0.0:
        return result;
    
    result['T'] = p[0]
    result['A'] = p[1]
    result['C'] = p[2]
    result['Load'] = sc
    return result

def Activity(day, values, usr):
    result = {'Activity A':None, 'Activity G':None}
    
    gyro = [[val.val0, val.val1, val.val2] for val in values if val.type == 4 ]
    
    if len(gyro) > 0:
        df = np.abs(np.diff(gyro, axis = 0))
        result['Activity G'] = np.mean( np.mean(df, axis = 0) )

    accel = [[val.val0, val.val1, val.val2] for val in values if val.type == 1 ]
    
    if len(accel) > 0:     
        df = np.abs(np.diff(accel, axis = 0))
        result['Activity A'] = np.mean( np.mean(df, axis = 0) )
        
    return result

def Feedback(day, values, usr):
    result = {'RPE':None, 'DALDA':None}
    
    data = [val for val in values if val.type == 1024 ]
    
    if len(data) > 0:
        
        dalda = []
        
        for val in data:
            if 'RPE' in val.tag:
                if val.val0 > 0:
                    result['RPE'] = val.val0
            else:
                dalda.append(val.val0)
        
        if len(dalda) > 0:
            result['DALDA'] = np.mean(dalda)
        
    return result

def Sleep(day, values, usr):
    result = {'Sleep length': None, 'Sleep start': None, 'Sleep end': None, 'Deep sleep': None}
    
    vals = [val for val in values if val.type == 777 ]
    
    if len(vals) > 0:   
        val = vals[-1] 
        if val.val0 < 2.0 or val.val0 > 12.0:
            return result
        result['Sleep length'] = val.val0
        result['Sleep start'] = (val.val1).hour
        
        if result['Sleep start'] > 12:
            result['Sleep start'] = result['Sleep start']-24
        
        result['Sleep end'] = val.time_stamp.hour
        result['Deep sleep'] = val.val2 if val.val2 > 0 else None
    
    return result


def run(user=None):
    '''
    run the S3-script
    Args:
        user: If user is None, als users in db will be taken
    Returns:

    '''
    ### choose here the features to be extracted

    ff = [Day, RestingHR, FittedCurve, Activity, Sleep, Feedback]

    ###
    #client = MongoClient('localhost', 27017)
    #db = client['triathlon']
    dct = {}
    #collections = db.collection_names()
    #find users to compute
    if user:
        dct[user] = []
    else:
        for user_elem in db_extended.get_all_users():
            dct[user_elem['email']] = []
    #delete users _data-collections
    for user_elem in dct:
        db_extended.drop_correl(user_elem)
    #find all measuremtens and sort list by date
    for user_elem in dct:
        lst = []
        for elem in db_extended.find_data_user(user_elem):
            if isinstance(elem.time_stamp, datetime):
                lst.append(elem)
        dct[user_elem] = sorted(lst, key=lambda date: date.time_stamp)



    #with open("sorted.bin", "r+b") as u:
    #    dct = pc.load(u)

    feat = {key: [] for key in dct}

    oneday = timedelta(days = 1)

    for usr in dct:

        daystart = datetime.today().replace(hour = 3, minute = 00)
        dayend = daystart + oneday

        data = dct[usr]

        all_feat = []

        for i in range(300):

            daystart = daystart - oneday
            dayend = dayend - oneday

            # get data in the range
            values = [val for val in data if daystart <= val.time_stamp and val.time_stamp <= dayend ]

            if len(values) < 1:
                continue

            # extract features from the data

            r = {'time_stamp':daystart}
            for fnc in ff :
                r.update(fnc(daystart, values, usr))

            # save them for the user
            all_feat.append(correl_wrapper.correl_wrapper_gen(r))

        #new save
        collection_name = ('%s_data' % (usr))
        if all_feat:
            for data in all_feat:
                db_inserts.insert_correl(usr, data)
                #db[collection_name].insert(data)
        else:
            pass

        # save the data
    #    pc.dump(all_feat, open('/home/matthias/data/' +usr + '/' + usr + '.data','w+b'))


if __name__ == '__main__':
    run()