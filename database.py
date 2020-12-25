import os

import psycopg2

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

    def info(self):
        """Display the information from the database connection
        """
        print('\n*** Database information ***')
        print('HOST:\t\t', HOST)
        print('PORT:\t\t', PORT)
        print('DATABASE:\t', DATABASE)
        print('USER:\t\t', USER)
        print('PASSWORD:\t', PASSWORD)
        print('\n')

    def select(self, table, columns='*', order='item_id'):
        """SQL select call

        Args:
            table (str): 'FROM' statement
            columns (str, optional): 'SELECT' statement columns. Defaults to '*'.
            order (str, optional): 'ORDER BY' statement. Defaults to 'item_id'.

        Returns:
            [type]: [description]
        """
        command = 'SELECT ' + columns + ' FROM ' + str(table) + ' ORDER BY ' + order + ';'
        self.cur.execute(command)
        query = self.cur.fetchall()
        print(command)
        return query

    def set(self, table, item, value):
        """SQL set call

        Args:
            table (str): 'FROM' statement
            item (str): 'WHERE' statement
            value (str): 'SET' statement
        """
        command = 'UPDATE ' + str(table) + " SET item='" + str(value) + "' WHERE item='" + str(item) + "';"
        self.cur.execute(command)
        self.conn.commit()
        print('\n' + command)

    def delete(self, table, item):
        """SQL DELETE call

        Args:
            table (str): 'FROM' statement
            item (str): 'WHERE' statement
        """
        command = 'DELETE FROM ' + str(table) + " WHERE item='" + str(item) + "';"
        self.cur.execute(command)
        self.conn.commit()
        print('\n' + command)

    def truncate(self, table):
        """SQL TRUNCATE call

        Args:
            table (str): 'TUNCATE' statement
        """
        command = 'TRUNCATE ' + str(table) + ';'
        self.cur.execute(command)
        self.conn.commit()
        print('\n' + command)

    def insert(self, table, value):
        """SQL INSERT call

        Args:
            table (str): 'FROM' statement
            value (str): 'VALUES' statement
        """
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

    def close(self):
        """Close the connection to the database
        """
        print('\nClosing connection...')
        self.conn.close()
        self.cur.close()
        print('Connection closed')
