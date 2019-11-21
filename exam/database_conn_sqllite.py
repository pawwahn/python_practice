import sqllite3
try:
    con = sqllite3.connect("test_db")       #   connection establishment
    cur = con.cursor()                      #   creation of cursor
    cur.execute("DROP TABLE IF EXISTS Employee")
    cur.execute('CREATE TABLE EMPLOYEE (id INT, name VARCHAR, city VARCHAR)')
    cur.execute("INSERT INTO EMPLOYEE VALUES(1,'pavan','chennai')")
    con.commit()
    cur.execute("SELECT * FROM EMPLOYEE")
    data = cur.fetchall()
    for row in data:
        print (row)
except sqllite3.Error as e:
    if con:
        con.rollback()
        print ("There was a problem occured")
finally:
    if con:
        con.close()

