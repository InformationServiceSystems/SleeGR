import os
from triathlon_reader import CSVTriathlonReader
from datetime import datetime, timedelta

def read_hr_data(path, date_obj):
    """
    Reads the heart rate data (channel 21) from user path for specific date.
    Returns [] if there is no hr data for some specific day. 
    
    Parameters:
        path: the user path, where the csv files are located.
        date: the day for which to read the hr data. Needs to be a
              datetime object.
    
    Returns array of tuples.
    """
    date = date_obj.strftime("%Y.%m.%d")
    xy = ReadCSVData(path, date, "21", "Cooldown", True)
    
    if len(xy) < 1:
        return []
    
    x0 = xy[0][0]
    x = [(val[0] - x0).seconds for val in xy ]
    y = [val[1] for val in xy ]
    
    return zip(x,y)

def ReadCSVData(path, date, type_idx, activity=None, after_activity=False):
    
    filename = os.path.join(path, date + "-" + type_idx + ".csv")
    
    if not os.path.exists(filename):
        return []
    
    reader = CSVTriathlonReader();
    reader.ReadSensorData(filename)
    
    
    if activity is None:
        return [val.ValX for val in reader.sensorRawData if val.SensorType == 21]
    else:
        if after_activity:
            result = [];
            after = False;
            for val in reader.sensorRawData:
                if not val.SensorType == 21:
                    continue;
            
                if val.ExtraData == activity:
                    after = True;
                
                if after:
                    result.append([val.TimeStamp, val.ValX])
            
            return result
                
        else:        
            return [val.ValX for val in reader.sensorRawData if val.SensorType == 21 and val.ExtraData == activity]

if __name__ == "__main__":
    # example usage of read_hr_data
    print (read_hr_data("Daniel", datetime.now() - timedelta(days = 10)))