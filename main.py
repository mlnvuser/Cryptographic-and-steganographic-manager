from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from form import Ui_MainWindow as interface
from secondary import Window
import sys, os, pyAesCrypt, datetime, zipfile, threading

class My_Window(Window):
    '''Главное окно программы'''

    def __init__(self):
        super(My_Window, self).__init__()
        self.ui = interface()  # Работа с импортированным классом будет происходить с помощью данной переменной;
        self.ui.setupUi(self)  # Вызвали метод в котором создано графическое окно;
        self.setWindowTitle('Шифратор')  # Изменили название окна;
        self.setWindowIcon(QtGui.QIcon('images/ico.ico'))
        self.ui.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)  # Метод, скрывающий пароль звёздочками;
        self.functions = {0:'Шифрование', 1:'Дешифрование', 2:'Стеганография', 3:'Стегоанализ', 4:'Настройки'}
        self.functions_copy = {'Шифрование':0, 'Дешифрование':1, 'Стеганография':2, 'Стегоанализ':3,
                               'Настройки':4}
        self.functions_icons = {'Шифрование':'images/encrypt.png', 'Дешифрование':'images/decrypt.png',
                                'Стеганография':'images/stegan.png', 'Стегоанализ':'images/generate.png',
                                'Генерация ключей':'images/settings.png'}
        self.cwd = os.getcwd()
        self.i = 0
        self.files_lw2 = {}
        self.files_lw3 = {}
        self.files_lw4 = {}
        self.settings = self.read_settings()

        self.ui.tabWidget.currentChanged.connect(self.tabChanged)
        self.ui.listWidget.currentRowChanged.connect(self.selected_listwidget_element)
        self.ui.lineEdit.textChanged.connect(self.filter)

        self.ui.pushButton.clicked.connect(lambda: self.browse_for_select_file(self.ui.lineEdit_12, 'directory'))
        self.ui.pushButton_2.clicked.connect(lambda: self.click_generation_password(self.ui.lineEdit_3))
        self.ui.pushButton_3.clicked.connect(lambda: self.browse_for_select_file(self.ui.lineEdit_3, 'key'))
        self.ui.pushButton_4.clicked.connect(lambda: self.browse_for_select_file(self.ui.listWidget_2, 'files'))
        self.ui.pushButton_5.clicked.connect(lambda: self.show_pass(self.ui.lineEdit_5))
        self.ui.pushButton_6.clicked.connect(self.click_okay)
        self.ui.pushButton_7.clicked.connect(self.closeEvent)
        self.ui.pushButton_8.clicked.connect(lambda: self.browse_for_select_file(self.ui.lineEdit_5, 'key'))
        self.ui.pushButton_9.clicked.connect(lambda: self.browse_for_select_file(self.ui.listWidget_3, 'files'))
        self.ui.pushButton_10.clicked.connect(lambda: self.browse_for_select_file(self.ui.lineEdit_7, 'directory'))
        self.ui.pushButton_11.clicked.connect(lambda: self.browse_for_select_file(self.ui.listWidget_4, 'files'))
        self.ui.pushButton_12.clicked.connect(lambda: self.browse_for_select_file(self.ui.lineEdit_13, 'directory'))
        self.ui.pushButton_13.clicked.connect(lambda: self.browse_for_select_file(self.ui.lineEdit_9, 'file'))
        self.ui.pushButton_14.clicked.connect(lambda: self.browse_for_select_file(self.ui.lineEdit_2, 'file'))
        self.ui.pushButton_15.clicked.connect(lambda: self.browse_for_select_file(self.ui.lineEdit_10, 'directory'))



    #Обратное стеганографическое преобразование
    def destegan(self, path, photo):
        '''Обратное стеганографическое преобразование'''
        try:
            with open(fr"{path}\{datetime.datetime.now().strftime('%d-%m-%Y %H-%M-%S')}.zip",
                      'wb') as f, open(photo,'rb') as s:  # Первый файл - создаваемый архив с данными на запись их в него; Второй файл - изображение;
                f.write(s.read())  # Записать в файл f стеганографическое содержимое файла s;
        except:
            self.display_result(self.ui.label_18,
                                'red', 'Ошибка обратного стеганографического преобразования!', 5, button=self.ui.pushButton_6)
        else:
            self.clear_form(self.ui.lineEdit_2, self.ui.lineEdit_10)
            self.display_result(self.ui.label_18,
                                'green', 'Преобразование успешно!', 5, button=self.ui.pushButton_6)


    #Стеганографическое преобразовние
    def stegan(self, files, photo):
        '''Стеганографическое преобразование'''

        try:
            with zipfile.ZipFile(r'temp/files.zip',
                                 'w') as zf:  # Создаём пустой архив в папке с временными файлами;
                for i in files:
                    zf.write(filename=i, arcname=files[i])  # Добавляем в архив выбранные файлы;
        except:
            self.display_result(self.ui.label_14,
                                'red', 'Ошибка создания архива с файлами!', 5, button=self.ui.pushButton_6)
        else:
            try:
                with open(photo, 'ab') as f, open(r'temp/files.zip','rb') as s:  # Первый файл - изображение; Второй файл - архив с данными;
                    f.write(s.read())  # Дополнить файл f содержимым файла s;
            except:
                self.display_result(self.ui.label_14,
                                    'red', 'Ошибка стеганографического преобразования!', 5, button=self.ui.pushButton_6)
            else:
                self.clear_form(self.ui.lineEdit_9, self.ui.listWidget_4)
                self.display_result(self.ui.label_14,
                                    'green', 'Преобразование успешно!', 5, button=self.ui.pushButton_6)


    #Функция поток для криптографии
    def crypt(self, crypt, files, path, key, button = False):
        '''Функция-поток для криптографии'''

        if button:
            button.setEnabled(False)
        try:
            if crypt == 'encrypt':
                for i in files:
                    pyAesCrypt.encryptFile(i, path + fr"\{self.rename_file_name(files[i], mode='encrypt')}", key)
            elif crypt == 'decrypt':
                for i in files:
                    pyAesCrypt.decryptFile(i, path + fr"\{self.rename_file_name(files[i], mode='decrypt')}", key)
        except:
            if crypt == 'encrypt':
                self.display_result(self.ui.label_5,
                                    'red', 'Ошибка при попытке операции!',
                                    5, button=self.ui.pushButton_6)
            elif crypt == 'decrypt':
                self.display_result(self.ui.label_10,
                                    'red', 'Ошибка при попытке операции!',
                                    5, button=self.ui.pushButton_6)
        else:
            self.clear_form(self.ui.lineEdit_3, self.ui.lineEdit_12,
                            self.ui.listWidget_2)
            if crypt == 'encrypt':
                self.display_result(self.ui.label_5,
                                'green', 'Операция выполнена!', 5,
                                button=self.ui.pushButton_6)
            elif crypt == 'decrypt':
                self.display_result(self.ui.label_10,
                                    'green', 'Операция выполнена!', 5,
                                    button=self.ui.pushButton_6)


    #При выполнении программы
    def click_okay(self):
        '''При нажатии на кнопку - окей'''

        if self.ui.tabWidget.currentIndex() == 0: #Если выбрана вкладка - шифрование файлов;
            if len(self.ui.lineEdit_3.text()) == 0: #Если поле ввода пустое;
                self.display_result(self.ui.label_5,
                                    'red','Введите ключ шифрования!',
                                    5, button=self.ui.pushButton_6, lineedit=self.ui.lineEdit_3)
            else:
                if len(self.ui.lineEdit_3.text()) < 8: #Если длина пароля меньше 8 символов;
                    self.display_result(self.ui.label_5,
                                        'red', 'Введите надежный пароль!',5, button=self.ui.pushButton_6, lineedit=self.ui.lineEdit_3)
                else:
                    if self.ui.listWidget_2.count() == 0: #Если в listwidget нет выбранных файлов;
                        self.display_result(self.ui.label_5,
                                            'red', 'Выберите файл(ы)!',5, button=self.ui.pushButton_6)
                    else:
                        if len(self.ui.lineEdit_12.text()) == 0 and len(self.ui.lineEdit_13.text()) == 0: #Если локально и в настройках не выбран путь сохранения
                            self.display_result(self.ui.label_5,
                                                'red', 'Выберите путь сохранения!', 5,
                                                button=self.ui.pushButton_6, lineedit=self.ui.lineEdit_12)
                        else:
                            if len(self.ui.lineEdit_12.text()) == 0:
                                path = self.ui.lineEdit_13.text()
                            else:
                                path = self.ui.lineEdit_12.text()

                            if self.ui.checkBox.isChecked(): #Если в настройках отмечено сохранять ключи шифрования;
                                try:
                                    with open(f'keys/key ({datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")}).txt',
                                              'w') as f:
                                        f.write(self.ui.lineEdit_3.text())
                                except:
                                    self.display_result(self.ui.label_5,
                                                        'red', 'Ошибка при сохранении ключа шифрования!', 5,
                                                        button=self.ui.pushButton_6)
                                else:
                                    p = threading.Thread(target=self.crypt,
                                                             args=('encrypt',self.files_lw2,path,
                                                                   self.ui.lineEdit_3.text(), self.ui.pushButton_6))  # Запуск функции-потока с передачей параметров;
                                    p.start()


        elif self.ui.tabWidget.currentIndex() == 1: #Если выбрана вкладка - дешифрование файлов;
            if len(self.ui.lineEdit_5.text()) == 0:  #Если поле ввода пустое;
                self.display_result(self.ui.label_10,
                                    'red', 'Введите ключ дешифрования или выберите файл с ключом!',
                                    5, button=self.ui.pushButton_6, lineedit=self.ui.lineEdit_5)
            else:
                if self.ui.listWidget_3.count() == 0:  # Если в listwidget нет выбранных файлов для дешифрования;
                    self.display_result(self.ui.label_10,
                                        'red', 'Выберите файл(ы) для дешифрования!', 5, button=self.ui.pushButton_6)
                else:
                    if len(self.ui.lineEdit_7.text()) == 0 and len(self.ui.lineEdit_13.text()) == 0:  # Если не выбран путь сохранения;
                        self.display_result(self.ui.label_10,
                                            'red', 'Выберите путь сохранения!', 5, button=self.ui.pushButton_6, lineedit=self.ui.lineEdit_7)
                    else:
                        if len(self.ui.lineEdit_7.text()) == 0:
                            path = self.ui.lineEdit_13.text()
                        else:
                            path = self.ui.lineEdit_7.text()
                        p = threading.Thread(target=self.crypt,
                                             args=('decrypt', self.files_lw3, path,
                                                   self.ui.lineEdit_5.text(),
                                                   self.ui.pushButton_6))  # Запуск функции-потока с передачей параметров;
                        p.start()


        elif self.ui.tabWidget.currentIndex() == 2:
            if self.ui.listWidget_4.count() == 0:  # Если в listwidget нет выбранных файлов;
                self.display_result(self.ui.label_14,
                                    'red', 'Выберите файл(ы)!', 5, button=self.ui.pushButton_6)
            else:
                if len(self.ui.lineEdit_9.text()) == 0:  # Если поле ввода пустое;
                    self.display_result(self.ui.label_14,
                                        'red', 'Выберите файл, куда необходимо спрятать!',
                                        5, button=self.ui.pushButton_6, lineedit=self.ui.lineEdit_9)
                else:
                    p = threading.Thread(target=self.stegan,args=(self.files_lw4,self.ui.lineEdit_9.text()))  # Запуск функции-потока с передачей параметров;
                    p.start()


        elif self.ui.tabWidget.currentIndex() == 3:
            if len(self.ui.lineEdit_2.text()) == 0:  # Если поле ввода пустое;
                self.display_result(self.ui.label_18,
                                    'red', 'Выберите файл!',
                                    5, button=self.ui.pushButton_6,lineedit=self.ui.lineEdit_2)
            else:
                if len(self.ui.lineEdit_10.text()) == 0 and len(self.ui.lineEdit_13.text()) == 0:  # Если поле ввода пустое;
                    self.display_result(self.ui.label_18,
                                        'red', 'Выберите путь сохранения!',
                                        5, button=self.ui.pushButton_6,lineedit=self.ui.lineEdit_10)
                else:
                    if len(self.ui.lineEdit_10.text()) == 0:
                        path = self.ui.lineEdit_13.text()
                    else:
                        path = self.ui.lineEdit_10.text()
                    p = threading.Thread(target=self.destegan, args=(
                    path,self.ui.lineEdit_2.text()))  # Запуск функции-потока с передачей параметров;
                    p.start()


        elif self.ui.tabWidget.currentIndex() == 4:
            try:
                self.save_settings()
            except:
                self.display_result(self.ui.label_13,
                                    'red', 'Ошибка сохранения!',
                                    5, button=self.ui.pushButton_6)
            else:
                self.display_result(self.ui.label_13,
                                    'green', 'Сохранение выполнено!',
                                    5, button=self.ui.pushButton_6)





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = My_Window()
    application.setStyleSheet("#MainWindow{border-image:url(images/background2.jpg)}")
    application.show()

    sys.exit(app.exec())