import mysql.connector
from mysql.connector import Error

# to establish connection to our database we need some parameters first
db_name = 'fitness_center'
user = 'root'
password = 'Tomatillo4!'
host = '127.0.0.1'  # localhost = 127.0.0.1


def connection():
    '''
Creates and returns a connection to our database.
'''
    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host)  # connect function only takes certain keyword arguements which is why we have to create new variables here

        if conn.is_connected():
            print("Connected to MySQL database successful!")
            return conn

    except Error as e:
        print(f"Error: {e}")
        return None
