import sys
import math
from PyQt5.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow
from typing import Union, Optional
from operator import add, sub, mul, truediv


class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # нажатие цифер
        self.ui.btn_0.clicked.connect(lambda: self.add_digit('0'))
        self.ui.btn_1.clicked.connect(lambda: self.add_digit('1'))
        self.ui.btn_2.clicked.connect(lambda: self.add_digit('2'))
        self.ui.btn_3.clicked.connect(lambda: self.add_digit('3'))
        self.ui.btn_4.clicked.connect(lambda: self.add_digit('4'))
        self.ui.btn_5.clicked.connect(lambda: self.add_digit('5'))
        self.ui.btn_6.clicked.connect(lambda: self.add_digit('6'))
        self.ui.btn_7.clicked.connect(lambda: self.add_digit('7'))
        self.ui.btn_8.clicked.connect(lambda: self.add_digit('8'))
        self.ui.btn_9.clicked.connect(lambda: self.add_digit('9'))
        # отрицание
        self.ui.b_negative.clicked.connect(self.negative)
        # нажатие с и се
        self.ui.b_c.clicked.connect(self.clear_all)
        self.ui.b_ce.clicked.connect(self.clear_entry)
        self.ui.b_back.clicked.connect(self.backspace)
        # нажатие точки (запятой)
        self.ui.b_point.clicked.connect(self.add_point)
        # обработка событий для lbl_temp
        self.ui.b_plus.clicked.connect(self.add_temp)
        self.ui.b_minus.clicked.connect(self.add_temp)
        self.ui.b_multiply.clicked.connect(self.add_temp)
        self.ui.b_divide.clicked.connect(self.add_temp)
        self.ui.b_deg.clicked.connect(self.add_temp)
        self.ui.b_deg_2.clicked.connect(self.add_temp)
        self.ui.b_sqrt.clicked.connect(self.add_temp)
        self.ui.b_rt.clicked.connect(self.add_temp)
        self.ui.b_equal.clicked.connect(self.add_temp_equal)

    def add_digit(self, btn_text: str) -> None:
        '''
        Добавление цифр в le_entry
        :param btn_text: нажатая кнопка
        :return: None
        '''
        if self.ui.le_entry.text() == '0':
            self.ui.le_entry.setText(btn_text)
            self.adjust_entry_font_size()
        else:
            self.ui.le_entry.setText(self.ui.le_entry.text() + btn_text)
            self.adjust_entry_font_size()
        self.clear_temp_if_equality()

    def clear_all(self) -> None:
        '''
        Отчистка le_entry и lbl_temp
        :return: None
        '''
        self.ui.le_entry.setText('0')
        self.adjust_entry_font_size()
        self.ui.lbl_temp.clear()
        self.change_able_buttons(False)

    def clear_entry(self) -> None:
        '''
        Отчистка только поля результата le_entry
        :return: None
        '''
        self.ui.le_entry.setText('0')
        self.adjust_entry_font_size()

    def backspace(self) -> None:
        entry = self.ui.le_entry.text()
        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.ui.le_entry.setText('0')
                self.adjust_entry_font_size()
            else:
                self.ui.le_entry.setText(entry[:-1])
                self.adjust_entry_font_size()
        else:
            self.ui.le_entry.setText('0')
            self.adjust_entry_font_size()

    def add_point(self) -> None:
        '''
        Добавление точки - вещественных чисел
        :return: None
        '''
        if '.' not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')
            self.adjust_entry_font_size()
            self.clear_temp_if_equality()

    def add_temp(self) -> None:
        '''
        Временное выражение lbl_temp
        :return: None
        '''
        btn = self.sender()
        # обрезка незначащих нулей
        temp = self.ui.lbl_temp.text()
        entry = self.remove_trailing_zeros(self.ui.le_entry.text())
        if not temp or temp[-1] == '=':
            if btn == self.ui.b_deg:
                self.ui.lbl_temp.setText(entry + ' ^ ')
                self.ui.le_entry.setText('0')
                self.adjust_entry_font_size()
                self.adjust_temp_font_size()
            elif btn == self.ui.b_deg_2:
                self.ui.lbl_temp.setText(entry + ' ^ ')
                self.ui.le_entry.setText('2')
                self.adjust_entry_font_size()
                self.adjust_temp_font_size()
            elif btn == self.ui.b_sqrt:  # !!!!
                self.ui.lbl_temp.setText(f'sqrt({entry})')
                self.ui.le_entry.setText('0')
                self.adjust_entry_font_size()
                self.adjust_temp_font_size()
            elif btn == self.ui.b_rt:
                self.ui.lbl_temp.setText(f'rt({entry},')
                self.ui.le_entry.setText('0')
                self.adjust_entry_font_size()
                self.adjust_temp_font_size()
            else:
                self.ui.lbl_temp.setText(entry + f' {btn.text()} ')
                self.ui.le_entry.setText('0')
                self.adjust_entry_font_size()
                self.adjust_temp_font_size()
        else:  # Смена знака
            if btn == self.ui.b_deg:
                if temp[-2] == '^' and entry == '2':
                    self.ui.le_entry.setText('0')
                    self.adjust_entry_font_size()
                elif temp[-2] != '^':
                    if temp[0] == 's':
                        new_temp = f'{temp[5:-1]} ^ '
                    elif temp[0] == 'r':
                        new_temp = f'{temp[3:-1]} ^ '
                    else:
                        new_temp = f'{temp[:-2]} ^ '
                    self.ui.lbl_temp.setText(new_temp)
                    self.adjust_temp_font_size()
            elif btn == self.ui.b_deg_2:
                if temp[0] == 's':
                    new_temp = f'{temp[5:-1]} ^ '
                elif temp[0] == 'r':
                    new_temp = f'{temp[3:-1]} ^ '
                else:
                    new_temp = f'{temp[:-2]}^ '
                self.ui.le_entry.setText('2')
                self.adjust_entry_font_size()
                self.ui.lbl_temp.setText(new_temp)
                self.adjust_temp_font_size()
            elif btn == self.ui.b_sqrt:
                new_temp = temp
                if temp[-2] == '^':
                    new_temp = f'sqrt({temp[:-3]})'
                elif temp[0] == 'r':
                    new_temp = f'sqrt({temp[3:-1]})'
                elif temp[0] != 's':
                    new_temp = f'sqrt({temp[:-3]})'
                self.ui.lbl_temp.setText(new_temp)
                self.ui.le_entry.setText('0')
                self.adjust_entry_font_size()
                self.adjust_temp_font_size()
            elif btn == self.ui.b_rt:
                new_temp = temp
                if temp[-2] == '^':
                    new_temp = f'rt({temp[:-3]},'
                elif temp[0] == 's':
                    new_temp = f'rt({temp[5:-1]},'
                elif temp[0] != 'r':
                    new_temp = f'rt({temp[:-3]},'
                self.ui.lbl_temp.setText(new_temp)
                self.adjust_temp_font_size()
            else:
                if temp[0] == 's':
                    new_temp = f'{temp[5:-1]} {btn.text()} '
                elif temp[0] == 'r':
                    new_temp = f'{temp[3:-1]} {btn.text()} '
                else:
                    new_temp = f'{temp[:-3]} {btn.text()} '
                self.ui.lbl_temp.setText(new_temp)
                self.adjust_temp_font_size()

    def add_temp_equal(self) -> None:
        temp = self.ui.lbl_temp.text()
        entry = self.remove_trailing_zeros(self.ui.le_entry.text())
        if temp:
            try:
                if temp[-2] == '^':
                    a = float(temp[:-3])
                    b = float(entry)
                    c = self.remove_trailing_zeros(pow(a, b))
                    self.ui.lbl_temp.setText(temp + entry + ' =')
                    self.ui.le_entry.setText(str(c))
                    self.adjust_entry_font_size()
                    self.adjust_temp_font_size()
                elif temp[0] == 's':
                    a = float(temp[5:-1])
                    c = self.remove_trailing_zeros(math.sqrt(a))
                    self.ui.lbl_temp.setText(temp + ' =')
                    self.ui.le_entry.setText(str(c))
                    self.adjust_entry_font_size()
                    self.adjust_temp_font_size()
                elif temp[0] == 'r':
                    a = float(temp[3:-1])
                    b = 1 / float(entry)
                    c = self.remove_trailing_zeros(pow(a, b))
                    self.ui.lbl_temp.setText(temp + ' ' + entry + ') =')
                    self.ui.le_entry.setText(str(c))
                    self.adjust_entry_font_size()
                    self.adjust_temp_font_size()
                else:
                    operations = {
                        '+': add,
                        '-': sub,
                        '*': mul,
                        '/': truediv
                    }
                    a = float(temp[:-3])
                    b = float(entry)
                    self.ui.lbl_temp.setText(temp + entry + ' =')
                    self.adjust_temp_font_size()
                    if b == 0 and temp[-2:-1] == '/':
                        self.ui.le_entry.setText("смешно (жми C)")
                        self.adjust_entry_font_size()
                        self.change_able_buttons(True)
                    else:
                        c = self.remove_trailing_zeros(operations[temp[-2:-1]](a, b))
                        self.ui.le_entry.setText(str(c))
                        self.adjust_entry_font_size()
            except:
                pass

    @staticmethod
    def remove_trailing_zeros(num: str) -> str:
        '''
        Удаление незначащих нулей
        :param num: число из le_entry
        :return: str(num) без нулей после запятой
        '''
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    def negative(self) -> None:
        self.clear_temp_if_equality()
        entry = self.ui.le_entry.text()
        if '-' not in entry:
            if entry != '0':
                entry = '-' + entry
        else:
            entry = entry[1:]
        max_entry = self.ui.le_entry.maxLength()
        if len(entry) == max_entry + 1 and '-' in entry:
            self.ui.le_entry.setMaxLength(max_entry + 1)
        else:
            self.ui.le_entry.setMaxLength(max_entry)
        self.ui.le_entry.setText(entry)
        self.adjust_entry_font_size()

    def clear_temp_if_equality(self) -> None:
        '''
        Удаляем lbl_temp когда после равенства нажата любая кнопка
        :return:
        '''
        temp = self.ui.lbl_temp.text()
        if len(temp) > 0:
            if temp[-1] == '=':
                self.ui.lbl_temp.clear()

    def change_able_buttons(self, flag) -> None:
        self.ui.b_back.setDisabled(flag)
        self.ui.b_ce.setDisabled(flag)
        self.ui.b_deg.setDisabled(flag)
        self.ui.b_deg_2.setDisabled(flag)
        self.ui.b_divide.setDisabled(flag)
        self.ui.b_equal.setDisabled(flag)
        self.ui.b_minus.setDisabled(flag)
        self.ui.b_multiply.setDisabled(flag)
        self.ui.b_negative.setDisabled(flag)
        self.ui.b_plus.setDisabled(flag)
        self.ui.b_point.setDisabled(flag)
        self.ui.b_rt.setDisabled(flag)
        self.ui.b_sqrt.setDisabled(flag)
        self.ui.btn_0.setDisabled(flag)
        self.ui.btn_1.setDisabled(flag)
        self.ui.btn_2.setDisabled(flag)
        self.ui.btn_3.setDisabled(flag)
        self.ui.btn_4.setDisabled(flag)
        self.ui.btn_5.setDisabled(flag)
        self.ui.btn_6.setDisabled(flag)
        self.ui.btn_7.setDisabled(flag)
        self.ui.btn_8.setDisabled(flag)
        self.ui.btn_9.setDisabled(flag)

    def get_entry_text_width(self) -> int:
        # le_entry ширина текста в пикселях
        return self.ui.le_entry.fontMetrics().boundingRect(
            self.ui.le_entry.text()).width()

    def get_temp_text_width(self) -> int:
        # lbl_temp ширина текста в пикселях
        return self.ui.lbl_temp.fontMetrics().boundingRect(
            self.ui.lbl_temp.text()).width()

    def resizeEvent(self, event) -> None:
        self.adjust_entry_font_size()
        self.adjust_temp_font_size()

    def adjust_entry_font_size(self) -> None:
        # уменьшение
        font_size = default_entry_font_size
        while self.get_entry_text_width() > self.ui.le_entry.width() - 5:
            font_size -= 1
            self.ui.le_entry.setStyleSheet('font-size: ' + str(font_size) + 'pt; border: none;')
        # увеличение
        font_size = 1
        while self.get_entry_text_width() < self.ui.le_entry.width() - 20:
            font_size += 1
            if font_size > default_entry_font_size:
                break
            self.ui.le_entry.setStyleSheet(
                'font-size: ' + str(font_size) + 'pt; border: none;')

    def adjust_temp_font_size(self) -> None:
        font_size = default_font_size
        while self.get_temp_text_width() > self.ui.lbl_temp.width() - 10:
            font_size -= 1
            self.ui.lbl_temp.setStyleSheet(
                'font-size: ' + str(font_size) + 'pt; color: #666;')
        font_size = 1
        while self.get_temp_text_width() < self.ui.lbl_temp.width() - 60:
            font_size += 1
            if font_size > default_font_size:
                break
            self.ui.lbl_temp.setStyleSheet(
                'font-size: ' + str(font_size) + 'pt; color: #666;')


if __name__ == "__main__":
    default_font_size = 14
    default_entry_font_size = 40
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
