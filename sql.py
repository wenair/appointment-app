import sqlite3
import datetime
from flask import g

def create_table():
    print("Creating table")
    create_query='''CREATE TABLE IF NOT EXISTS appointments (                                                                                                                                                                         
                    id INTEGER NOT NULL PRIMARY KEY,                                                                                                                                                                                                             userid TEXT NOT NULL,                                                                                                                                                                                                                        appointment timestamp);'''
    query_sql(create_query, None, False, True)
    
def get_records_for_id(userid):
    select_query = """SELECT userid, appointment from appointments where userid = ?"""
    data_tuple=(userid,)
    records = query_sql(select_query, data_tuple, True)
    if records is not None and len(records) > 0:
        print("SQL: found no records"); 
    else:
        print("SQL: found ", len(records), " records")
    return records

def insert_record(userid, appointment):
    sqlite_insert_with_param = """INSERT INTO 'appointments'                                                                                                                                                                         
                      ('userid', 'appointment')                                                                                                                                                                                      
                      VALUES (?, ?);"""                                                                                                                                                                                               

    data_tuple = (userid, appointment)                   
    query_sql(sqlite_insert_with_param, data_tuple, False, True)


def get_matches(userid, dt):
     sqlite_select_query = """SELECT userid, appointment from appointments where userid = ? AND DATE(appointment) = ?"""
     data_tuple=(userid,dt.date())
     records = query_sql(sqlite_select_query, data_tuple, True)
     if records is not None and len(records) > 0:
         return True
     else:
         return False

def drop_table():
    drop_query='''DROP TABLE appointments'''
    query_sql(drop_query, None, False, True)

def query_sql(query, data_tuple=None, return_results=False, should_commit=False):
    try:
        sqliteConnection = sqlite3.connect('SQLite_Python.db',
                                          detect_types=sqlite3.PARSE_DECLTYPES |
                                          sqlite3.PARSE_COLNAMES)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        if data_tuple is None:
            print("executing query without data tuple")
            cursor.execute(query)
        else:
            print("executing query with data tuple")
            cursor.execute(query, data_tuple)
        print(query)

        if should_commit is True:
            sqliteConnection.commit() 

        if return_results is True:
            records = cursor.fetchall();
                    
    except sqlite3.Error as error:
        print("Error while working with SQLite", error)
    finally:
        sqliteConnection.close()

    if return_results is True:
        return records

drop_table()
create_table()
