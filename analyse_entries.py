import database
from datetime import datetime
import matplotlib
from dateutil import rrule
from datetime import datetime
from datetime import timedelta
import pymongo
import pprint

matplotlib.use('Agg')
import matplotlib.pyplot as plt

db_inserts, db_extends = database.init()


def analyse(user: str, day: datetime):
    cooldown_value_list = db_extends.find_data_full(user, day, 'Cooldown', 'Heart rate')
    training_value_list = db_extends.find_data_full(user, day, 'TrainingHR', 'Heart rate')
    if len(cooldown_value_list) == 0 or len(training_value_list) == 0:
        print("No data for", user, "(at", day, ")")
        return
    cooldown_value_list.sort(key=lambda key: key.time_stamp)
    training_value_list.sort(key=lambda key: key.time_stamp)
    cooldown_start_time = cooldown_value_list[0].time_stamp
    cooldown_end_time = cooldown_value_list[-1].time_stamp
    training_start_time = training_value_list[0].time_stamp
    training_end_time = training_value_list[-1].time_stamp
    x_axis_cooldown_values = []
    x_axis_training_values = []
    y_axis_cooldown_values = []
    y_axis_training_values = []
    for value in training_value_list:
        x_axis_training_values.append((value.time_stamp - training_start_time).seconds)
        y_axis_training_values.append(value.val0)
    line = plt.plot(x_axis_training_values, y_axis_training_values, 'ro', color="red", linewidth=50)
    for value in cooldown_value_list:
        x_axis_cooldown_values.append((value.time_stamp - training_start_time).seconds)
        y_axis_cooldown_values.append(value.val0)
    plt.plot(x_axis_cooldown_values, y_axis_cooldown_values, 'ro', color="blue", linewidth=50)
    minimal_value = min(cooldown_value_list, key=lambda val: val.val0).val0
    maximal_value = max(cooldown_value_list, key=lambda val: val.val0).val0
    time_delta = cooldown_end_time - training_start_time
    plt.xticks(range(0, time_delta.seconds, 120))
    plt.axis([0, time_delta.seconds, minimal_value, maximal_value])
    plt.show()
    plt.xlabel('seconds')
    plt.ylabel('BPM')
    plt.savefig(('%s_%s.png' % (user, day.date())), dpi=600)
    plt.clf()
    print('\n\n\n----------------------------------------------------------------------')
    print('For user', user)
    print('training took:', training_end_time - training_start_time, 'minutes from:', training_start_time, 'to',
          training_end_time)
    print('cooldown took:', cooldown_end_time - cooldown_start_time, ' minutes from:', cooldown_start_time, 'to',
          cooldown_end_time)
    print('----------------------------------------------------------------------\n\n\n')

def analyse_patients ():
    first_day = datetime(2016, 12, 12, 0, 0, 0)
    second_day = datetime(2016, 12, 14, 0, 0, 0)
    third_day = datetime(2016, 12, 15, 0, 0, 0)
    fourth_day = datetime(2016, 12, 19, 0, 0, 0)

    users = [('pathmate2.p8@gmail.com', first_day),
             ('pathmate2.p9@gmail.com', second_day),
             ('pathmate2.p10@gmail.com', fourth_day),
             ('pathmate2.p11@gmail.com', first_day),
             ('pathmate2.p12@gmail.com', fourth_day),
             ('pathmate2.p13@gmail.com', first_day),
             ('pathmate2.p14@gmail.com', third_day),
             ('pathmate2.p15@gmail.com', fourth_day),
             ('pathmate2.p17@gmail.com', fourth_day),
             ('pathmate2.p33@gmail.com', third_day),
             ('pathmate2.p34@gmail.com', fourth_day),
             ('pathmate2.p36@gmail.com', fourth_day),
             ('pathmate2.p41@gmail.com', fourth_day),
             ('pathmate2.p51@gmail.com', second_day)]
    for user in users:
        analyse(user[0], user[1])

def analyse_data_all_days ():
    users = ['s9mhpaul@stud.uni-saarland.de', 'ralfbleymehl@gmail.com']
    for user in users:
        tags = ['Cooldown', 'TrainingHR', 'Step Tracking', 'Sleep Tracking']
        start_date = db_extends.db_base._db['%s_measure' % user].find().sort('effectiveDateTime', pymongo.ASCENDING).limit(1)[0]['effectiveDateTime']
        end_date = db_extends.db_base._db['%s_measure' % user].find().sort('effectiveDateTime', pymongo.DESCENDING).limit(1)[0]['effectiveDateTime']
        dates = []
        for day in rrule.rrule(rrule.DAILY, dtstart=start_date,
                               until=end_date):
            dates.append(day.date())
        all_data = list(db_extends.db_base._db['%s_measure' % user].find())
        print(len(all_data))
        res = []
        for day in dates:
            temp = {}
            for tag in tags:
                data_size = len(list(filter(lambda entry: entry['effectiveDateTime'].date() == day and entry['category']['coding'][0]['display'] == tag, all_data)))
                if data_size > 0:
                    temp[tag] = data_size
            if len(temp) > 0:
                res.append({day.strftime('%d.%m.%Y') :temp })
        res = {user : res}
        pprint.pprint(res, indent=4)


if __name__ == '__main__':
    analyse_data_all_days()
