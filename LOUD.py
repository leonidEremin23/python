import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QComboBox, QTextEdit, QMainWindow
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
is_auth = False
con = sqlite3.connect('school.db')
cur = con.cursor()




class Teacher(QWidget):
    def __init__(self, name, spec):
        super().__init__()
        self.is_auth = True
        self.table_name = spec
        self.name = name
        self.is_auth = True
        self.initUI()




    def initUI(self):
        self.resize(818, 410)
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 170, 791, 221))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.mark_field = QtWidgets.QLineEdit(self)
        self.mark_field.setGeometry(QtCore.QRect(540, 50, 211, 21))
        self.mark_field.setObjectName("mark_field")
        self.gogo = QtWidgets.QPushButton(self)
        self.gogo.setGeometry(QtCore.QRect(540, 110, 211, 31))
        self.gogo.setObjectName("gogo")
        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(540, 20, 211, 22))
        self.comboBox.setObjectName("comboBox")
        self.jl = QtWidgets.QPushButton(self)
        self.jl.setGeometry(QtCore.QRect(280, 70, 151, 41))
        self.jl.setText('Просмотреть оценки')
        self.jl.clicked.connect(self.jol)
        self.warning_field = QtWidgets.QLineEdit(self)
        self.warning_field.setGeometry(QtCore.QRect(540, 80, 211, 22))
        self.warning_field.setObjectName("warning_field")
        self.gogo.setText("Выставить")
        self.make_table()
        self.gogo.clicked.connect(self.query_mk)
        self.comboBox.clear()
        self.start_fings()

    def make_table(self):
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["id", "name", "mark", "teacher", "warinings"])

    def start_fings(self):

        query = f"SELECT DISTINCT name FROM {self.table_name}"
        res = cur.execute(query).fetchall()
        for i in res:
            self.comboBox.addItem(i[0])
        self.mark_field.setText('Выставляйте оценку сюда')
        self.warning_field.setText('И примичание сюда')


    def query_mk(self):
        if self.is_auth:
            puple = self.comboBox.currentText()
            mark = self.mark_field.text()
            warning = self.warning_field.text()
            if warning:
                query = f"INSERT INTO {self.table_name}(name, mark, teacher, warning)"
                query += f" VALUES('{puple}',{mark},'{self.name}','{warning}')"
            else:
                query = f"INSERT INTO {self.table_name}(name, mark, teacher)"
                query += f" VALUES('{puple}',{mark},'{self.name}')"
            fe = cur.execute(query)
            con.commit()
            query = f"SELECT * FROM {self.table_name}"
            res = cur.execute(query).fetchall()
            self.tableWidget.setRowCount(len(res))
            for row in range(len(res)):
                element = res[row]
                for col in range(len(element)):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(element[col])))
        else:
            self.lineEdit.setText('ПРОЙДИТЕ')
            self.lineEdit_2.setText('АВТОРИЗАЦИЮ')

    def jol(self):
        if self.is_auth:
            query = f"SELECT * FROM {self.table_name}"
            res = cur.execute(query).fetchall()
            self.tableWidget.setRowCount(len(res))
            for row in range(len(res)):
                element = res[row]
                for col in range(len(element)):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(element[col])))
        else:
            self.lineEdit.setText('ПРОЙДИТЕ')
            self.lineEdit_2.setText('АВТОРИЗАЦИЮ')


