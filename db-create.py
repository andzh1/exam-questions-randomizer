import sqlite3

table_name = 'Subjects.db'
sqlite_connection = sqlite3.connect(
    f'{table_name}', check_same_thread=False)


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
    # setup_questions()
    # print(f"Number of different questions is {constants.number_of_questions}.")
    # print(f"Number of non-skipped questions is {constants.skip_questions_after}.")
    # print(f"Total number of questions is {len(seed_questions)}.")
    # app = QtWidgets.QApplication(sys.argv)
    # MainWindow = QtWidgets.QMainWindow()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    # MainWindow.show()
    # exit_code = app.exec()
    # sys.exit(exit_code)
