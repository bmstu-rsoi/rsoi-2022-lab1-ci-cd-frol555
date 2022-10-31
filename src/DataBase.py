import psycopg2
from psycopg2 import Error

DATABASE_URL = "postgres://gsfbpcgbcniasi:7dea11062fc1fde9c0acb971b5393956e93f101cfc40d287151bf8488da13b81@ec2-54-163" \
               "-34-107.compute-1.amazonaws.com:5432/defechmiva6e9v"


class DataBase:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(DATABASE_URL)
            self.cursor = self.connection.cursor()
            if not self.db_check_table():
                self.db_create_table()
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)

    def db_check_table(self):
        self.cursor.execute(
            "SELECT EXISTS (SELECT 1 AS result FROM pg_tables WHERE tablename = 'persons');")
        tableExists = self.cursor.fetchone()[0]
        return tableExists

    def db_create_table(self):
        create_table_query = '''CREATE TABLE persons
                                (
                                    PersonID    SERIAL PRIMARY KEY,
                                    NAME        CHARACTER VARYING(30),
                                    ADDRESS     CHARACTER VARYING(30),
                                    WORK        CHARACTER VARYING(30),
                                    AGE         INTEGER
                                ); '''
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def db_write(self, insert_data):
        insert_query = "INSERT INTO persons (NAME, ADDRESS, WORK, AGE) " \
                       "VALUES (%s,%s,%s,%s) RETURNING PersonID"
        self.cursor.execute(insert_query, insert_data)
        self.connection.commit()
        return self.cursor.fetchone()

    def db_read(self, person_id=None):
        if person_id is None:
            read_query = "SELECT * FROM persons"
        else:
            read_query = f"SELECT * FROM persons WHERE PersonID={person_id}"
        self.cursor.execute(read_query)
        self.connection.commit()

        # Converting to json format
        rows = self.cursor.fetchall()
        objects_list = []
        for row in rows:
            d = dict()
            d["id"] = row[0]
            d["name"] = row[1]
            d["address"] = row[2]
            d["work"] = row[3]
            d["age"] = row[4]
            objects_list.append(d)

        return objects_list

    def db_update(self, person_id, update_data):
        params = ""
        for key in update_data.keys():
            params += f"{key}='{update_data[key]}',"

        tmp = list(params)
        tmp[-1] = " "
        params = "".join(tmp)

        update_query = f"UPDATE persons SET {params} WHERE PersonID={person_id} " \
                       f"RETURNING PersonID, NAME, ADDRESS, WORK, AGE "
        self.cursor.execute(update_query)
        self.connection.commit()
        row = self.cursor.fetchone()
        d = dict()
        d["id"] = row[0]
        d["name"] = row[1]
        d["address"] = row[2]
        d["work"] = row[3]
        d["age"] = row[4]
        return d

    def db_delete(self, person_id):
        delete_query = f"DELETE FROM persons WHERE PersonID={person_id}"
        self.cursor.execute(delete_query)
        self.connection.commit()
        return

    def db_disconnect(self):
        self.cursor.close()
        self.connection.close()