class Puple(QWidget):
    def __init__(self, name):
        super().__init__()
        self.is_auth = True
        self.name = name
        self.initUI()


    def initUI(self):
        self.setObjectName("Form")
        self.resize(1000, 500)
        self.tableWidget = QtWidgets.QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(10, 230, 901, 192))
        self.tableWidget.setObjectName("tableWidget")

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(390, 30, 271, 22))
        self.comboBox.setObjectName("comboBox")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(390, 110, 271, 28))
        self.pushButton_2.setObjectName("pushButton_2")
        self.comboBox_2 = QtWidgets.QComboBox(self)
        self.comboBox_2.setGeometry(QtCore.QRect(390, 70, 271, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton_2.setText("Просмотреть")
        self.make_table()
        self.make_combo_boxes()
        self.pushButton_2.clicked.connect(self.make_query)


    def make_combo_boxes(self):
        self.comboBox.addItem('Предмет')
        self.comboBox.addItem('language')
        self.comboBox.addItem('math')
        self.comboBox_2.addItem('Вид записи')
        self.comboBox_2.addItem('Оценка')
        self.comboBox_2.addItem('Замечание')
        self.comboBox_2.addItem('Всё сразу')

    def make_table(self):
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["id", "name", "mark", "teacher", "warinings"])

    def le_try(self):

        query = f"SELECT password, type FROM users WHERE name = '{self.lineEdit.text()}'"
        res = cur.execute(query).fetchall()
        truepswr = res[0][0]
        typeq = res[0][1]
        actualpswrd = self.lineEdit_2.text()
        if truepswr == actualpswrd and typeq == 'puple':
            self.is_auth = True
            self.name = self.lineEdit.text()
            self.lineEdit_2.setText('УСПЕШНО')
        elif typeq == 'puple':
            self.lineEdit.setText('YOUR PASSWORD IS INCORRECT')
        else:
            self.lineEdit.setText('YOUR ARE TEACHER')

    def make_query(self):

        if self.is_auth:
            table_name = self.comboBox.currentText()
            type_of_findings = self.comboBox_2.currentText()
            if type_of_findings == 'Всё сразу':
                type_of_findings = '*'
                self.tableWidget.setColumnCount(5)
                self.tableWidget.setHorizontalHeaderLabels(["id", "name", "mark", "teacher", "warinings"])
                query = f'SELECT * FROM {table_name} WHERE name = "{self.name}"'
            elif type_of_findings == 'Оценка':
                self.tableWidget.setColumnCount(4)
                type_of_findings = 'id, name, mark, teacher'
                self.tableWidget.setHorizontalHeaderLabels(["id", "name", "mark", "teacher"])
                query = f'SELECT id, name, mark, teacher FROM {table_name} WHERE name = "{self.name}"'
            elif type_of_findings == 'Замечание':
                self.tableWidget.setColumnCount(4)
                type_of_findings == 'id, name, teacher, warnings'
                self.tableWidget.setHorizontalHeaderLabels(["id", "name", "teacher", "warinings"])
                query = f'SELECT id, name, teacher, warning FROM {table_name} WHERE name = "{self.name}"'


            res = cur.execute(query).fetchall()
            self.tableWidget.setRowCount(len(res))
            for row in range(len(res)):
                element = res[row]
                for col in range(len(element)):
                    self.tableWidget.setItem(row, col, QTableWidgetItem(str(element[col])))
        else:
            self.lineEdit.setText('ПРОЙДИТЕ')
            self.lineEdit_2.setText('АВТОРИЗАЦИЮ')

class Register(QWidget):
    def __init__(self):
        super().__init__()
        self.is_auth = False
        self.initUI(self)


    def initUI(self, Form):
        Form.setObjectName("Form")
        Form.resize(397, 386)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(10, 160, 381, 91))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 270, 381, 91))
        self.pushButton_2.setObjectName("pushButton_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 80, 191, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 55, 16))
        self.label_2.setObjectName("label_2")
        self.combo = QtWidgets.QComboBox(Form)
        self.combo.setGeometry(QtCore.QRect(10, 30, 191, 21))
        self.make_combo()
        self.pushButton_3 = QtWidgets.QPushButton(Form)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 110, 131, 28))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 55, 16))
        self.label.setObjectName("label")
        self.INFORM = QtWidgets.QLabel(Form)
        self.INFORM.setGeometry(QtCore.QRect(220, 30, 160, 80))
        self.INFORM.setObjectName("INFORM")

        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "JOURNAL"))
        self.pushButton.setText(_translate("Form", "Учительское"))
        self.pushButton_2.setText(_translate("Form", "Ученическое"))
        self.label_2.setText(_translate("Form", "Пароль"))
        self.pushButton_3.setText(_translate("Form", "Авторизоваться"))
        self.label.setText(_translate("Form", "Имя"))
        self.INFORM.setText(_translate("Form", "TextLabel"))
        self.pushButton_3.clicked.connect(self.le_try)
        self.pushButton.clicked.connect(self.teach)
        self.pushButton_2.clicked.connect(self.pupl)
        self.INFORM.setText('ПРОЙДИТЕ АВТОРИЗАЦИЮ')

    def make_combo(self):
        query = f"SELECT name FROM users"
        res = cur.execute(query).fetchall()
        for i in res:
            self.combo.addItem(i[0])
    def teach(self):
        if self.is_auth and self.typeq == 'teacher':
            self.th = Teacher(self.name, self.spec)
            self.th.show()

    def pupl(self):
        if self.is_auth and self.typeq == 'puple':
            self.pl = Puple(self.name)
            self.pl.show()

    def le_try(self):
        query = f"SELECT DISTINCT name FROM users"
        res = cur.execute(query).fetchall()
        flag = True
        if flag:
            query = f"SELECT password, type FROM users WHERE name = '{self.combo.currentText()}'"
            res = cur.execute(query).fetchall()
            truepswr = res[0][0]
            typeq = res[0][1]
            actualpswrd = self.lineEdit_2.text()
            if truepswr == actualpswrd:
                self.is_auth = True
                self.name = self.lineEdit.text()
                self.INFORM.setText('УСПЕШНО')
                query = f"SELECT type FROM users WHERE name = '{self.lineEdit.text()}'"
                res = cur.execute(query).fetchall()
                self.typeq = res[0][0]
                if typeq == 'teacher':
                    query = f"SELECT spec FROM teachers WHERE name = '{self.lineEdit.text()}'"
                    res = cur.execute(query).fetchall()
                    self.spec = res[0][0]
                    print(self.spec)
                    print(self.name)
                    self.INFORM.setText('АВТОРИЗОВАН КАК УЧИТЕЛЬ')
                else:
                    self.INFORM.setText('АВТОРИЗОВАН КАК УЧЕНИК')
            else:
                self.INFORM.setText('НЕВЕРНЫЙ ПАРОЛЬ')
        else:
            self.INFORM.setText('НЕТ ПОЛЬЗОВАТЕЛЯ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Register()
    ex.show()
    sys.exit(app.exec())