'''
Created on Nov 9, 2015

@author: Euler
'''

import csv
import collections
from datetime import timedelta,datetime
from matplotlib import pyplot as plt
from math import sqrt

def SensorDataToCSV(records, fname):
    with open(fname, 'w') as csvfile:
            lines = []
            for rec in records:
                date = datetime.strftime(rec.TimeStamp,'%Y.%m.%d_%H:%M:%S');
                line = [str(rec.UserID) , str(rec.SensorType), date, str(rec.ExtraData), str(rec.ValX), str(rec.ValY), str(rec.ValZ)];
                lines.append( ','.join(line) )
            csvfile.write('\n'.join(lines))

class CSVTriathlonReader:
    """
    A class to handle processing of the raw data
    """
    
    def __init__(self):
        self.SensorDataTuple = collections.namedtuple("ISSDataRecord", 'UserID, SensorType, TimeStamp, ExtraData, ValX, ValY, ValZ');
        self.SleepDataTuple = collections.namedtuple("ISSSleepTuple", 'TimeStamp, DeepSleep, Length');
        
    
    #Allows to read raw data into internal representation
    def ReadSensorData(self, filename):
        with open(filename, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            SensorData = self.SensorDataTuple;
            self.sensorRawData = [];
            for row in filereader:
                # avoid weirdness at the end of the file
                if  len(row) < 1:
                    continue;
                date = datetime.strptime(row[2],'%Y.%m.%d_%H:%M:%S');
                item = SensorData(UserID = int(row[0]), SensorType = int(row[1]), TimeStamp = date, ExtraData = row[3], ValX = float(row[4]), ValY = float(row[5]), ValZ = float(row[6]));
                self.sensorRawData.append(item)
            
            self.sensorRawData.sort(key = lambda x: x.TimeStamp)

    

    #Allows to read raw data into internal representation
    def ReadSleepData(self, filename):
        with open(filename, 'rb') as csvfile:
            filereader = csv.reader(csvfile, delimiter=',')
            SleepData = self.SleepDataTuple;
            self.sleepRawData = [];
            for row in filereader:
                # avoid weirdness at the end of the file
                if  len(row) < 1:
                    continue;
                
                if  row[0] == 'Id':
                    continue;
                
                dstring = row[3];
                
                date = datetime.strptime(dstring,'%d. %m. %Y %H:%M');
                item = SleepData(TimeStamp = date, DeepSleep = float(row[12]), Length = float(row[5]));
                self.sleepRawData.append(item)

    # helper function for range of days
    def daterange(self, start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

    # this is useful to construct the dataset
    def normalizeSensorMeasurement(self, record):
        ValX = record.ValX;
        ValY = record.ValY;
        ValZ = record.ValZ;
        
        if record.SensorType == 21:
            ValX /= 200;
        if record.SensorType == 1:
            ValX /= 20;
            ValY /= 20;
            ValZ /= 20;
        if record.SensorType == 4:
            ValX /= 10;
            ValY /= 10;
            ValZ /= 10;
            
        return ValX, ValY, ValZ

    # Returns the features that describe a sertain day
    def GetDailySleepDescriptors(self, datapath, user, start_date, end_date, impute_missing = True):
        """
        Gets the sleep data for the user for the time period start_date to end_date
        Returns array with descriptors for sleep quality for days starting from
        start day and including the night of the end date
        """
        # read all data
        self.ReadSleepData(datapath + "User_" + str(user) + "_sleep-export.csv")
        # read, impute and clean the target values
        # select only records longer than 2 h, less than 16h
        targets = [ item for item in self.sleepRawData if item.Length > 2 and item.Length < 16 and item.TimeStamp >= start_date and item.TimeStamp <= end_date ];
        # compute average deep sleep percentage for imputation
        deep_sleep_avg = reduce(lambda x,y: x + y, [item.DeepSleep for item in targets])
        deep_sleep_avg /= len(targets)
        sleep_length_avg = reduce(lambda x,y: x + y, [item.Length for item in targets])
        sleep_length_avg /= len(targets)
        # create time series
        
        deep_sleep_avg = deep_sleep_avg;
        sleep_length_avg = sleep_length_avg;
        
        # date in the morning is considered. To assign target value 
        # properly, sleep data date needs to be moved 1 day back
        delta = timedelta(days=-1);
        
        # this structure holds target values, real or imputed
        deepSleepDict = {}
        
        for day in self.daterange(start_date, end_date):
            deepSleepDict[(day-delta).strftime('%Y.%m.%d')] = [deep_sleep_avg* impute_missing, sleep_length_avg* impute_missing]
        
        # get all feasible real measurements of target value
        for item in targets:
            deepSleepDict[(item.TimeStamp-delta).strftime('%Y.%m.%d')] = [item.DeepSleep if item.DeepSleep > 0 else deep_sleep_avg, item.Length]
        
        return deepSleepDict, deep_sleep_avg, sleep_length_avg

    # useful for debugging
    def PlotValues(self,data,sensorType):
        
        data = [item for item in data if item.SensorType == sensorType]
        
        x = [ item.TimeStamp for item in data ]
        y = [ item.ValX for item in data ]
        
        fig = plt.figure()
        
        graph = fig.add_subplot(111)
        
        # Plot the data as a red line with round markers
        graph.plot(x,y,'r-o')
        
        plt.show()

    def GetDailyIdleHRValues(self, datapath, user, start_date, end_date, impute_missing=True):
        """
        Gets the idle heart rate values in the morning and in the afternoon
        """
        
        filename = datapath + "User_" + str(user) + "_triathlon.csv"
        
        # read all data
        self.ReadSensorData(filename)
        # read, impute and clean the target values
        # select only records longer than 2 h, less than 16h
        targets = [ item for item in self.sensorRawData if item.SensorType == 21 ];
        # compute the values in the morning and in the afternoon
        
        morningValues = {};
        eveningValues = {};
        hrthr = 100.0;
        over_threshold = {};
        
        morningStart = start_date.replace(hour = 4)
        eveningStart = start_date.replace(hour = 20)
        
        length = 0;
        
        for day in self.daterange(start_date, end_date):
            # count the amount of time athlete spent with hr above threshold
            
            over_threshold[day.strftime('%Y.%m.%d')] = 0.0;
            values = [ item for item in targets if item.TimeStamp > morningStart and item.TimeStamp < (morningStart + timedelta(hours=24))]
            
            if len(values) > 1:
                over_threshold[day.strftime('%Y.%m.%d')] = len([item.ValX for item in values if item.ValX > hrthr]);
            
            # get all values that can contain the morning measurements
            values = [ item for item in targets if item.TimeStamp > morningStart and item.TimeStamp < (morningStart + timedelta(hours=8))]
            if len(values) > 1:
                #earliestMeasurement = values[0].TimeStamp;
                #self.PlotValues(values, 21)
                #values = [ item for item in values if item.TimeStamp >= earliestMeasurement and item.TimeStamp < earliestMeasurement + timedelta(minutes = 3)]
                #self.PlotValues(values, 21)
                #values = values[-len(values)/2:];
                #self.PlotValues(values, 21)
                selectedMorning = reduce(lambda x, y: min(x,y), [item.ValX for item in values]);
                morningValues[day.strftime('%Y.%m.%d')] = selectedMorning;
                #morningValues[day.strftime('%Y.%m.%d')] = selectedMorning / len(values);
            
            values = [ item for item in targets if item.TimeStamp > eveningStart and item.TimeStamp < eveningStart + timedelta(hours=8)]
            if len(values) > 1:
                #latestMeasurement = values[-1].TimeStamp;
                #values = [ item for item in values if item.TimeStamp > latestMeasurement - timedelta(minutes = 3) and item.TimeStamp <= latestMeasurement]
                #values = values[-len(values)/2:];
                selectedEvening = reduce(lambda x, y: min(x,y), [item.ValX for item in values]);
                eveningValues[day.strftime('%Y.%m.%d')] = selectedEvening;
                #eveningValues[day.strftime('%Y.%m.%d')] = selectedEvening / len(values);
            
            morningStart += timedelta(days=1)
            eveningStart += timedelta(days=1)
        
        # compute imputation values
        imp_morning = reduce(lambda x, y: x + y, [item[1] for item in morningValues.items()]) / len(morningValues.items())
        imp_evening = reduce(lambda x, y: x + y, [item[1] for item in eveningValues.items()]) / len(eveningValues.items())
                
        for day in self.daterange(start_date, end_date):
            if day.strftime('%Y.%m.%d') in morningValues:
                continue;
            morningValues[day.strftime('%Y.%m.%d')] = imp_morning if impute_missing else 0;
             
        for day in self.daterange(start_date, end_date):
            if day.strftime('%Y.%m.%d') in eveningValues:
                continue;
            eveningValues[day.strftime('%Y.%m.%d')] = imp_evening if impute_missing else 0;
        
        datasetValues = {};
        
        for day in self.daterange(start_date, end_date):
            datasetValues[day.strftime('%Y.%m.%d')] = [ morningValues[day.strftime('%Y.%m.%d')],
                                                        eveningValues[day.strftime('%Y.%m.%d')] ];
        
        return datasetValues, over_threshold, imp_morning, imp_evening
        
    # this returns the dataset with which it is possible to train rnn
    def GetDataset_HW_DS_4RNN(self, datapath, users):
        """
        Reads data from users, and converts it to the history data,
        suitable for rnn or lstm training
        Only (H)eart rate data and (W)atch data is used 
        Target is the (D)eep (S)leep percentage
        Target value is the last value
        """
        
        timeSeries = [] 
        
        for user in users:
            # read all data
            #self.ReadSensorData("C:\Users\Euler\Documents\data\User_" + str(user) + "_triathlon.csv")
            #self.ReadSleepData("C:\Users\Euler\Documents\data\User_" + str(user) + "_sleep-export.csv")
            # read, impute and clean the target values
            # select only records longer than 2 h
            targets = [ item for item in self.sleepRawData if item.Length > 2 and item.Length < 16 ];
            # compute average deep sleep percentage for imputation
            target_impute = reduce(lambda x,y: x + y, [item.DeepSleep for item in targets])
            target_impute /= len(targets)
            # create time series
            
            # date in the morning is considered. To assign target value 
            # properly, sleep data date needs to be moved 1 day back
            delta = timedelta(days=1);
            
            # this structure holds target values, real or imputed
            deepSleepDict = {}
            
            for day in self.daterange(targets[-1].TimeStamp, targets[0].TimeStamp):
                deepSleepDict[(day-delta).strftime('%Y.%m.%d')] = target_impute
            
            # get all feasible real measurements of target value
            for item in targets:
                deepSleepDict[(item.TimeStamp-delta).strftime('%Y.%m.%d')] = item.DeepSleep
            
            for item in self.sensorRawData:
                
                # target: deep sleep percentage the night after measurement
                key = item.TimeStamp.strftime('%Y.%m.%d');
                
                if not key in deepSleepDict:
                    continue;
                
                recTarget = deepSleepDict[key]
                
                recHour = item.TimeStamp.hour / 24.0
                
                ValX, ValY, ValZ = self.normalizeSensorMeasurement(item)
                
                record = [recHour, 
                          1*(item.SensorType == 1), 
                          1*(item.SensorType == 4), 
                          1*(item.SensorType == 21), 
                          ValX, ValY, ValZ, recTarget]
                timeSeries.append(record);
        
        return timeSeries

    # <<<<<<<<<<<<<<<<<<< Functions for chart plotting >>>>>>>>>>>>>>>>>>>>>>>> 
    
    def GetHRChart(self, datapath, userid, days):
        """
        datapath:  path to the csv files of the user
        userid: id of the user, e.g. 1024 for prof. Maass
        days: number of days from now to get data for
        """
        end_date = datetime.today();
        start_date = end_date - timedelta(days = days);
        hr_data, impute_morning, impute_evening = self.GetDailyIdleHRValues(datapath, userid, start_date, end_date, False)
                
        return hr_data, impute_morning, impute_evening
      
    def GetSleepChart(self, datapath, userid, days):
        """
        datapath:  path to the csv files of the user
        userid: id of the user, e.g. 1024 for prof. Maass
        days: number of days from now to get data for
        """
        end_date = datetime.today();
        start_date = end_date - timedelta(days = days);
        sleep_data, deep_sleep_avg, sleep_length_avg = self.GetDailySleepDescriptors(datapath, userid, start_date, end_date, False)
                
        return sleep_data, deep_sleep_avg, sleep_length_avg
    
    def GetRawHRChart(self, datapath, userid, days):
        """
        datapath:  path to the csv files of the user
        userid: id of the user, e.g. 1024 for prof. Maass
        days: number of days from now to get data for
        """
        end_date = datetime.today();
        start_date = end_date - timedelta(days = days);
        
        filename = datapath + "User_" + str(userid) + "_triathlon.csv"
        
        # read all data
        self.ReadSensorData(filename)
        # read, impute and clean the target values
        # select only records longer than 2 h, less than 16h
        targets = [ item for item in self.sensorRawData if item.SensorType == 21 and item.TimeStamp >= start_date and item.TimeStamp <= end_date];
               
        # convert to dictionary
        sleep_data = {};
        
        for item in targets:
            key = item.TimeStamp.strftime('%Y-%m-%d %H:%M:%S')
            sleep_data[key] = item.ValX
           
        return sleep_data
    
    
    def GetRawAcceloremeterChart(self, datapath, userid, days):
        """
        datapath:  path to the csv files of the user
        userid: id of the user, e.g. 1024 for prof. Maass
        days: number of days from now to get data for
        """
    
        end_date = datetime.today();
        start_date = end_date - timedelta(days=days)
        filename = datapath + "User_" + str(userid) + "_triathlon.csv"
        
        self.ReadSensorData(filename)
        
        targets = [ item for item in self.sensorRawData if item.SensorType == 1 and item.TimeStamp >= start_date and item.TimeStamp <= end_date];
        acceloremeter_data = {};
        
        
        for item in targets:
            key = item.TimeStamp.strftime('%Y-%m-%d %H:%M:%S')
           
            acceloremeter_data[key] = sqrt(item.ValX * item.ValX  + item.ValY * item.ValY + item.ValZ * item.ValZ ) 
           
        return acceloremeter_data
    
    
    def GetHourlyAcceloremeterChart(self, datapath, userid, days):
        """
        datapath:  path to the csv files of the user
        userid: id of the user, e.g. 1024 for prof. Maass
        days: number of days from now to get data for
        """
        
        end_date = datetime.today();
        start_date = end_date - timedelta(days=days)
        delta_hours = end_date - start_date
        number_of_hours = int(delta_hours.total_seconds() / 60 / 60) 
        
    
        filename = datapath + "User_" + str(userid) + "_triathlon.csv"
        
        self.ReadSensorData(filename)
        acceloremeter_data = {};
        
        for h in range(0, number_of_hours):
            targets = [ item for item in self.sensorRawData if item.SensorType == 1 and item.TimeStamp >= start_date + timedelta(hours =h)
                        and item.TimeStamp <= end_date]
            value = 0.0
            
            for item in targets:
                value = value + sqrt(item.ValX * item.ValX  + item.ValY * item.ValY + item.ValZ * item.ValZ )
           
            temp_date = start_date+timedelta(hours =h)
            key = temp_date.strftime('%Y-%m-%d %H')
            # Normalize according the sample length
            if len(targets)  == 0:
                acceloremeter_data[key] = 0
            else:
                acceloremeter_data[key] = value / len(targets) - 9.8 
           
        
        
        
        
           
        return acceloremeter_data
    
   
    
    
    def GetRawGyroscopeChart(self, datapath, userid, days):
        """
        datapath:  path to the csv files of the user
        userid: id of the user, e.g. 1024 for prof. Maass
        days: number of days from now to get data for
        """
    
        end_date = datetime.today();
        start_date = end_date - timedelta(days=days)
        filename = datapath + "User_" + str(userid) + "_triathlon.csv"
        
        self.ReadSensorData(filename)
        
        targets = [ item for item in self.sensorRawData if item.SensorType == 4 and item.TimeStamp >= start_date and item.TimeStamp <= end_date];
        acceloremeter_data = {};
        
        
        for item in targets:
            key = item.TimeStamp.strftime('%Y-%m-%d %H:%M:%S')
           
            acceloremeter_data[key] = sqrt(item.ValX * item.ValX  + item.ValY * item.ValY + item.ValZ * item.ValZ ) 
           
        return acceloremeter_data
    
    def VO2Max_HR_Age(self, restingHeartRate, age):
        MHR = 208 - (0.7 * age);
        return 15.3 * (MHR / restingHeartRate);

"""

import time
import numpy as np
import math

sleeps = reader.GetDailySleepDescriptors(datapath, 1024, start_date, end_date)

training_data = {}

for day in reader.daterange(start_date, end_date):
    training_data[day.strftime('%Y.%m.%d')] = [0];

training_data['2015.10.29'] = [1];
training_data['2015.11.02'] = [1];
training_data['2015.11.03'] = [1];

X = [];
Y = [];

# combine the data
for day in reader.daterange(start_date, end_date):
    key = day.strftime('%Y.%m.%d');
    
    training_features = training_data[key]
    sensor_features = hr_data[key]
    sleep_features = sleeps[key]
    
    allfeatures = [training_features, sleep_features, [sensor_features[0]]];
    X.append([item for array in allfeatures for item in array]);
    Y.append([sensor_features[1]])

X =  np.array(X)
Y = np.array(Y)

x = np.max(np.abs(X), axis=0) 
y = np.max(np.abs(Y), axis=0)

X = X / x
Y = Y / y

import h5py

f = h5py.File("dataset.hdf5", "w")
print f.create_dataset("X", data = X)
print f.create_dataset("Y", data = Y)
print f.create_dataset("x", data = x)
print f.create_dataset("y", data = y)
f.close()
"""
"""
"""

