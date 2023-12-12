import pymysql
from datetime import datetime



def get_timestamp():
    current_datetime = datetime.now()
    current_time = current_datetime.strftime("%H:%M:%S")
    current_date = current_datetime.strftime("%d/%m/%Y")
    return (current_time, current_date)

def insert_to_db(msg, time, date, location):
    conn = pymysql.connect(
    user='user1',
    password = 'test',
    host = '192.168.2.21',
    port=3306,
    database = 'customer_satisfaction')
    cur = conn.cursor()
    query = f"""INSERT INTO ratings (feedback, time, date, location)  
                VALUES('{msg}', '{time}', '{date}', '{location}');"""
    cur.execute(query)
    print(f'successfully updated the database')
    conn.commit()
    conn.close()

