import psycopg2, os

#!  Credentials set in environment variables
HOST =  os.environ['POSTGRESQL_HOST']
PORT = os.environ['POSTGRESQL_PORT']
DATABASE = os.environ['LIST_DATABASE']
USER = os.environ['POSTGRESQL_USER']
PASSWORD = os.environ['POSTGRESQL_PASSWORD']

class database:
    def __init__(self):
        #*  Make the database connection
        self.conn = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
        self.cur = self.conn.cursor()

    #   SQL select call
    #   table       -'FROM' statement
    #   columns     -'SELECT' statement columns
    #   order       -'ORDER BY' statement
    def select(self, table, columns='*', order='item_id'):
        command = 'SELECT ' + columns + ' FROM ' + str(table) + ' ORDER BY ' + order + ';'
        self.cur.execute(command)
        query = self.cur.fetchall()
        print(command)
        return query

    #   SQL set call
    #   table   -'FROM' statement
    #   item    -'WHERE' statement
    #   value   -'SET' statement
    def set(self, table, item, value):
        command = 'UPDATE ' + table + " SET item='" + str(value) + "' WHERE item='" + str(item) + "';"
        self.cur.execute(command)
        self.conn.commit()
        print('\n' + command)

    #   SQL DELETE call
    #   table   -'FROM' statement
    #   item    -'WHERE' statement
    def delete(self, table, item):
        command = 'DELETE FROM ' + table + " WHERE item='" + str(item) + "';"
        self.cur.execute(command)
        self.conn.commit()
        print('\n' + command)

    #   SQL TRUNCATE call
    #   table   -'TUNCATE' statement
    def truncate(self, table):
        command = 'TRUNCATE ' + str(table) + ';'
        self.cur.execute(command)
        self.conn.commit()
        print('\n' + command)

    #   SQL INSERT call
    #   table   -'FROM' statement
    #   value   -'VALUES' statement
    def insert(self, table, value):
        #*  Get the largest id in the database
        command = 'SELECT MAX(item_id) FROM ' + str(table) + ';'
        self.cur.execute(command)
        query = self.cur.fetchall()
        print('\n' + command)

        if query[0][0]:
            max_id = query[0][0] + 1
        else:
            max_id = 1

        #*  Insert the new item with id = max + 1
        command = 'INSERT INTO ' + str(table) + "(item_id, item, completed) VALUES(" + str(max_id) + ", '" + value + "', False);"
        self.cur.execute(command)
        self.conn.commit()
        print(command)

    #   Close the connection to the database
    def close(self):
        print('\nClosing connection...')
        self.conn.close()
        self.cur.close()
        print('Connection closed')