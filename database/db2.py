import psycopg2

print (psycopg2.__version__)
 
conn = psycopg2.connect(database="test_db", user = "pavankumark", password = "123Welcome@", host = "127.0.0.1", port = "5432")
 
print ("Opened database successfully")
 
cur = conn.cursor()

cur.execute("""
                INSERT INTO COLLEGE
                        (id, first_name, last_name, age, sex, income) 
                VALUES (1,'Pavan Kumar','Kota',25,'M',25000);


            """)

conn.commit()
conn.close()





"""
INSERT INTO abs_absent_location_rel(
            search_id, location_id)
    VALUES (?, ?);


"""