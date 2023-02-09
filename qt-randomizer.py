from PyQt6 import QtCore, QtWidgets
import random
import sqlite3

import constants

table_name = 'QUESTIONS'
sqlite_connection = sqlite3.connect(
    f'{table_name}.db', check_same_thread=False)

questions = [i + 1 for i in range(constants.number_of_questions)]
seed_questions = [i + 1 for i in range(constants.number_of_questions)] * constants.starting_priority


def rand_question():
    random.shuffle(seed_questions)
    for i in range(len(seed_questions)):
        question = seed_questions[i]
        if (constants.skip_questions_before <= question and question <= constants.skip_questions_after):
            print(f'Next question is {question}.')
            return i
    print('No more non-skipped questions left')
    return -1


def insert_into_db(cursor, question, number):
    sqlite_insert_query = '''INSERT INTO {} (question, number) VALUES ({},\'{}\')'''.format(table_name,
                                                                                            question, number)
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()


def update_in_db(cursor, question, number):
    sqlite_insert_query = f"UPDATE {table_name} SET number = {number} WHERE question = {question};"
    cursor.execute(sqlite_insert_query)
    sqlite_connection.commit()


def get_number_by_question_from_db(cursor, question):
    sqlite_select_query = f"SELECT number FROM {table_name} WHERE question='{question}'"
    res = cursor.execute(sqlite_select_query)
    return res.fetchone()[0]


def add_by_question_in_db(cursor, question, delta):
    res = get_number_by_question_from_db(cursor, question)
    update_in_db(cursor, question, res + delta)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.YesButton = QtWidgets.QPushButton(self.centralwidget)
        self.YesButton.setObjectName("YesButton")
        self.gridLayout_2.addWidget(self.YesButton, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 2, 0, 1, 2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.NoButton = QtWidgets.QPushButton(self.centralwidget)
        self.NoButton.setObjectName("NoButton")
        self.gridLayout_3.addWidget(self.NoButton, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 2, 2, 1, 2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.text = QtWidgets.QLabel(self.centralwidget)
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.text.setObjectName("text")
        self.verticalLayout_2.addWidget(self.text)
        self.gridLayout_4.addLayout(self.verticalLayout_2, 0, 0, 1, 4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.current_question = 1
        self.question_number = QtWidgets.QLabel(self.centralwidget)
        self.question_number.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.question_number.setObjectName("question_number")
        self.verticalLayout.addWidget(self.question_number)
        self.gridLayout_4.addLayout(self.verticalLayout, 1, 0, 1, 4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.SkipButton = QtWidgets.QPushButton(self.centralwidget)
        self.SkipButton.setObjectName("SkipButton")
        self.gridLayout.addWidget(self.SkipButton, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 4, 1, 1, 2)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_5.addWidget(self.widget, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_5, 3, 1, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.set_methods()
        self.current_cursor = sqlite_connection.cursor()
        self.show_question()

    def set_methods(self):
        self.YesButton.clicked.connect(lambda: self.handle_yes())
        self.NoButton.clicked.connect(lambda: self.handle_no())
        self.SkipButton.clicked.connect(lambda: self.handle_skip())
        print("Succesfully constructed main window.")

    def handle_no(self):
        print(f"Update {seed_questions[self.current_question]} by 1")
        add_by_question_in_db(self.current_cursor,
                              seed_questions[self.current_question], 1)
        seed_questions.append(seed_questions[self.current_question])
        self.show_question()

    def handle_yes(self):
        print(f"Update {seed_questions[self.current_question]} by -1")
        add_by_question_in_db(self.current_cursor,
                              seed_questions[self.current_question], -1)
        seed_questions.pop(self.current_question)
        self.show_question()

    def show_question(self):
        _translate = QtCore.QCoreApplication.translate
        self.current_question = rand_question()
        self.question_number.setText(_translate(
            "MainWindow", f"{seed_questions[self.current_question]}"))
        color_number = get_number_by_question_from_db(
            self.current_cursor, seed_questions[self.current_question]) - 1
        if color_number >= len(constants.colors):
            color_number = -1
        MainWindow.setStyleSheet(f"background-color: {constants.colors[color_number]};")

    def handle_skip(self):
        self.show_question()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Randomizer"))
        self.YesButton.setText(_translate("MainWindow", "Yes"))
        self.NoButton.setText(_translate("MainWindow", "No"))
        self.text.setText(_translate("MainWindow", "Your next question is..."))
        self.question_number.setText(_translate(
            "MainWindow", f"{seed_questions[self.current_question]}"))
        self.SkipButton.setText(_translate("MainWindow", "Skip"))

    def __del__(self):
        self.current_cursor.close()


def create_new_table():
    cursor = sqlite_connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

    sqlite_create_table_query = f'''CREATE TABLE {table_name} (
                                question INTEGER,
                                number INTEGER);'''
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    for question in range(constants.number_of_questions):
        insert_into_db(cursor, question + 1, constants.starting_priority)
    sqlite_connection.commit()
    cursor.close()
    global seed_questions
    seed_questions = [i + 1 for i in range(
        constants.number_of_questions)] * constants.starting_priority
    print("Created new database.")


def get_questions_from_db():
    cursor = sqlite_connection.cursor()
    global seed_questions
    seed_questions = []
    for question in range(constants.number_of_questions):
        cur_number = get_number_by_question_from_db(cursor, question + 1)
        seed_questions += [question + 1] * cur_number
    cursor.close()
    print("Loaded questions from existing database.")


def setup_questions():
    cursor = sqlite_connection.cursor()
    # table_name = constants.subject + '-questions'
    existance_check_query = f"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    res = cursor.execute(existance_check_query)
    if res.fetchone()[0] != 1:
        create_new_table()
    else:
        get_questions_from_db()


def create_new_subjects_table():
    cursor = sqlite_connection.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')

    sqlite_create_table_query = f'''CREATE TABLE {table_name} (
                                subject STRING,
                                number_of_questions INTEGER,
                                skip_before INTEGER,
                                skip_after INTEGER);'''
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    cursor.close()
    print("Created new database.")


def insert_subject_into_table(subject, number_of_questions, skip_before, skip_after):
    cursor = sqlite_connection.cursor()
    new_table_name = subject + '_questions'
    existance_check_query = f"SELECT COUNT(name) FROM sqlite_master WHERE type='table' AND name='{new_table_name}';"
    res = cursor.execute(existance_check_query)
    if res.fetchone()[0] == 1:
        return
    sqlite_create_table_query = f'''CREATE TABLE {new_table_name} (
                                question INTEGER,
                                number INTEGER);'''
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    

if __name__ == "__main__":
    # create_new_table()
    import sys
    setup_questions()
    print(f"Number of different questions is {constants.number_of_questions}.")
    print(f"Number of non-skipped questions is {constants.skip_questions_after}.")
    print(f"Total number of questions is {len(seed_questions)}.")
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    exit_code = app.exec()
    sys.exit(exit_code)
