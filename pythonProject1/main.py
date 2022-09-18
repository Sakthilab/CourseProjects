import pymysql

def insert_row(name, country, team):
    conn = pymysql.connect(user="root", password="welcome$1234", host="127.0.0.1", database="test_python_sql")
    cursor = conn.cursor()
    sql_query = f"insert into players(Name, Country, IPL_team) values('{name}', '{country}', '{team}')"
    print(sql_query)
    try:
        cursor.execute(sql_query)
        conn.commit()
        print(" row inserted")
    except Exception as ex:
        print("error")
        message = f'''an exception type of {type(ex).__name__}occurred. Arguments:{ex.args}'''
        print(message)
    finally:
        cursor.close()
        conn.close()

def select():
    print('########## PRINT THE TABLE CONTENT #########')
    conn = pymysql.connect(user="root", password="welcome$1234", host="127.0.0.1", database="test_python_sql")
    cursor = conn.cursor()
    cursor.execute("select * from players")
    row = cursor.fetchone()
    while True:
        if row is not None:
            print(row)
        else:
            break


n = int(input("enter the number of row "))
for i in range(n):
    name = input("Enter the name ")
    country = input("Enter the country ")
    team = input("Enter the team name ")
    insert_row(name, country, team)
    print('------------------------------------------')
select()







