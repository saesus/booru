import sqlite3
from sqlite3 import Error
import pathlib
#import PyQt5
#from PyQt5.QtWidgets import QApplication, QLabel

import os, errno

"""
Ctrl+Shift+P, SQLite
c:/Users/darkl/Documents/booru/booru.py to run
drag sqlite3.exe onto the booruv1.db file to run 
then type> select * from image;

"""
 
def create_connection(db_file):
    """ create a database connection to a SQLite database 
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    
    return None

def create_table(conn, create_table_sql):
    """ create a table from create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return: 
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_image(conn, image):
    """ create a new image in the image table
    :param conn: Connection object
    :param image:
    :return: image id
    """
    sql = ''' INSERT INTO image(name, date)
            VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, image)
    return cur.lastrowid

def create_tag(conn, tag):
    """ create a new tag in the tag table
    :param conn: Connection object
    :param tag:
    :return: tag id
    """
    sql = ''' INSERT INTO tag(name)
            VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, tag)
    return cur.lastrowid

def delete_image(conn, name):
    """
    Delete an image by image name
    :param conn: Connection object
    :param name: image name
    :return:
    """
    sql = 'DELETE FROM image WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (name,))

def delete_all_image(conn):
    """
    Delete all rows in the image table
    :param conn: Connection object
    :return:
    """
    sql = 'DELETE FROM image'
    cur = conn.cursor()
    cur.execute(sql)

def delete_tag(conn, name):
    """
    Delete an tag by tag name
    :param conn: Connection object
    :param name: tag name
    :return:
    """
    sql = 'DELETE FROM tag WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (name,))

def delete_all_tag(conn):
    """
    Delete all rows in the tag table
    :param conn: Connection object
    :return:
    """
    sql = 'DELETE FROM image'
    cur = conn.cursor()
    cur.execute(sql)

def select_all_image(conn):
    """
    Query all rows in the image table
    :param conn: Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM image")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def select_image_by_name(conn, name):
    """
    Query image by name
    :param conn: Connection object
    :param name: image name
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM image WHERE name=?", (name,))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def select_all_tag(conn):
    """
    Query all rows in the tag table
    :param conn: Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tag")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def update_image(conn, image):
    """
    update name,date of an image
    :param conn: Connection object
    :param image:
    :return: image id
    """
    sql = ''' UPDATE image
            SET name = ? ,
                date = ?
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, image)
    return cur.lastrowid

def update_tag(conn, tag):
    """
    update name of a tag
    :param conn: Connection object
    :param tag:
    :return: tag id
    """
    sql = ''' UPDATE tag
            SET name = ?,
            WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, tag)
    return cur.lastrowid

def main():
    database = r'sqlite/db/booruv1.db'

    # Ensures that the directory exists, if not, creates one
    try:
        os.makedirs('sqlite/db')
    except FileExistsError:
        # directory already exists
        pass

    sql_create_image_table = """ CREATE TABLE IF NOT EXISTS image (
                                        id INTEGER PRIMARY KEY,
                                        name text NOT NULL,
                                        date text NOT NULL
                                    ); """
    
    sql_create_tag_table = """ CREATE TABLE IF NOT EXISTS tag (
                                        id INTEGER PRIMARY KEY,
                                        name text NOT NULL
                                    ); """

    #create a database connection
    conn = create_connection(database)

    if conn is not None:
        #create image table
        create_table(conn, sql_create_image_table)
        #create tag table
        create_table(conn, sql_create_tag_table)
    else:
        print("Error! cannot create the database connection")

    with conn:
        #user input
        com = input("Enter command: ")
        while com != "exit":
            if com == "createimage":
                name = input("Enter name: ")
                date = input("Enter date: ")
                #create a new image
                image = (name, date)
                create_image(conn, image)
            elif com == "createtag":
                name = input("Enter name: ")
                #create a new tag
                tag = (name,)
                create_tag(conn, tag)   
            elif com == "deleteimage":
                name = input("Enter name:")
                delete_image(conn, (name))
            elif com == "deletetag":
                name = input("Enter name:")
                delete_tag(conn, (name))
            elif com == "selectallimage":
                select_all_image(conn)
            elif com == "selectalltag":
                select_all_tag(conn)
            elif com == "selectimagebyname":
                name = input("Enter name: ")
                select_image_by_name(conn, name)
            elif com == "updateimage":
                id = int(input("Enter id: "))
                name = input("Enter name: ")
                date = input("Enter date: ")
                image = (name, date, id)
                update_image(conn, image)
            elif com == "updatetag":
                id = int(input("Enter id: "))
                name = input("Enter name: ")
                tag = (name, id)
                update_tag(tag, id)
            com = input("Enter command: ")

    print("finished")

if __name__ == '__main__':
    main()
