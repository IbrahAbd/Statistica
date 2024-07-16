import sys
import time
from OPGGparser import *
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self) 

        champ = "Jhin" 

        start_time = time.time()
        rates = output(champ)
        end_time = time.time()
        elapsed_time = end_time - start_time

        role = rates['role']
        font = QtGui.QFont()
        font.setPointSize(40)  
        
        pixmap = QPixmap(f'Roles\{role}.png')
        self.roleIMG.setPixmap(pixmap)
        self.roleIMG.setPixmap(pixmap.scaled(self.roleIMG.size(), aspectRatioMode=True))
        self.roleIMG.resize(pixmap.width(), pixmap.height())

        self.display_image(f'Images\{champ}.png')

        if (champ.find(" ") == False):
            champName = champ.split(" ")
            champ = champName[0] + " " + champName[1]
            print(champ)

        self.name.setText(champ)
        self.name.setFont(font)

        sumSpell1 = rates['SumSpell1'][0]
        sumSpell2 = rates['SumSpell2'][0]

        pixmapSpell1 = QPixmap(f'SummonerSpells\{sumSpell1}.png')
        self.Summoner1.setPixmap(pixmapSpell1)
        self.Summoner1.setPixmap(pixmapSpell1.scaled(self.Summoner1.size(), aspectRatioMode=True))
        self.Summoner1.resize(pixmapSpell1.width(), pixmapSpell1.height())

        pixmapSpell2 = QPixmap(f'SummonerSpells\{sumSpell2}.png')
        self.Summoner2.setPixmap(pixmapSpell2)
        self.Summoner2.setPixmap(pixmapSpell2.scaled(self.Summoner2.size(), aspectRatioMode=True))
        self.Summoner2.resize(pixmapSpell2.width(), pixmapSpell2.height())

        font2 = QtGui.QFont()
        font2.setPointSize(20)  

        self.WinRate.setText("Win rate: " + rates['win_rate'])
        self.WinRate.setFont(font2)
        self.WinRate.setStyleSheet("color: green;")

        self.BanRate.setText("Ban rate: " + rates['ban_rate'])
        self.BanRate.setFont(font2)
        self.BanRate.setStyleSheet("color: red;")

        self.PickRate.setText("Pick rate: " + rates['pick_rate'])
        self.PickRate.setFont(font2)

        self.role.setText(role)
        self.role.setFont(font2)

        #pixmapMainRune = QPixmap(f'SummonerSpells\{sumSpell2}.png')
        #self.Summoner2.setPixmap(pixmapMainRune)
        #self.Summoner2.setPixmap(pixmapMainRune.scaled(self.Summoner2.size(), aspectRatioMode=True))
        #self.Summoner2.resize(pixmapMainRune.width(), pixmapMainRune.height())


        print(f"Elapsed time: {elapsed_time} seconds\n")

    def display_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            
            self.label.setPixmap(scaled_pixmap)
            self.label.setAlignment(QtCore.Qt.AlignCenter) 
        else:
            print(f"Error: Unable to load image from {image_path}")

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())