from scipy.optimize import minimize
from datetime import datetime, timedelta
import os
from triathlon_reader import CSVTriathlonReader,SensorDataToCSV
import numpy as np
import json
from sleegr_reader import ReadCSVData

def get_alpha(xy, b, c, offset):

    x0 = xy[0][0]
    
    x = np.array( [(val[0] - x0).seconds for val in xy ] )
    y = np.array( [val[1] for val in xy ] )
    
    
    def exp_crv(p):
        return np.exp(-(x) / p)*b + c
    
    def obj_fnc(p):
        return np.mean( (exp_crv(p) - y)**2 )
    
    pst = minimize(obj_fnc, 1000.0, bounds=[[10.0,10000.0]], tol=1e-20).x.tolist()[0]
    
    """
    print x0, b, c
    yp = exp_crv(pst)    
    plt.scatter(x,y)
    plt.scatter(x,yp,c='r')
    plt.show()
    """
    
    return pst


def GetDatesRange():
    size = 120
    today = datetime.now()
    result = []
    
    for i in range(size):
        today = today + timedelta(days=-1);
        dstr = today.strftime("%Y.%m.%d")
        result.append(dstr)
    
    return result
        
def MinMaxHR(path):
    
    # check if there is an override
    
    file_override = os.path.join(path, "user.cfg")
    
    if os.path.exists(file_override):
        # read the override
        
        dct = json.load(open(file_override))
        return dct['minHR'], dct['maxHR']
    
    min_all = []
    max_all = []
    rng = GetDatesRange()
    
    for date in rng:
        min_all.extend(ReadCSVData(path, date, "21","Resting"))
        
        max_all.extend(ReadCSVData(path, date, "21","Cooldown"))
    
    if len(max_all) == 0:
        raise BaseException( "no HR data found in " + path )
    
    max_all.sort()
    
    if len(min_all) == 0:
        minHR = np.min( max_all )
    else:
        minHR = np.mean( min_all )
        
    maxHR = np.max( max_all )

    # save to temp file for analysis
    json.dump({'minHR':minHR, 'maxHR':maxHR}, open(os.path.join(path, "user.autocfg"),'w'))
    
    return minHR, maxHR

def ConvertFingerFile(path, date):
    
    timeidx = 7-1
    readidx = 15-1
    
    fname_finger = os.path.join(path, date + "_HR.txt")
    
    content = []
    
    if not os.path.exists(fname_finger):
        return
    
    with open(fname_finger,'r') as f:
        content = f.readlines()
    
    sampling_rate = 32
    hr_sum = 0.0;
    accu = 0; # the counter of samples. needed to compute average per n seconds
    
    cooldown = []
    
    for i in range(len(content)):
        
        if i == timeidx:
            
            current_date = datetime.strptime(date,'%Y.%m.%d');
            
            try:
                val = content[i][-10:].split(":")
                hours = int(val[0])
                mints = int(val[1])
                secs = int(val[2])
                
                current_date = current_date.replace(hour = hours, minute=mints, second = secs, microsecond = 0)
            except Exception as ex:
                current_date = current_date.replace(hour = 19, minute=0, second = 0, microsecond = 0)
        
        if i >= readidx:
            #split = re.split(r'\t+', content[i])
            #hrval = split[0]
            hrval = content[i]
            try:
                val = float( hrval )
            except Exception as ex:
                continue;
            
            hr_sum = hr_sum + val;
            accu = accu + 1;
            
            if accu >= sampling_rate*3:
                avg = hr_sum / accu;
                current_date = current_date + timedelta(seconds = 3.0);
                cooldown.append([current_date, avg])
                hr_sum = 0.0;
                accu = 0; # the counter of samples. needed to compute average per n seconds
    
    # read the 21 type file
    
    fname21 = os.path.join(path, date + "-21.csv")
    
    reader = CSVTriathlonReader()
    reader.ReadSensorData(fname21)
    
    data = [rec for rec in reader.sensorRawData if not rec.ExtraData == "Cooldown"]
    
    # write the extracted heart rate data into the type 21 with cooldown tag
    
    recs = []
    
    for date, value in cooldown:
        rec = reader.SensorDataTuple(UserID = 0, SensorType = 21, TimeStamp = date, ExtraData = "Cooldown", ValX = value, ValY = 0.0, ValZ = 0.0)
        recs.append(rec)
    
    before = [rec for rec in data if rec.TimeStamp < current_date]
    after = [rec for rec in data if rec.TimeStamp > current_date]
        
    result = before + recs + after
    
    if len(result) > 0:
        SensorDataToCSV(result, fname21)
    
def _get_hr_data(path, date):
    # read cooldown fingure measurement
    
    # maybe athlete measured with scosche 
    hr_cooldown = ReadCSVData(path, date, "21", "Cooldown", True);

    return hr_cooldown



def SaveCurveParams(path, date, params):
    filename = os.path.join(path, date + "-32.csv")
    with open(filename, "w") as text_file:
        text_file.write("0,32,date,Summary," + ','.join(str(x) for x in params))

def SetCurves(path):
    """
    This recomputes the curve fit for the hr recovery data
    """
    
    rng = GetDatesRange()
    
    # preprocessing : convert all existing finger files to proper csvs
    for date in rng:
        ConvertFingerFile(path, date)
    
    # extract min / max HR
    minHR, maxHR = MinMaxHR(path);
    
    b = maxHR - minHR
    c = minHR
    
    for date in rng:
        
        raw_data = _get_hr_data(path, date)
                   
        if len(raw_data) == 0:
            continue;
                
        a = get_alpha(raw_data, b, c, 0.0)
        print(a)
        SaveCurveParams(path, date, [a,b,c])

if __name__ == "__main__":
    paths = os.listdir('.')
    for path in paths:
        
        if os.path.isfile(path):
            continue;
        
        try:
            print(path)
            SetCurves(path)
        except BaseException as ex:
            print (ex)
        