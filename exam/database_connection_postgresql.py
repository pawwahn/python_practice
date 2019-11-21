import psycopg2
def main():
    try:
        con = psycopg2.connect(database='test_db',user='Pavank',password='password',host='localhost',port=5432)
        cur = con.cursor()
        cur.executescript('CREATE TABLE STUDENT (id INT, name Varchar,place Varchar);'
                          'INSERT INTO STUDENT (id,name,place) values(1,"pavan","Chennai");'
                          'INSERT INTO STUDENT (id,name,place) values(1,"pavan","Chennai");')
        con.commit()
        cur.execute('Select * from student')
        data = cur.fetchall()
        for row in data:
            print row
    except psycopg2.Error as e:
        if con:
            con.rollback()
            print "Problem with database connection"
    finally:
        if con:
            con.close()

if __name__=='__main__':
    main()