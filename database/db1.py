# import psycopg2
# 
# 
# 
# try:
#     print "Inside try"
#     conn = psycopg2.connect(database="test_db", user = "pavankumark", password = "123Welcome@", host = "127.0.0.1", port = "5432")
# except:
#     print "I am unable to connect to the database"
# 
# print "cur"
# cur = conn.cursor()
# 
# cur.execute("DROP TABLE IF EXISTS management")
# 
# # Create table as per requirement
# sqls = '''CREATE TABLE management
#          ( ID INT PRIMARY KEY     NOT NULL,
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,  
#          SEX CHAR(1),
#          INCOME FLOAT );'''
# 
# print sqls
# cur.execute(sqls)
# print "executed **"
# # disconnect from server
# conn.close()



#################

import psycopg2
 
conn = psycopg2.connect(database="test_db", user = "pavankumark", password = "123Welcome@", host = "127.0.0.1", port = "5432")
 
print ("Opened database successfully")
 
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS daily_data")
 
cur.execute('''CREATE TABLE daily_data
      (ID INT PRIMARY KEY     NOT NULL,
      NAME           TEXT    NOT NULL,
      AGE            INT     NOT NULL,
      ADDRESS        CHAR(50),
      SALARY         REAL);''')
print ("Table created successfully")
 
conn.commit()
conn.close()