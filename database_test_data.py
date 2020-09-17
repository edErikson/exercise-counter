from random import choice
import random
import time
from datetime import datetime
from database import add_act, add_done_act, first_time_db, get_acts, db_connection, get_column_names, sql_command_dict, get_done_acts
import os


def str_time_prop(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%d.%m.%Y %H:%M:%S', prop)


class Choice:
    def __init__(self, *choice):
        self._choice = choice

    def __get__(self, obj, owner):
        return choice(self._choice)


class TestData:
    acts = Choice(1, 2, 3, 4, 5)
    quantity = Choice(10, 15, 20, 25, 30, 35, 40, 50, 60)


g = TestData()
test_data_dict = {}


def test_dict_data():
    for i in range(271):
        acts = g.acts
        qty = g.quantity
        date = random_date("04.04.2020 09:00:00", "20.05.2020 18:30:00", random.random())
        if date[:11] in test_data_dict:
            test_data_dict[date[:11]].append((acts, qty, date[11:]))
        else:
            test_data_dict[date[:11]] = [(acts, qty, date[11:])]


def test_db_record(records=300):
    for i in range(records):
        acts = g.acts
        qty = g.quantity
        date = random_date("04.04.2020 09:00:00", "20.05.2020 18:30:00", random.random())
        datetime_object = datetime.strptime(date, '%d.%m.%Y %H:%M:%S')
        yield acts, qty, datetime_object.date(), str(datetime_object.time())


##################################################################################
def insert_first_acts():
    actions = ['pushups', 'press', 'situps', 'shoulders', 'biceps']
    for act in actions:
        add_act(act)
    print('Finished')


def insert_done_acts_test_data():
    for line in test_db_record(350):
        add_done_act(line[0], line[1], line[2], line[3])
    print('Finished')


if __name__ == "__main__":
    if not os.path.isfile("exercise.db"):
        print('No database detected, creating...')
        first_time_db()
        print(get_column_names())
    else:
        print('database detected with, \nTable name: ', db_connection(sql_command_dict['table_name_sql'], receive=True))
        print()
        if not get_acts():
            print('Adding acts....')
            insert_first_acts()
            print(get_acts())
        else:
            print('Table "acts" items', get_acts())
            if not get_done_acts():
                print('Table "done_acts items :', get_done_acts(),'\nempty table, need data...')
                print('inserting test data for "done_acts" table')
                insert_done_acts_test_data()
            else:
                print("***** Current done acts ***")
                #print(db_connection(sql_command_dict['all_done_acts_sql'], receive=True))
                print('Test data stats : acts, made, days, reps, avg',db_connection(sql_command_dict['all_stat_sql'], receive=True))
