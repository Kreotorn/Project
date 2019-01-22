import pyaudio
import time
import threading
import sys
from PIL import Image
from PyQt5.QtGui import QPixmap, QIcon, QFont, QMovie, QPainter, QCursor
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QProgressBar
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtMultimedia import QSound


class App(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('The Seeker of fire')
        self.showFullScreen()

        self.Text = QLabel(self)
        self.book = QLabel(self)
        self.location = QLabel(self)
        self.changed = False

        self.action_targ = QLabel(self)
        self.action_targ.resize(self.width() / 12, 10)
        self.action_targ.move(0, 0)
        self.action_targ.setStyleSheet('QLabel {background-color: Red;'
                                       'border-radius: 5px }')
        self.targ_pos = [(self.width() / 2.17, self.height() / 2.5 - 20),
                         (self.width() / 2.9, self.height() / 2.5 - 20),
                         (self.width() / 1.75, self.height() / 2.5 - 20)]

        self.the_right_answer = [False, False, False]

        self.ur_damage = 10
        self.e_damage = 0
        self.HP_points = 100
        self.eHP_points = 100
        self.result = False

        self.cursor = QCursor(QPixmap('cursor_3.png'))
        self.cursor.pixmap()
        self.setCursor(self.cursor)

        self.skip = QPushButton(self)
        self.skip.resize(100, 20)
        self.skip.move(self.width() / 2 + 180, self.height() / 4 + self.height() / 16 + 20)
        self.skip.setText('SKIP')
        self.skip.setStyleSheet('QPushButton {background-color: rgba(10, 20, 100, 0.2)}'
                                'QPushButton:hover {background-color: Red}')
        self.read = True
        self.skip.clicked.connect(self.next)

        melody = 'DS2.wav'
        self.playable = QSound(melody)
        self.playable.play()

        melody2 = 'in_battle.wav'
        self.playable2 = QSound(melody2)
        self.next_melody = False

        self.movie = QMovie("fire_3.gif")
        self.movie.setScaledSize(QSize(self.width(), self.height()))
        self.movie.frameChanged.connect(self.repaint)
        self.movie.start()

        self.NPC_enemy = QLabel(self)
        self.NPC_enemy.resize(self.height() / 5, self.height() / 5)
        self.NPC_enemy.move(self.width() / 2.3, self.height() / 16)
        self.NPC_enemy.setStyleSheet("QLabel {color: rgb(0, 0, 51);"
                                     'background-color: rgba(10, 20, 100, 0.2);'
                                     'border-color: rgba(100, 100, 100, 0.5);'
                                     'border-style: solid;'
                                     'border-width: 2px;'
                                     '}'
                                     'QLabel:hover {background-color: rgba(100, 0, 0, 0.7)}')

        self.book.resize(self.width() / 3, self.height() / 16)
        self.book.move(self.width() / 3, self.height() / 4 + 40)
        self.book.setStyleSheet("QLabel {background-color: rgba(100, 40, 51, 0.5);"
                                "text-align: center }")
        self.book.setFont(QFont('Times New Roman', 12))

        self.attack = QPushButton(self)
        self.defend = QPushButton(self)
        self.dodge = QPushButton(self)

        self.change_size('attack_proj.png', (int(self.width() / 12), int(self.height() / 4)))
        self.change_size('shield.png', (int(self.width() / 12), int(self.height() / 4)))
        self.change_size('dodging.png', (int(self.width() / 12), int(self.height() / 4)))

        self.attack.setStyleSheet('QPushButton {background-color: rgba(10, 20, 100, 0.2);'
                                  'border-color: rgb(10, 20, 100,);'
                                  'border-style: solid;'
                                  'border-width: 5px;'
                                  'border-radius: 40px;'
                                  'background-image: url(attack_proj.png)'
                                  '}'
                                  'QPushButton:pressed {background-image: url(DS3.jpg)}')
        self.attack.resize(self.width() / 12, self.height() / 4)
        self.attack.move(self.width() / 2.17, self.height() / 2.5)
        self.attack.clicked.connect(self.attack_fnc)

        self.defend.setStyleSheet('QPushButton {background-color: rgba(10, 20, 100, 0.2);'
                                  'border-color: rgb(10, 20, 100,);'
                                  'border-style: solid;'
                                  'border-width: 5px;'
                                  'border-radius: 40px;'
                                  'background-image: url(shield.png)'
                                  '}'
                                  'QPushButton:pressed {background-image: url(DS3.jpg)}')
        self.defend.resize(self.width() / 12, self.height() / 4)
        self.defend.move(self.width() / 2.9, self.height() / 2.5)
        self.defend.clicked.connect(self.defend_fnc)

        self.dodge.setStyleSheet('QPushButton {background-color: rgba(10, 20, 100, 0.2);'
                                 'border-color: rgb(10, 20, 100,);'
                                 'border-style: solid;'
                                 'border-width: 5px;'
                                 'border-radius: 40px;'
                                 'background-image: url(dodging.png)'
                                 '}'
                                 'QPushButton:pressed {background-image: url(DS3.jpg)}')
        self.dodge.resize(self.width() / 12, self.height() / 4)
        self.dodge.move(self.width() / 1.75, self.height() / 2.5)
        self.dodge.clicked.connect(self.dodge_fnc)

        self.Text.move(self.width() / 3, 0)
        self.Text.resize(self.width() / 3, self.height())
        self.Text.move(self.width() / 3, 0)

        self.Text.setStyleSheet("QLabel {color: rgb(0, 0, 51);"
                                'font-family: "Times New Roman", Georgia, Serif;'
                                'font-size: 25px;'
                                'background-color: rgba(10, 20, 100, 0.2);'
                                'border-color: rgb(10, 20, 100,);'
                                'border-style: solid;'
                                'border-width: 5px'
                                '}')
        self.HP = QProgressBar(self)
        self.HP.resize(self.width() / 3, 30)
        self.HP.move(self.width() / 3, self.height() * 0)
        self.HP.setStyleSheet("QProgressBar{border: 1px solid transparent;text-align: center;"
                              "color:rgba(255,255,250,0);"
                              "border-radius: 10px;"
                              "border-width: 8px;"
                              "border-image: 9,2,5,2; "
                              "background-color: Grey;"
                              "}"
                              "QProgressBar::chunk {background-color: qlineargradient(x1: 0, "
                              "y1: 0, x2: 0, y2: 1, stop: 0 rgba(100,80,50,1), stop: 1 rgba(255,0,0,1));"
                              "border-radius: 5px}")
        self.HP.setValue(self.HP_points)

        self.eHP = QProgressBar(self)
        self.eHP.resize(self.width() / 6, 10)
        self.eHP.setStyleSheet("QProgressBar{border: 1px solid transparent;text-align: center;"
                               "color:rgba(255,255,250,0);"
                               "border-radius: 10px;"
                               "border-width: 8px;"
                               "border-image: 9,2,5,2; "
                               "background-color: Grey"
                               "}"
                               "QProgressBar::chunk {background-color: qlineargradient(x1: 0, "
                               "y1: 0, x2: 0, y2: 1, stop: 0 rgba(100,80,50,100), stop: 1 rgba(255,0,0,255));"
                               "border-radius: 5px}")
        self.eHP.move(self.width() / 2.45, self.width() / 6.5)

        self.close_button = QPushButton(self)
        self.close_button.resize(self.width() / 4, self.height() / 20)
        self.close_button.move(self.width() / 3 + self.width() / 24, self.height() / 1.07)
        self.close_button.setStyleSheet('QPushButton {border: 3px solid;'
                                        'border-radius: 10px;'
                                        'background-color: Khaki'
                                        '}'
                                        'QPushButton:pressed{border: 1px solid;'
                                        'border-radius: 40px;'
                                        'background-color: Red'
                                        '}'
                                        'QPushButton:hover{background-color: rgba(255, 0, 0, 40)}')
        self.close_button.clicked.connect(self.close_event)
        self.close_button.setFont(QFont('Times New Roman', 20))
        self.close_button.setText('Выход')

        self.location.resize(self.width() / 3, self.height() / 8)
        self.location.move(self.width() / 3, self.height() / 4)
        self.location.setFont(QFont('Times New Roman', 20))
        self.location.setText('ЗАБРОШЕННЫЕ МОГИЛЫ')
        self.location.setStyleSheet("QLabel {background-color: rgba(250, 40, 51, 0.5);"
                                    "}")
        self.location.setAlignment(Qt.AlignCenter)

        self.game()

    def next(self):
        self.read = False

    def paintEvent(self, event):
        currentframe = self.movie.currentPixmap()
        framerect = currentframe.rect()
        framerect.moveCenter(self.rect().center())
        if framerect.intersects(event.rect()):
            painter = QPainter(self)
            painter.drawPixmap(framerect.left(), framerect.top(), currentframe)

    def close_event(self):
        self.close()

    def game(self):
        dont_stop = threading.Thread(target=self.always_on)
        screen = threading.Thread(target=self.on_screen)
        screen.start()
        dont_stop.start()

    def on_screen(self):
        self.HP.show()
        self.close_button.show()
        self.Text.show()
        self.book.show()
        self.NPC_enemy.show()
        self.skip.show()
        self.attack.show()
        self.defend.show()
        self.dodge.show()
        self.eHP.show()

        self.write('И в самом деле. Замок, что зовётся Лотриком, ')
        self.write('стоит там, где сходятся земли Повелителей пепла. ')
        self.write('Покоряя север, пилигримы убеждаются, что старые сказания не лгут')
        self.write('Огонь затухает, и повелители пепла покидают свои троны')
        self.write('Когда огонь под угрозой, когда звонит колокол,')
        self.write(' Повелители пепла поднимаются из своих могил.')
        self.write('Олдрик, святой покровитель глубин.')
        self.write('Легион нежити Фаррона, Хранители Бездны')
        self.write('И мрачный правитель из осквернённой столицы - гигант Йорм.')
        self.write('Но в действительности... Повелители оставят свои троны, и негорящие восстанут.')
        self.write('Безымянная, проклятая нежить, недостойная стать пеплом.')
        self.write('И стало так. Негорящие всегда ищут угли.')

        self.location.show()
        time.sleep(2)
        self.location.close()

        self.write('Вы поднимаетесь из могилы. В руках у вас ваш меч. ')
        self.write('Вы чётко знате, что будуте делать дальше')
        self.write('Вам предстоит вернуть повелителей на свои троны и спасти ')
        self.write('угасающий мир от погружения во тьму')
        self.write('Перед вами тропа')
        self.write('Пути назад больше нет')
        self.write('...')
        self.write('Вы идете по тропе')

        self.write('Перед вами Полый, нежить, потерявшая рассудок и навеки лишившаяся ')
        self.write('возможности прикоснуться к Огню')
        self.write('Полый достает меч')
        self.write('Приготовьтесь к битве')
        self.write(' ')

        self.NPC_enemy.close()
        self.NPC_enemy.setStyleSheet('QLabel { background-image: url(hollow.jpg)}')
        time.sleep(0.3)
        self.NPC_enemy.show()
        self.next_melody = True
        self.playable.stop()
        # self.eHP.setValue(100)

        self.book.setStyleSheet('QLabel {color: Red }')

        self.the_right_answer = [False, False, True]
        self.write_in_battle('Усиленная атака сверху')
        time.sleep(2)

        if self.result is not True:
            self.write_in_battle('Вы погибли')
            time.sleep(2)
            self.close()
        else:
            self.eHP_points -= 10
            self.eHP.close()
            self.eHP.setValue(self.eHP_points)
            self.eHP.show()
            self.write_in_battle('Вы успешно уклонились')
            self.result = False

        self.the_right_answer = [False, True, False]
        self.write_in_battle('Противник потерял равновесие')
        time.sleep(2)

        if self.result is not True:
            self.write_in_battle('Вы погибли')
            time.sleep(2)
            self.close()
        else:
            self.eHP_points -= 10
            self.eHP.close()
            self.eHP.setValue(self.eHP_points)
            self.eHP.show()
            self.write_in_battle('Вы успешно атаковали')
            self.result = False

        self.the_right_answer = [False, False, True]
        self.write_in_battle('Выпад вперед!')
        time.sleep(1)

        if self.result is not True:
            self.write_in_battle('Вы погибли')
            time.sleep(2)
            self.close()
        else:
            self.eHP_points -= 10
            self.eHP.close()
            self.eHP.setValue(self.eHP_points)
            self.eHP.show()
            self.write_in_battle('Ваш противник в ярости!')
            self.result = False

        self.the_right_answer = [True, False, False]
        self.write_in_battle('Полый нансосит слабый удар')
        time.sleep(1.5)

        if self.result is not True:
            self.write_in_battle('Вы погибли')
            time.sleep(2)
            self.close()
        else:
            self.eHP_points -= 10
            self.eHP.close()
            self.eHP.setValue(self.eHP_points)
            self.eHP.show()
            self.write_in_battle('Щит сломан')
            self.result = False

        self.the_right_answer = [False, True, False]
        self.write_in_battle('Полый выронил меч. Это ваш шанс!')
        victory = False
        time.sleep(0.8)

        if self.result is not True:
            self.write_in_battle('Полый увернулся')
            self.write_in_battle('Вы подбираете его щит')
        else:
            self.eHP_points -= 60
            self.eHP.close()
            self.eHP.setValue(self.eHP_points)
            self.eHP.show()
            self.write_in_battle('Полый побежден!')
            self.result = False
            victory = True

        if victory is False:
            self.the_right_answer = [False, False, True]
            self.write_in_battle('Полый нансосит слабый удар')
            time.sleep(1.5)

            if self.result is not True:
                self.write_in_battle('Вы погибли')
                time.sleep(2)
                self.close()
            else:
                self.eHP_points -= 30
                self.eHP.close()
                self.eHP.setValue(self.eHP_points)
                self.eHP.show()
                self.write_in_battle('Парирование')
                self.result = False

            self.the_right_answer = [False, True, False]
            self.write_in_battle('Полый медленно замахнулся')
            time.sleep(1.5)

            if self.result is not True:
                self.write_in_battle('Вы погибли')
                time.sleep(2)
                self.close()
            else:
                self.eHP_points -= 30
                self.eHP.close()
                self.eHP.setValue(self.eHP_points)
                self.eHP.show()
                self.write_in_battle('Полый сделал шаг назад')
                self.result = False

            self.the_right_answer = [False, True, False]
            self.write_in_battle('Полый поднимает меч')
            time.sleep(1.5)

            if self.result is not True:
                self.write_in_battle('Вы погибли')
                time.sleep(2)
                self.close()
            else:
                self.eHP_points -= 10
                self.eHP.close()
                self.eHP.setValue(self.eHP_points)
                self.eHP.show()
                self.write_in_battle('Полый падает')
                self.result = False

        self.next_melody = False
        self.NPC_enemy.close()
        self.NPC_enemy.setStyleSheet("QLabel {color: rgb(0, 0, 51);"
                                     'background-color: rgba(10, 20, 100, 0.2);'
                                     'border-color: rgba(100, 100, 100, 0.5);'
                                     'border-style: solid;'
                                     'border-width: 2px;'
                                     '}'
                                     'QLabel:hover {background-color: rgba(100, 0, 0, 0.7)}')
        time.sleep(0.3)
        self.NPC_enemy.show()
        self.write('Полый побежден')
        if victory is True:
            self.NPC_enemy.close()
            self.NPC_enemy.setStyleSheet('QLabel { background-image: url(letter.jpg)}')
            time.sleep(0.3)
            self.NPC_enemy.show()
            self.write('Вы получили новый щит: урон противников снижен')
            self.write('Ваш щит сломан: урон противников повышен')
            self.write('Вы продолжаете идти по тропе')
            self.write('Справа от вас труп')
            self.write('В его карамане что-то есть')
            self.write('Найдена записка')
            self.write('С тех времен, как Гвин впервые ')
            self.write('разжег <не разобрать>, минуло много веков и много циклов <не разобрать>')
            self.write('пламени. После того, как он разжег огонь,')
            self.write('этот путь повторили многие великие герои, ')
            self.write('известные как <не разобрать>')

    def always_on(self):
        while True:
            time.sleep(0.5)
            if self.playable.isFinished() is True:
                if self.next_melody is False:
                    self.playable2.stop()
                    self.playable.play()
            if self.playable2.isFinished() is True:
                if self.next_melody is True:
                    self.playable2.play()

    def change_size(self, input_image_path, size=(0, 0)):
        original_image = Image.open(input_image_path)
        resized_image = original_image.resize(size)
        resized_image.save(input_image_path)
        self.changed = True

    def write(self, text):
        your_text = ' '

        for letter in text:
            if self.read is True:
                time.sleep(0.1)
                your_text += letter
                self.book.setText(your_text)
            else:
                self.read = True
                break
        time.sleep(0.2)

    def write_in_battle(self, text):
        your_text = ' '

        for letter in text:
            time.sleep(0.05)
            your_text += letter
            self.book.setText(your_text)

    def defend_fnc(self):
        if self.the_right_answer[0] is True:
            self.result = True
        else:
            self.result = False

        self.action_targ.close()
        self.action_targ.move(self.targ_pos[1][0], self.targ_pos[1][1])
        self.action_targ.show()

    def attack_fnc(self):
        if self.the_right_answer[1] is True:
            self.result = True
        else:
            self.result = False
        self.action_targ.close()
        self.action_targ.move(self.targ_pos[0][0], self.targ_pos[0][1])
        self.action_targ.show()

    def dodge_fnc(self):
        if self.the_right_answer[2] is True:
            self.result = True
        else:
            self.result = False
        self.action_targ.close()
        self.action_targ.move(self.targ_pos[2][0], self.targ_pos[2][1])
        self.action_targ.show()


app = QApplication(sys.argv)
ex = App()
ex.show()
sys.exit(app.exec_())