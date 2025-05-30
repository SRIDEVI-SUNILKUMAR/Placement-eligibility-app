#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# database.py
import mysql.connector
from mysql.connector import Error

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Connected to MySQL.")
        except Error as e:
            print("Error:", e)
            self.connection = None

    def execute_query(self, query, data=None):
        try:
            self.cursor.execute(query, data)
        except Error as e:
            print("Query Error:", e)

    def commit(self):
        self.connection.commit()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed.")

