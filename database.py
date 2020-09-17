import sqlite3

sql_command_dict = {
    'first_sql': "CREATE TABLE IF NOT EXISTS acts(act_id INTEGER PRIMARY KEY, act_name TEXT NOT NULL UNIQUE)",
    'second_sql': "CREATE TABLE IF NOT EXISTS done_acts(done_id INTEGER PRIMARY KEY, "
                  "act_id  INTEGER NOT NULL, quantity INTEGER NOT NULL, date DATE, time TIME,"
                  "FOREIGN KEY (act_id) REFERENCES acts(act_id))",

    'acts_column_name_sql': "PRAGMA table_info(acts)",
    'done_acts_column_name_sql': "PRAGMA table_info(done_acts)",
    'table_name_sql': "SELECT name FROM sqlite_master where type='table'",

    'add_act_sql': "INSERT INTO acts(act_name) VALUES (?)",
    'add_task_sql': "INSERT INTO done_acts(act_id, quantity, date, time) VALUES (?,?,?,?)",

    'all_acts_sql': "SELECT act_id, act_name FROM acts",
    'all_done_acts_sql': "SELECT done_id, act_id, quantity, date, time FROM done_acts",

    'all_stat_sql': "SELECT COUNT(distinct act_id), COUNT(act_id), COUNT(DISTINCT date), sum(quantity), ROUND(avg(quantity),1) from done_acts"

    }


def db_connection(sql_task, data=None, receive=False):
    conn = sqlite3.connect('exercise.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cursor = conn.cursor()
    if data:
        cursor.execute(sql_task, data)
    else:
        cursor.execute(sql_task)

    if receive:
        return cursor.fetchall()
    else:
        conn.commit()
    conn.close()


def first_time_db():
    try:
        db_connection(sql_command_dict['first_sql'])
        print("created :", db_connection(sql_command_dict['acts_column_name_sql'], receive=True))
        db_connection(sql_command_dict['second_sql'])
        print("created :", db_connection(sql_command_dict['done_acts_column_name_sql'], receive=True))
    except Exception as e:
        print('Error on string: ', e)


def get_column_names():
    cursor = db_connection(sql_command_dict['done_acts_column_name_sql'], receive=True)
    done_acts_column = list(map(lambda x: x[1], cursor))

    cursor2 = db_connection(sql_command_dict['acts_column_name_sql'], receive=True)
    acts_column = list(map(lambda x: x[1], cursor2))
    return 'done_act columns : ', tuple(done_acts_column), 'acts_column :', tuple(acts_column)


def add_act(name):
    db_connection(sql_command_dict['add_act_sql'], (name,))


def add_done_act(act_id, quantity, date, time):
    db_connection(sql_command_dict['add_task_sql'], (act_id, quantity, date, time,))


def get_acts():
    return db_connection(sql_command_dict['all_acts_sql'], receive=True)


def get_done_acts():
    return db_connection(sql_command_dict['all_done_acts_sql'], receive=True)


################################
def get_all_stats():
    return db_connection(sql_command_dict['all_stat_sql'], receive=True)


