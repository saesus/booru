import sys
import PyQt5
from  PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import sql as sql

PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

database = r'sqlite/db/booruv1.db'

sql_create_image_table = """ CREATE TABLE IF NOT EXISTS image (
                                        id INTEGER PRIMARY KEY,
                                        name TEXT,
                                        date TEXT NOT NULL,
                                        source TEXT,
                                        explicit INTEGER
                                    ); """

sql_create_tag_table = """ CREATE TABLE IF NOT EXISTS tag (
                                    id INTEGER PRIMARY KEY,
                                    name text NOT NULL
                                ); """

# create a database connection
conn = sql.create_connection(database)

if conn is not None:
    # create image table
    sql.create_table(conn, sql_create_image_table)
    # create tag table
    sql.create_table(conn, sql_create_tag_table)
else:
    print("Error! cannot create the database connection")


def text_based():

    with conn:
        # user input
        com = input("Enter command: ")
        while com:
            if com == "createimage":
                name = input("Enter name: ")
                date = input("Enter date: ")
                source = input("Enter source: ")
                explicit = input("Enter explicit: ")
                # create a new image
                image = (name, date, id, source, explicit)
                sql.create_image(conn, image)
            elif com == "createtag":
                name = input("Enter name: ")
                # create a new tag
                tag = (name,)
                sql.create_tag(conn, tag)
            elif com == "deleteimage":
                name = input("Enter name:")
                sql.delete_image(conn, (name))
            elif com == "deletetag":
                name = input("Enter name:")
                sql.delete_tag(conn, (name))
            elif com == "selectallimage":
                sql.select_all_image(conn)
            elif com == "selectalltag":
                sql.select_all_tag(conn)
            elif com == "selectimagebyname":
                name = input("Enter name: ")
                sql.select_image_by_name(conn, name)
            elif com == "updateimage":
                id = int(input("Enter id: "))
                name = input("Enter name: ")
                date = input("Enter date: ")
                source = input("Enter source: ")
                explicit = input("Enter explicit: ")
                image = (name, date, id, source, explicit)
                sql.update_image(conn, image)
            elif com == "updatetag":
                id = int(input("Enter id: "))
                name = input("Enter name: ")
                tag = (name, id)
                sql.update_tag(tag, id)
            com = input("Enter command: ")

    print("finished")

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'booru 1.1.0'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        button = QPushButton('Add an Image', self)
        button.setToolTip('Add an Image (name, date, image, source, explicit)')
        button.move(100, 70)
        button.clicked.connect(self.on_click)

        self.show()

    @pyqtSlot()
    def on_click(self):
        sql.select_all_image(conn)

def run_app():
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
