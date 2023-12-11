import pymysql


conn = pymysql.connect(
    user='user1',
    #password = 'test',
    password = '2ndSemester',
    # host = '10.120.0.209',
    host = '192.168.1.12',
    port=3306,
    database = 'customer_satisfaction')

cur = conn.cursor()
queries = [
    """DROP TABLE IF EXISTS ratings;""",
    """CREATE TABLE ratings (
        id int NOT NULL AUTO_INCREMENT,
        feedback VARCHAR(255) NOT NULL,
        time VARCHAR(255) NOT NULL,
        date VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL,
        PRIMARY KEY (id)
    );""" 
]

           
confirmation = input('Reset Database. continue [Y/n]? ')
if confirmation.lower() in ('y', 'yes'):
    for query in queries:
        cur.execute(query)
    print('successfully created table(s)')

conn.commit()
conn.close()