from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLabel, QLineEdit, QComboBox, QFrame
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5 import uic
import pandas as pd
import sqlite3


# connect existing database or create new one and create a cursor:
conn = sqlite3.connect('chincho.db')
curr = conn.cursor()
# create table if it does not exists:
curr.execute('''CREATE TABLE IF NOT EXISTS user(name text, surname text, birthdate text, gender text, phone text, email text, country text, city text)''')
# commit changes and close connection:
conn.commit()
conn.close()


class MikeTyson(QMainWindow):
    def __init__(self):
        super(MikeTyson, self).__init__()

        uic.loadUi("register.ui", self)

        #define content:
        self.hello_label = self.findChild(QLabel, "hello_label")
        self.name_label = self.findChild(QLabel, "name_label")
        self.surname_label = self.findChild(QLabel, "surname_label")
        self.birth_label = self.findChild(QLabel, "birth_label")
        self.gender_label = self.findChild(QLabel, "gender_label")
        self.phone_label = self.findChild(QLabel, "phone_label")
        self.mail_label = self.findChild(QLabel, "mail_label")
        self.country_label = self.findChild(QLabel, "country_label")
        self.city_label = self.findChild(QLabel, "city_label")
        self.answer_label = self.findChild(QLabel, "answer_label")

        self.name_line = self.findChild(QLineEdit, "name_line")
        self.surname_line = self.findChild(QLineEdit, "surname_line")
        self.birth_line = self.findChild(QLineEdit, "birth_line")
        self.phone_line = self.findChild(QLineEdit, "phone_line")
        self.mail_line = self.findChild(QLineEdit, "mail_line")
        self.country_line = self.findChild(QLineEdit, "country_line")
        self.city_line = self.findChild(QLineEdit, "city_line")
        self.value_line = self.findChild(QLineEdit, "value_line")
        self.update_line = self.findChild(QLineEdit, "update_line")
        self.old_line = self.findChild(QLineEdit, "old_line")

        self.submit_button = self.findChild(QPushButton, "submit_button")
        self.show_button = self.findChild(QPushButton, "show_button")
        self.close_button = self.findChild(QPushButton, "close_button")
        self.delete_button = self.findChild(QPushButton, "delete_button")
        self.update_button = self.findChild(QPushButton, "update_button")

        self.line_1 = self.findChild(QFrame, "line_1")
        self.line_2 = self.findChild(QFrame, "line_2")

        self.box_1 = self.findChild(QComboBox, "box_1")
        self.box_2 = self.findChild(QComboBox, "box_2")
        self.box_3 = self.findChild(QComboBox, "box_3")
        self.box_4 = self.findChild(QComboBox, "box_4")

        self.table_widget = self.findChild(QTableWidget, "table_widget")

        # define some validators:
        allowed = QRegExp("[a-z-A-Z_]+")
        magia = QRegExpValidator(allowed)
        self.name_line.setValidator(magia)
        self.surname_line.setValidator(magia)
        self.country_line.setValidator(magia)
        self.city_line.setValidator(magia)

        Only_int = QIntValidator()
        self.phone_line.setValidator(Only_int)


        # call defined methods from here:
        self.submit_button.clicked.connect(self.Insert_Into_DataBase)
        self.show_button.clicked.connect(self.Display_From_Database)
        self.delete_button.clicked.connect(self.Delete_from_database)
        self.update_button.clicked.connect(self.Update_Database)
        self.close_button.clicked.connect(lambda: self.close())

        self.show()

#------------------------------------------ logic ------------------------------------- #
    # define colors:
    def Green(self):
        self.answer_label.setStyleSheet("background-color: rgb(155, 255, 184)")
    def Red(self):
        self.answer_label.setStyleSheet("background-color: rgb(255, 178, 216)")
    def White(self):
        self.answer_label.setStyleSheet("background-color: rgb(240, 240, 240)")

    # define clean method:
    def Clean_fields(self):
        self.name_line.setText("")
        self.surname_line.setText("")
        self.birth_line.setText("")
        self.phone_line.setText("")
        self.mail_line.setText("")
        self.country_line.setText("")
        self.city_line.setText("")
        self.value_line.setText("")
        self.old_line.setText("")
        self.update_line.setText("")

    # take items from database:
    def Display_From_Database(self):
        conn = sqlite3.connect("chincho.db")
        curr = conn.cursor()

        basic_list = []
        for item in curr.execute('''SELECT * FROM user'''):
            basic_list.append(list(item))

        conn.commit()
        conn.close()

        magic_frame = pd.DataFrame(basic_list, columns = ['Name', 'Surname', 'BirthDate', 'Gender', 'Phone', 'Email', 'Country', 'City'])
        
        RowNumber = len(magic_frame.index)
        ColumnNumber = len(magic_frame.columns)

        self.table_widget.setColumnCount(ColumnNumber)
        self.table_widget.setRowCount(RowNumber)
        self.table_widget.setHorizontalHeaderLabels(magic_frame.columns)

        for rows in range(RowNumber):
            for columns in range(ColumnNumber):
                self.table_widget.setItem(rows, columns, QTableWidgetItem(str(magic_frame.iat[rows, columns])))
        
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        self.answer_label.setText("")
        self.White()
        self.Clean_fields()

    # define method for submit button:
    def Insert_Into_DataBase(self):
        firstname = self.name_line.text()
        lastname = self.surname_line.text()
        birth = self.birth_line.text()
        gender = self.box_1.currentText()
        phone = self.phone_line.text()
        email = self.mail_line.text()
        country = self.country_line.text()
        city = self.city_line.text()

        conn = sqlite3.connect("chincho.db")
        curr = conn.cursor()

        curr.execute(f"""INSERT INTO user VALUES('{firstname}','{lastname}','{birth}','{gender}','{phone}','{email}','{country}','{city}')""")

        conn.commit()
        conn.close()

        self.answer_label.setText("User's information has been submitted successfully!")
        self.Green()
        self.Clean_fields()
    
    # define method for delete button:
    def Delete_from_database(self):
        chosen = self.box_2.currentText()
        column_name = self.box_3.currentText()
        record = self.value_line.text()

        conn = sqlite3.connect("chincho.db")
        curr = conn.cursor()

        if chosen == "All Rows":
            curr.execute(f"""DELETE FROM user;""")
            self.answer_label.setText("All rows have been deleted from database, Successfully!")
            self.Green()
        else:
            curr.execute(f"""DELETE FROM user WHERE {column_name} = '{record}';""")
            self.answer_label.setText("Specified row has been deleted from database, Successfully!")
            self.Green()

        conn.commit()
        conn.close()
        self.Clean_fields()
    
    # define method for delete button:
    def Update_Database(self):
        column_name = self.box_4.currentText()
        old_value = self.old_line.text()
        new_value = self.update_line.text()

        conn = sqlite3.connect("chincho.db")
        curr = conn.cursor()

        curr.execute(f"""UPDATE user SET {column_name} = '{new_value}' WHERE {column_name} = '{old_value}';""")
        self.answer_label.setText("Specified record has been updated, Successfully!")
        self.Green()

        conn.commit()
        conn.close()
        self.Clean_fields()


#------------------------------------------- end -------------------------------------- #

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    tyson = MikeTyson()
    sys.exit(app.exec_())