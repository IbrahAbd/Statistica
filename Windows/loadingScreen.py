import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout,QMainWindow,QDialog
import sys
import os
import random
from PyQt5 import QtWidgets, QtGui

class MainWindow3(QtWidgets.QMainWindow):
    def __init__(self, gif_folder):
        super().__init__()
        uic.loadUi('loadingScreen.ui', self)
        self.gif_folder = gif_folder
        self.display_random_gif()

    def display_random_gif(self):
        gif_files = [f for f in os.listdir(self.gif_folder) if f.endswith('.gif')]
        if gif_files:
            random_gif = random.choice(gif_files)
            gif_path = os.path.join(self.gif_folder, random_gif)
            self.movie = QtGui.QMovie(gif_path)
            self.gif.setMovie(self.movie)
            self.movie.start()
        else:
            self.gif.setText("No GIFs found in the specified folder")
