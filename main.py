import sys
import sqlite3

from design import Ui_MainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Browser(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.connection = sqlite3.connect("base111.db")
        self.setupUi(self)
        self.SeekBtn.clicked.connect(self.seek)
        self.action.triggered.connect(self.open_thirdwindow)
        self.second_window = None
        self.third_window = None
        self.res = self.connection.cursor().execute('''SELECT name, year, genre, about, developer FROM Games 
        ''').fetchall()
        self.fill(self.res)

    def seek(self):
        if self.GameInput.text() == '':
            Game_input = 'like' + ' ' + '"' + '%' + '"'
        else:
            Game_input = '=' + ' ' + '"' + self.GameInput.text() + '"'
        if self.YearInput.text().isdigit():
            Year_input = '=' + ' ' + self.YearInput.text()
        else:
            Year_input = '>' + ' ' + '1'
        if self.GenreInput.text() == '':
            Genre_input = 'like' + ' ' + '"' + '%' + '"'
        else:
            Genre_input = '=' + ' ' + '"' + self.GenreInput.text() + '"'
        if self.DeveloperInput.text() == '':
            Developer_input = 'like' + ' ' + '"' + '%' + '"'
        else:
            Developer_input = '=' + ' ' + '"' + self.DeveloperInput.text() + '"'
        self.res = self.connection.cursor().execute('''SELECT name, year, genre, about, developer FROM Games
                                            WHERE name {} and year {} and genre {} and developer {}
                                            '''.format(Game_input, Year_input, Genre_input, Developer_input)).fetchall()
        self.fill(self.res)

    def createCellWidget(self, text, btn):
        layout = QGridLayout()
        frame = QFrame()
        frame.setLayout(layout)
        layout.addWidget(QLabel(text), 0, 0)
        btn = QPushButton(btn)
        btn.clicked.connect(self.open_secondwindow)
        layout.addWidget(btn, 1, 0)
        return frame

    def fill(self, res):
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setColumnWidth(0, 120)
        self.tableWidget.setColumnWidth(1, 50)
        self.tableWidget.setColumnWidth(2, 90)
        self.tableWidget.setColumnWidth(3, 230)
        self.tableWidget.setColumnWidth(4, 120)
        self.tableWidget.setColumnWidth(5, 300)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            self.tableWidget.setRowHeight(i, 120)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
            widget = self.createCellWidget('Подробнее:', row[j - 4])
            self.tableWidget.setCellWidget(
                i, 5, widget)

    def open_secondwindow(self):
        wtgame = self.sender().text()
        self.second_window = MsgBox(wtgame, self)
        self.second_window.show()

    def open_thirdwindow(self):
        self.third_window = MyConfig()
        self.third_window.show()


class MyConfig(QWidget):
    def __init__(self):
        super().__init__()
        self.CardsList2 = None
        self.CpusList2 = None
        self.connection = sqlite3.connect("base111.db")
        self.user_cfg = self.connection.cursor().execute('''SELECT * FROM Config
        ''').fetchall()
        self.cpu = None
        self.card = None
        self.space = None
        self.space1 = None
        self.opspace = None
        self.setWindowTitle('Ваша Конфигурация')
        self.setFixedSize(600, 250)
        self.connection = sqlite3.connect("base111.db")
        self.mycpu = QLabel('Процессор:', self)
        self.mycpu.setAlignment(Qt.AlignTop)
        self.mycpu.move(20, 20)
        self.mycpu.resize(100, 30)
        self.mycpu.setFont(QFont('Arial', 12))

        self.mycpu_input = QLineEdit(self)
        self.mycpu_input.move(130, 20)
        self.mycpu_input.resize(200, 20)
        self.mycpu_input.setEnabled(False)

        self.mycard = QLabel('Видеокарта:', self)
        self.mycard.setAlignment(Qt.AlignTop)
        self.mycard.move(20, 60)
        self.mycard.resize(100, 30)
        self.mycard.setFont(QFont('Arial', 12))

        self.mycard_input = QLineEdit(self)
        self.mycard_input.move(130, 60)
        self.mycard_input.resize(200, 20)
        self.mycard_input.setEnabled(False)
        self.myspace = QLabel('Свободное место:', self)
        self.myspace.setAlignment(Qt.AlignTop)
        self.myspace.move(20, 100)
        self.myspace.resize(200, 30)
        self.myspace.setFont(QFont('Arial', 12))

        self.myspace_input = QLineEdit(self)
        self.myspace_input.move(160, 100)
        self.myspace_input.resize(40, 20)
        self.myspace_input.setEnabled(False)
        self.combobox1 = QComboBox(self)
        self.combobox1.move(210, 100)
        self.combobox1.resize(50, 20)
        self.combobox1.setFont(QFont('Arial', 10))
        self.combobox1.addItems(['ГБ', 'ТБ', 'МБ'])
        self.combobox1.setEnabled(False)

        self.myopspace = QLabel('Оперативная память:', self)
        self.myopspace.setAlignment(Qt.AlignTop)
        self.myopspace.move(20, 140)
        self.myopspace.resize(200, 30)
        self.myopspace.setFont(QFont('Arial', 12))

        self.myopspace_input = QLineEdit(self)
        self.myopspace_input.move(182, 140)
        self.myopspace_input.resize(50, 20)
        self.myopspace_input.setEnabled(False)

        self.myopspace2 = QLabel('ГБ', self)
        self.myopspace2.resize(20, 20)
        self.myopspace2.move(240, 140)
        self.myopspace2.setFont(QFont('Arial', 10))

        self.savebtn = QPushButton('Сохранить', self)
        self.savebtn.resize(90, 30)
        self.savebtn.move(300, 190)

        self.editbtn = QPushButton('Редактировать', self)
        self.editbtn.resize(90, 30)
        self.editbtn.move(200, 190)
        self.editbtn.clicked.connect(self.Edit)

        self.dialog = QMessageBox(self)
        self.dialog.setWindowTitle('Ошибка!')
        if self.user_cfg[0][1]:
            self.mycpu_input.setText(self.user_cfg[0][1])
        else:
            self.mycpu_input.setText('?')

        if self.user_cfg[0][2]:
            self.mycard_input.setText(self.user_cfg[0][2])
        else:
            self.mycard_input.setText('?')

        if self.user_cfg[0][3]:
            self.myspace_input.setText(str(self.user_cfg[0][3]))
        else:
            self.myspace_input.setText('?')

        if self.user_cfg[0][5]:
            self.myopspace_input.setText(str(self.user_cfg[0][5]))
        else:
            self.myopspace_input.setText('?')

    def Save(self):
        self.connection.cursor().execute('''UPDATE Config SET cpu = "{}" 
        WHERE id = 1 '''.format(self.cpu))
        self.connection.cursor().execute('''UPDATE Config SET card = "{}" 
        WHERE id = 1 '''.format(self.card))
        self.connection.cursor().execute('''UPDATE Config SET space = {} 
        WHERE id = 1 '''.format(self.space))
        self.connection.cursor().execute('''UPDATE Config SET space_1 = "{}" 
        WHERE id = 1 '''.format(self.space1))
        self.connection.cursor().execute('''UPDATE Config SET op_space = {} 
        WHERE id = 1 '''.format(self.opspace))
        self.connection.commit()
        self.user_cfg = self.connection.cursor().execute('''SELECT * FROM Config''').fetchall()
        self.mycpu_input.setEnabled(False)
        self.mycard_input.setEnabled(False)
        self.myspace_input.setEnabled(False)
        self.combobox1.setEnabled(False)
        self.myopspace_input.setEnabled(False)

    def fill(self):
        count = 0
        if self.mycpu_input.text() in self.CpusList2:
            self.cpu = self.mycpu_input.text()
            count += 1
        elif self.mycpu_input.text() == '':
            self.dialog.setText('Не введено значение - процессор.')
            self.dialog.show()
        else:
            self.dialog.setText('Такого процессора не существует.')
            self.dialog.show()
        if self.mycard_input.text() in self.CardsList2:
            self.card = self.mycard_input.text()
            count += 1
        elif self.mycard_input.text() == '':
            self.dialog.setText('Не введено значение - видеокарта.')
            self.dialog.show()
        else:
            self.dialog.setText('Такой видеокарты не существует.')
            self.dialog.show()
        if self.myspace_input.text().isdigit():
            self.space = self.myspace_input.text()
            count += 1
        elif self.myspace_input.text() == '':
            self.dialog.setText('Не введено значение - свободное место.')
            self.dialog.show()
        else:
            self.dialog.setText('Значение(свободное место) должно быть числом.')
            self.dialog.show()
        self.space1 = self.combobox1.currentText()
        if self.myopspace_input.text().isdigit():
            self.opspace = self.myopspace_input.text()
            count += 1
        elif self.myopspace_input.text() == '':
            self.dialog.setText('Не введено значение - оперативная память.')
            self.dialog.show()
        else:
            self.dialog.setText('Значение(оперативная память) должно быть числом.')
            self.dialog.show()
        if count == 4:
            self.Save()

    def Edit(self):
        self.mycpu_input.setEnabled(True)
        self.mycard_input.setEnabled(True)
        self.myspace_input.setEnabled(True)
        self.combobox1.setEnabled(True)
        self.myopspace_input.setEnabled(True)
        CpusList = self.connection.cursor().execute('''SELECT name FROM Cpus''').fetchall()
        CardsList = self.connection.cursor().execute('''SELECT name FROM Gcards''').fetchall()
        self.CpusList2 = []
        self.CardsList2 = []
        for i in CpusList:
            for j in i:
                if j != '':
                    self.CpusList2.append(j)
        for i in CardsList:
            for j in i:
                if j != '':
                    self.CardsList2.append(j)
        completer1 = QCompleter(self.CpusList2, self.mycpu_input)
        completer1.setCaseSensitivity(False)
        self.mycpu_input.setCompleter(completer1)
        completer2 = QCompleter(self.CardsList2, self.mycard_input)
        completer2.setCaseSensitivity(False)
        self.mycard_input.setCompleter(completer2)
        self.savebtn.clicked.connect(self.fill)


class MsgBox(QWidget):
    def __init__(self, wtgame, parent=None):
        super().__init__()
        self.pixmap2 = None
        self.pixmap1 = None
        self.space_pow = None
        self.opspace_pow = None
        self.card_pow = None
        self.cpu_pow = None
        self.spacecomp = None
        self.opspacecomp = None
        self.cardcomp = None
        self.cpucomp = None
        self.yourspace = None
        self.youropspace = None
        self.yourcard = None
        self.yourcpu = None
        self.space_req_pow = None
        self.space_req = None
        self.opspace_req_pow = None
        self.opspace_req = None
        self.card_req_pow = None
        self.card_req = None
        self.cpu_req = None
        self.cpu_req_pow = None
        self.connection = sqlite3.connect("base111.db")
        self.user_cfg = self.connection.cursor().execute('''SELECT * FROM Config''').fetchall()
        self.wtgame = wtgame
        self.setWindowTitle(self.wtgame)
        self.setFixedSize(900, 900)
        self.move(100, 100)
        self.pixmap = QPixmap('C:/Users/makss/PycharmProjects/pythonProject/photos/{}.jpg'.format(self.wtgame))
        self.image = QLabel(self)
        self.image.setScaledContents(True)
        self.image.move(30, 100)
        self.image.resize(300, 400)
        self.image.setPixmap(self.pixmap)
        self.GameInfo = self.connection.cursor().execute('''SELECT * FROM Games 
                                          WHERE name = "{}" '''.format(self.wtgame)).fetchall()
        self.GameName = QLabel(self.GameInfo[0][1], self)
        self.GameName.setAlignment(Qt.AlignCenter)
        self.GameName.setFont(QFont('Arial', 16))
        self.GameName.resize(400, 100)
        self.GameName.move(250, 10)
        self.GameYear = QLabel('Год выпуска: {}'.format(self.GameInfo[0][2]), self)
        self.GameYear.resize(400, 50)
        self.GameYear.move(350, 110)
        self.GameYear.setFont(QFont('Arial', 12))
        self.GameGenre = QLabel('Жанр: {}'.format(self.GameInfo[0][3]), self)
        self.GameGenre.resize(400, 50)
        self.GameGenre.move(350, 140)
        self.GameGenre.setFont(QFont('Arial', 12))
        self.GameDeveloper = QLabel('Разработчик: {}'.format(self.GameInfo[0][5]), self)
        self.GameDeveloper.resize(400, 50)
        self.GameDeveloper.move(350, 170)
        self.GameDeveloper.setFont(QFont('Arial', 12))
        self.GameAbout = QLabel('Описание: {}'.format(self.GameInfo[0][4]), self)
        self.GameAbout.resize(500, 400)
        self.GameAbout.move(350, 230)
        self.GameAbout.setFont(QFont('Arial', 12))
        self.GameAbout.setWordWrap(True)
        self.GameAbout.setAlignment(Qt.AlignTop)
        self.yoursys = QLabel('Ваша система:', self)
        self.yoursys.setFont(QFont('Arial', 15))
        self.yoursys.resize(200, 100)
        self.yoursys.move(100, 520)
        self.yoursys.setAlignment(Qt.AlignLeft)
        self.sysreqlabel = QLabel('Системные Требования:', self)
        self.sysreqlabel.setFont(QFont('Arial', 15))
        self.sysreqlabel.resize(300, 100)
        self.sysreqlabel.move(550, 520)
        self.sysreqlabel.setAlignment(Qt.AlignLeft)
        self.game_req()
        self.yourconfig()
        self.comparisonreq()

    def game_req(self):
        cpu = self.connection.cursor().execute('''SELECT name FROM Cpus
                                                  WHERE power = {} '''.format(self.GameInfo[0][6])).fetchall()
        card = self.connection.cursor().execute('''SELECT name FROM GCards
                                                  WHERE power = {} '''.format(self.GameInfo[0][7])).fetchall()
        self.cpu_req = QLabel(f'Процессор: {cpu[0][0]}', self)
        self.cpu_req.move(570, 560)
        self.cpu_req.resize(240, 60)
        self.cpu_req.setFont(QFont('Arial', 10))
        self.cpu_req.setAlignment(Qt.AlignLeft)
        self.cpu_req_pow = self.GameInfo[0][6]
        self.card_req = QLabel(f'Видеокарта: {card[0][0]}', self)
        self.card_req.move(570, 590)
        self.card_req.resize(260, 60)
        self.card_req.setFont(QFont('Arial', 10))
        self.card_req.setAlignment(Qt.AlignLeft)
        self.card_req_pow = self.GameInfo[0][7]
        self.opspace_req = QLabel(f'Оперативная память: {self.GameInfo[0][9]} ГБ', self)
        self.opspace_req.move(570, 620)
        self.opspace_req.resize(240, 60)
        self.opspace_req.setFont(QFont('Arial', 10))
        self.opspace_req.setAlignment(Qt.AlignLeft)
        self.opspace_req_pow = self.GameInfo[0][9]
        self.space_req = QLabel(f'Место на жёстком диске: {self.GameInfo[0][8]} ГБ', self)
        self.space_req.move(570, 650)
        self.space_req.resize(320, 60)
        self.space_req.setFont(QFont('Arial', 10))
        self.space_req.setAlignment(Qt.AlignLeft)
        self.space_req_pow = self.GameInfo[0][8]

    def yourconfig(self):
        if self.user_cfg[0][1]:
            self.yourcpu = QLabel(f'Процессор: {self.user_cfg[0][1]}', self)
            self.yourcpu.move(120, 560)
            self.yourcpu.resize(260, 60)
            self.yourcpu.setFont(QFont('Arial', 10))
            self.yourcpu.setAlignment(Qt.AlignLeft)
        else:
            self.yourcpu = QLabel('Процессор: ?', self)
            self.yourcpu.move(120, 560)
            self.yourcpu.resize(260, 60)
            self.yourcpu.setFont(QFont('Arial', 10))
            self.yourcpu.setAlignment(Qt.AlignLeft)
        if self.user_cfg[0][2]:
            self.yourcard = QLabel(f'Видеокарта: {self.user_cfg[0][2]}', self)
            self.yourcard.move(120, 590)
            self.yourcard.resize(280, 60)
            self.yourcard.setFont(QFont('Arial', 10))
            self.yourcard.setAlignment(Qt.AlignLeft)
        else:
            self.yourcard = QLabel('Видеокарта: ?', self)
            self.yourcard.move(120, 590)
            self.yourcard.resize(260, 60)
            self.yourcard.setFont(QFont('Arial', 10))
            self.yourcard.setAlignment(Qt.AlignLeft)
        if self.user_cfg[0][3]:
            self.youropspace = QLabel(f'Оперативная память: {self.user_cfg[0][5]} ГБ', self)
            self.youropspace.move(120, 620)
            self.youropspace.resize(260, 60)
            self.youropspace.setFont(QFont('Arial', 10))
            self.youropspace.setAlignment(Qt.AlignLeft)
        else:
            self.youropspace = QLabel('Оперативная память: ?', self)
            self.youropspace.move(120, 620)
            self.youropspace.resize(260, 60)
            self.youropspace.setFont(QFont('Arial', 10))
            self.youropspace.setAlignment(Qt.AlignLeft)
        if self.user_cfg[0][5]:
            self.yourspace = QLabel(f'Место на жёстком диске: {self.user_cfg[0][3]} {self.user_cfg[0][4]}', self)
            self.yourspace.move(120, 650)
            self.yourspace.resize(260, 60)
            self.yourspace.setFont(QFont('Arial', 10))
            self.yourspace.setAlignment(Qt.AlignLeft)
        else:
            self.yourspace = QLabel('Место на жёстком диске: ?', self)
            self.yourspace.move(120, 650)
            self.yourspace.resize(260, 60)
            self.yourspace.setFont(QFont('Arial', 10))
            self.yourspace.setAlignment(Qt.AlignLeft)

    def comparisonreq(self):
        self.cpucomp = QLabel(self)
        self.cpucomp.move(530, 550)
        self.cpucomp.resize(30, 30)
        self.cpucomp.setFont(QFont('Arial', 10))
        self.cpucomp.setAlignment(Qt.AlignCenter)
        self.cpucomp.setAlignment(Qt.AlignTop)
        self.cpucomp.setScaledContents(True)
        self.cardcomp = QLabel(self)
        self.cardcomp.move(530, 580)
        self.cardcomp.resize(30, 30)
        self.cardcomp.setFont(QFont('Arial', 10))
        self.cardcomp.setAlignment(Qt.AlignCenter)
        self.cardcomp.setAlignment(Qt.AlignTop)
        self.cardcomp.setScaledContents(True)
        self.opspacecomp = QLabel(self)
        self.opspacecomp.move(530, 610)
        self.opspacecomp.resize(30, 30)
        self.opspacecomp.setFont(QFont('Arial', 10))
        self.opspacecomp.setAlignment(Qt.AlignCenter)
        self.opspacecomp.setAlignment(Qt.AlignTop)
        self.opspacecomp.setScaledContents(True)
        self.spacecomp = QLabel(self)
        self.spacecomp.move(530, 640)
        self.spacecomp.resize(30, 30)
        self.spacecomp.setFont(QFont('Arial', 10))
        self.spacecomp.setAlignment(Qt.AlignCenter)
        self.spacecomp.setAlignment(Qt.AlignTop)
        self.spacecomp.setScaledContents(True)
        if self.user_cfg[0][1]:
            self.cpu_pow = self.connection.cursor().execute('''SELECT power FROM Cpus 
                                                        WHERE name = "{}" '''.format(self.user_cfg[0][1])).fetchone()
            self.cpu_pow = self.cpu_pow[0]
        if self.user_cfg[0][2]:
            self.card_pow = self.connection.cursor().execute('''SELECT power FROM Gcards 
                                                        WHERE name = "{}" '''.format(self.user_cfg[0][2])).fetchone()
            self.card_pow = self.card_pow[0]
        if self.user_cfg[0][5]:
            self.opspace_pow = self.user_cfg[0][5]
        if self.user_cfg[0][3]:
            if self.user_cfg[0][4] == 'ТБ':
                self.space_pow = self.user_cfg[0][3] * 1000
            elif self.user_cfg[0][4] == 'ГБ':
                self.space_pow = self.user_cfg[0][3]
            else:
                self.space_pow = self.user_cfg[0][3] / 1000
        self.pixmap1 = QPixmap('+.png')
        self.pixmap2 = QPixmap('-.png')
        if self.user_cfg[0][1]:
            if int(self.cpu_pow) >= int(self.cpu_req_pow):
                self.cpucomp.setPixmap(self.pixmap1)
            else:
                self.cpucomp.setPixmap(self.pixmap2)
        if self.user_cfg[0][2]:
            if int(self.card_pow) >= int(self.card_req_pow):
                self.cardcomp.setPixmap(self.pixmap1)
            else:
                self.cardcomp.setPixmap(self.pixmap2)
        if self.user_cfg[0][5]:
            if int(self.opspace_pow) >= int(self.opspace_req_pow):
                self.opspacecomp.setPixmap(self.pixmap1)
            else:
                self.opspacecomp.setPixmap(self.pixmap2)
        if self.user_cfg[0][3]:
            if int(self.space_pow) >= int(self.space_req_pow):
                self.spacecomp.setPixmap(self.pixmap1)
            else:
                self.spacecomp.setPixmap(self.pixmap2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Browser()
    ex.show()
    sys.exit(app.exec())
