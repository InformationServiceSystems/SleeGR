import database

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

db_inserts, db_extends = database.init()
def analyse(user):
    cooldown = db_extends.find_data_tag(user, 'Cooldown', 'Heart rate')
    training = db_extends.find_data_tag(user, 'TrainingHR', 'Heart rate')
    cooldown.sort(key=lambda key: key.time_stamp)
    training.sort(key=lambda key: key.time_stamp)
    cooldown_start = cooldown[0].time_stamp
    cooldown_end = cooldown[-1].time_stamp
    training_start = training[0].time_stamp
    training_end = training[-1].time_stamp
    x = []
    y = []
    for value in cooldown:
        x.append((value.time_stamp - cooldown[0].time_stamp).seconds)
        y.append(value.val0)
        print (type(value.val0))
    plt.plot(x,y, 'ro')
    mini = min(cooldown, key=lambda val:val.val0).val0
    maxa = max(cooldown, key=lambda val:val.val0).val0
    print(mini, maxa)
    plt.axis([0, (cooldown[-1].time_stamp - cooldown[0].time_stamp).seconds, mini, maxa])
    plt.show()
    plt.savefig(('%s.png' % user))
    plt.clf()
    print('\n\n\n----------------------------------------------------------------------')
    print('For user', user)
    print('training took:', training_end-training_start, 'minutes from:', training_start, 'to', training_end)
    print('cooldown took:', cooldown_end-cooldown_start, ' minutes from:', cooldown_start, 'to', cooldown_end)


if __name__ == '__main__':
    users = ['pathmate2.p8@gmail.com',
             'pathmate2.p9@gmail.com',
             'pathmate2.p11@gmail.com',
             'pathmate2.p13@gmail.com',
             'pathmate2.p14@gmail.com',
             'pathmate2.p33@gmail.com',
             'pathmate2.p51@gmail.com']
    for user in users:
        analyse(user)