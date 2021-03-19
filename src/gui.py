#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from encoder_decoder import *
import cipher
from cryptography.fernet import Fernet
from random import randint


def write_key():
    key = Fernet.generate_key()
    with open('crypto_key', 'wb') as key_file:
        key_file.write(key)


def load_key():
    return open('crypto_key', 'rb').read()


class Gui(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.encode_msg)
        self.ui.pushButton_2.clicked.connect(self.open_file)
        self.ui.pushButton_3.clicked.connect(self.encode_file)
        self.rand = None
        self.value = 100
        self.key = load_key()
        self.file_path = ''

    def open_file(self):
        self.file_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file')[0]
        self.ui.lineEdit_2.setText(str(self.file_path))

    def encode_msg(self):
        f = Fernet(self.key)
        if self.ui.encoder.isChecked():
            if self.ui.lineEdit != '':
                text = self.ui.lineEdit.text()
                with open('message.txt', 'w') as msg_file:
                    msg_file.write(text)
                with open('message.txt', 'rb') as msg_file:
                    message_file = msg_file.read()
                    encrypted_data = f.encrypt(message_file)
                with open('message.txt', 'wb') as file:
                    file.write(encrypted_data)
                self.ui.plainTextEdit.setPlainText(f'Шифрование прошло успешно: {text}\n'
                                                   f'{str(encrypted_data)}')
            self.ui.lineEdit.setText(' ')

        if self.ui.decoder.isChecked():
            with open('message.txt', 'rb') as msg_file:
                encrypted_data = msg_file.read()
            decrypted_data = f.decrypt(encrypted_data)
            with open('message.txt', 'wb') as msg_file:
                msg_file.write(decrypted_data)
            self.ui.plainTextEdit.setPlainText(f'Сообщение расшифровано: {str(encrypted_data)}\n'
                                               f'{decrypted_data.decode("utf-8")}')

    def encode_file(self):
        f = Fernet(self.key)
        if self.ui.encoder.isChecked():
            with open(self.file_path, 'r') as file:
                read_file = file.read()
            with open(self.file_path, 'rb') as file:
                file_data = file.read()
                encrypted_data = f.encrypt(file_data)
            with open(self.file_path, 'wb') as file:
                file.write(encrypted_data)
            self.ui.plainTextEdit.setPlainText(f'Шифрование прошло успешно: \nБыло:    {read_file}\n'
                                               f'Стало:    {str(encrypted_data)}')
        self.ui.lineEdit_2.setText(' ')

        if self.ui.decoder.isChecked():
            with open(self.file_path, 'rb') as msg_file:
                encrypted_data = msg_file.read()
            decrypted_data = f.decrypt(encrypted_data)
            with open(self.file_path, 'wb') as msg_file:
                msg_file.write(decrypted_data)
            self.ui.plainTextEdit.setPlainText(f'Сообщение расшифровано:\nБыло:    {str(encrypted_data)}\n'
                                               f'Стало:    {decrypted_data.decode("utf-8")}')


if __name__ == '__main__':
    # cipher.write_key()
    app = QtWidgets.QApplication(sys.argv)
    myapp = Gui()
    myapp.show()
    sys.exit(app.exec_())
