from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from QtUi.window_editor import Ui_window_editor as UIM
import pygame
from Node.director import Director

pygame.init()



class NewMainWindow(UIM):
    def __init__(self):
        super(NewMainWindow, self).__init__()
        self.setupUi(MainWindow)

    def setup(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = NewMainWindow()
    ui.setup()
    MainWindow.show()
    sys.exit(app.exec_())



