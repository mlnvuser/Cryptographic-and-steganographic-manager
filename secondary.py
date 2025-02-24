from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys, random,time, threading, ast, traceback, os

class Window(QtWidgets.QMainWindow):
    '''Основные методы для окна программы'''


    # Сохраняет настройки программы в файл
    def save_settings(self):
        '''Сохраняет настройки программы при закрытии'''

        settings = {'save_key': self.ui.checkBox.isChecked(), 'default_path': self.ui.lineEdit_13.text()}

        with open(f'Settings.txt', 'w') as f:
            f.write(str(settings))


    # Считывает сохраненные настройки
    def read_settings(self):
        '''Считывает сохраненные настройки программы'''

        try:
            with open('Settings.txt') as f:
                text = f.read().split('\n')
                settings = ast.literal_eval(text[0].lstrip().rstrip()) # словарь с настройками;
        except:
            pass
        else:
            self.ui.checkBox.setChecked(settings['save_key']) # установили значение как в файле настройки- > сохранять ключи?
            self.ui.lineEdit_13.setText(settings['default_path'])
            return settings


    # Изменение вкладки при выборе элемента списка
    def selected_listwidget_element(self):
        '''При выборе элемента liswidget будет меняться tabwidget'''

        try:
            self.ui.tabWidget.setCurrentIndex(self.functions_copy[self.ui.listWidget.currentItem().text()])
        except:
            pass


    # Изменение главного текста в зависимости от выбранной вкладки
    def tabChanged(self, index):  # +++ index
        '''Изменили текст главного labl'a в зависимости от выбранного элемента tab'widget'''

        self.ui.label.setText(self.functions[self.ui.tabWidget.currentIndex()])


    # Показ и скрытие пароля
    def show_pass(self, lineedit):
        '''Показать пароль'''

        if self.i % 2 == 0:
            lineedit.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            lineedit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.i += 1


    # Генерация надежного пароля
    def click_generation_password(self, lineedit):
        '''При нажатии на кнопку генерации пароля'''

        letters = 'abcdefghijklmnopqrstuvwxyz'
        big_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        numbers = '1234567890'
        symbols = '!@#$%^&*()-+'
        general = [letters, big_letters, numbers, symbols]
        password = ''
        password += random.choice(letters)
        password += random.choice(big_letters)
        password += random.choice(numbers)
        password += random.choice(symbols)
        while len(password) < 32:
            password += random.choice(general[random.randint(0, 3)])
        lineedit.setText(password)


    # При выборе файлов
    def browse_for_select_file(self, obj, mode):
        """При нажатии на кнопку выбора файла(ов)"""

        if mode == 'file':
            fileName_choose, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", self.cwd,
                                                                              "All Files (*);;Text Files (*.txt)")  # Установить фильтр расширений файлов, через двойную ";;"

            if fileName_choose == "":
                print("Отменить выбор")
                return

            s = ''
            for i in fileName_choose:
                if i == '/':
                    s += '\\'
                else:
                    s += i
            obj.setText(s)

        elif mode == 'files':
            filesName_choose, filetype = QtWidgets.QFileDialog.getOpenFileNames(self, "Выбрать файлы", self.cwd)

            if filesName_choose == "":
                print("Отменить выбор")
                return

            files = {}
            for i in filesName_choose:
                s = ''
                for j in i:
                    if j == '/':
                        s += '\\'
                    else:
                        s += j
                files.update({s: self.file_name(s)})
            obj.clear()
            for i in files:
                self.add_file_to_listwidget(obj, self.file_name(i), self.select_icon(self.file_name(i)))
            if obj == self.ui.listWidget_2:
                self.files_lw2 = files
            elif obj == self.ui.listWidget_3:
                self.files_lw3 = files
            elif obj == self.ui.listWidget_4:
                self.files_lw4 = files

        elif mode == 'directory':
            destDir = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                 'Выбрать директорию',
                                                                 self.cwd)
            s = ''
            for i in destDir:
                if i == '/':
                    s += '\\'
                else:
                    s += i
            obj.setText(s)

        elif mode == 'key':
            fileName_choose, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "Выбрать файл", self.cwd,
                                                                              "Text Files (*.txt)")  # Установить фильтр расширений файлов, через двойную ";;"

            if fileName_choose == "":
                print("Отменить выбор")
                return

            s = ''
            for i in fileName_choose:
                if i == '/':
                    s += '\\'
                else:
                    s += i
            basename, extension = os.path.splitext(self.file_name(s))
            if extension != '.txt':
                self.display_result(self.ui.label_5,
                                    'red', 'Выберите файл формата .txt!',
                                    5, button=self.ui.pushButton_3)
            else:
                try:
                    with open(s) as f:
                        key = f.read().split('\n')
                        key = key[0].lstrip().rstrip()  # убрали отступы слева и справа;
                except:
                    self.display_result(self.ui.label_5,
                                        'red', 'Ошибка открытия файла с ключом!',
                                        5, button=self.ui.pushButton_3)
                else:
                    obj.setText(key)


    # Изменит имя шифруемого или дешифруемого файлов
    def rename_file_name(self, file_name, mode):
        '''Изменит имя файла'''

        basename, extension = os.path.splitext(file_name)

        if mode == 'encrypt':
            return f'{basename} (e){extension}'
        elif mode == 'decrypt':
            return f'{basename} (d){extension}'


    # Вернёт имя файла с расширением
    def file_name(self, path):
        '''Получает путь к файлу - возвращает имя файла с расширением'''

        name = ''
        for i in path[::-1]:
            if i != '\\':
                name += i
            else:
                return name[::-1]


    # Добавляет название файла в список
    def add_file_to_listwidget(self, listwidget, file_name, icon_path):
        '''Добавляет название файла в рабочее поле'''

        item = QtWidgets.QListWidgetItem()  # Создать объект QListWidgetItem
        item.setIcon(QtGui.QIcon(icon_path))
        item.setText(file_name)
        listwidget.addItem(item)


    # Вернёт путь к необходимой иконке
    def select_icon(self, name):
        "Возвращает путь к необходимой иконке"

        s = ''
        for i in name[::-1]:
            if i == '.':
                break
            else:
                s += i
        s = s[::-1].lower()
        if s == 'txt':
            path = "icons/txt.png"
        elif s == 'xls' or s == 'xlsx':
            path = "icons/excel.png"
        elif s == 'exe':
            path = "icons/exe.png"
        elif s == 'png' or s == 'jpg':
            path = "icons/jpg.png"
        elif s == 'pdf':
            path = "icons/pdf.png"
        elif s == 'ppt':
            path = "icons/powerpoint.png"
        elif s == 'txt':
            path = "icons/txt.png"
        elif s == 'doc' or s == 'docx':
            path = "icons/word.png"
        elif s == 'rar' or s == 'zip':
            path = "icons/archive.png"
        else:
            path = "icons/file.png"
        return path


    # При изменении текста в поле поиска
    def filter(self, input_text):
        '''При изменении текста в поле поиска'''

        self.ui.listWidget.clearSelection()  # Снять выделение с объекта listwidget
        if len(self.ui.lineEdit.text()) == 0:  # Если в поле поиска ничего нет
            self.ui.listWidget.clear()  # Очищаем элементы listwidget'a
            for i in self.functions_icons:
                item = QtWidgets.QListWidgetItem()  # Создать объект QListWidgetItem
                item.setIcon(QtGui.QIcon(self.functions_icons[i]))
                item.setText(i)
                self.ui.listWidget.addItem(item)  # Добавляем все сохраненные элементы в listwidget
        else:
            self.ui.listWidget.clear()
            for i in self.functions_copy:
                if input_text.lower() in i.lower():
                    item = QtWidgets.QListWidgetItem()  # Создать объект QListWidgetItem
                    item.setIcon(QtGui.QIcon(self.functions_icons[i]))
                    item.setText(i)
                    self.ui.listWidget.addItem(item)


    # Отобразит результат выполнения программы
    def display_result(self, label, color, text, sec, button=False, lineedit=False):
        '''Отобразить результат выполнения программы'''

        def result(label, t):
            '''Функция-поток'''

            time.sleep(t)  # 5сек.
            label.setText('')  # Убрать текст результата преобразования;
            if button:
                button.setEnabled(True)
            if lineedit:
                lineedit.setStyleSheet("border: 1px solid #000000; font: 12pt Georgia")

        label.setStyleSheet(f"color: {color}; font: 10pt Georgia")
        label.setText(text)
        if lineedit:
            lineedit.setStyleSheet("border: 1px solid #ff0000; font: 12pt Georgia")
        if button:
            button.setEnabled(False)
        p = threading.Thread(target=result,
                             args=(label, sec))  # Запуск функции-потока с передачей параметров;
        p.start()


    # Очистка форм ввода
    def clear_form(self, *objects):
        '''Функция очистки форм для записи'''

        for i in objects:
            try:
                i.setText('')
            except:
                try:
                    i.clear()
                except:
                    pass


    #При закрытии программы
    def closeEvent(self, event):
        '''При закрытии приложения'''

        reply = QtWidgets.QMessageBox.question(self, 'Выход!?', "Вы действительно хотите выйти?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                event.accept()
                self.save_settings()
            except:
                sys.exit()
        else:
            try:
                event.ignore()
            except:
                pass

