import psycopg2, os

#!  Credentials set in environment variables
HOST =  os.environ['LIST_HOST']
PORT = os.environ['LIST_PORT']
DATABASE = os.environ['LIST_DATaBASE']
USER = os.environ['LIST_USER']
PASSWORD = os.environ['LIST_PASSWORD']

class database:
    def __init__(self):
        #*  Make the database connection
        self.conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
        self.cur = self.conn.cursor()

    #   SQL select call
    #   table       -'FROM' statement
    #   columns     -'SELECT' statement columns
    #   condition   -'WHERE' statement
    #   order       -'ORDER BY' statement
    def select(self, table, columns='*', condition=0, order=0):
        command = 'SELECT ' + columns + ' FROM ' + str(table)
        self.cur.execute(command)
        query = self.cur.fetchall()
        return query

    #   SQL set call
    #   table   -'FROM' statement
    #   item    -'WHERE' statement
    #   value   -'SET' statement
    def set(self, table, item, value):
        command = 'UPDATE ' + table + " SET item='" + str(value) + "' WHERE item='" + str(item) + "';"
        self.cur.execute(command)
        self.conn.commit()

    #   SQL DELETE call
    #   table   -'FROM' statement
    #   item    -'WHERE' statement
    def delete(self, table, item):
        command = 'DELETE FROM ' + table + " WHERE item='" + str(item) + "';"
        self.cur.execute(command)
        self.conn.commit()

    #   SQL TRUNCATE call
    #   table   -'TUNCATE' statement
    def truncate(self, table):
        command = 'TRUNCATE ' + str(table)
        self.cur.execute(command)
        self.conn.commit()

    #   SQL INSERT call
    #   table   -'FROM' statement
    #   value   -'VALUES' statement
    def insert(self, table, value):
        #*  Get the largest id in the database
        command = 'SELECT MAX(item_id) FROM ' + str(table)
        self.cur.execute(command)
        query = self.cur.fetchall()

        if query[0][0]:
            max_id = query[0][0] + 1
        else:
            max_id = 1

        #*  Insert the new item with id = max + 1
        command = 'INSERT INTO ' + str(table) + "(item_id, item, completed) VALUES (" + str(max_id) + ", '" + value + "',False);"
        self.cur.execute(command)
        self.conn.commit()

    #   Close the connection to the database
    def close(self):
        print('Closing connection...')
        self.conn.close()
        self.cur.close()
        print('Connection closed')