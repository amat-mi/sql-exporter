import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('test.sqlite')
    with conn:
        cursor = conn.cursor()
        create = "CREATE TABLE test(one varchar(10), two smallint);"
        cursor.execute(create)
        for x in range(10):
            insert = "INSERT INTO test VALUES(?, ?)"
            cursor.execute(insert, (str(x),x))
        cursor.close()
    