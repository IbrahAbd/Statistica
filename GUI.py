import sys
import time
from OPGGparser import *
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap

#TODO: Get hover text working for runes
#TODO: Change backround colour
#TODO: Add champion abilities and passive with hovering working.


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self) 

        champ = "Zeri" 

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


        rune1 = rates['MainRuneName']
        rune2 = rates['SecondaryRuneName']
        primaryRune = rates['MainPrimaryRune'].replace(" ", "")
        runes = rates['MinorRunes']


        pixmapMainRune = QPixmap(f'Runes\{rune1}\{primaryRune}.png')
        self.MainRune.setPixmap(pixmapMainRune)
        self.MainRune.setPixmap(pixmapMainRune.scaled(self.MainRune.size(), aspectRatioMode=True))
        self.MainRune.resize(pixmapMainRune.width(), pixmapMainRune.height())

        pixmapSecondaryRune = QPixmap(f'Runes\{rune2}.png')
        self.SecondaryRune.setPixmap(pixmapSecondaryRune)
        self.SecondaryRune.setPixmap(pixmapSecondaryRune.scaled(self.SecondaryRune.size(), aspectRatioMode=True))
        self.SecondaryRune.resize(pixmapSecondaryRune.width(), pixmapSecondaryRune.height())

        pixmapPrimaryRune1 = QPixmap(f'Runes\{rune1}\{runes[0]}.png')
        self.MainRune1.setPixmap(pixmapPrimaryRune1)
        self.MainRune1.setPixmap(pixmapPrimaryRune1.scaled(self.MainRune1.size(), aspectRatioMode=True))
        self.MainRune1.resize(pixmapPrimaryRune1.width(), pixmapPrimaryRune1.height())

        
        pixmapPrimaryRune2 = QPixmap(f'Runes\{rune1}\{runes[1]}.png')
        self.MainRune2.setPixmap(pixmapPrimaryRune2)
        self.MainRune2.setPixmap(pixmapPrimaryRune2.scaled(self.MainRune2.size(), aspectRatioMode=True))
        self.MainRune2.resize(pixmapPrimaryRune2.width(), pixmapPrimaryRune2.height())

        
        pixmapPrimaryRune3 = QPixmap(f'Runes\{rune1}\{runes[2]}.png')
        self.MainRune3.setPixmap(pixmapPrimaryRune3)
        self.MainRune3.setPixmap(pixmapPrimaryRune3.scaled(self.MainRune3.size(), aspectRatioMode=True))
        self.MainRune3.resize(pixmapPrimaryRune3.width(), pixmapPrimaryRune3.height())


        pixmapSecondaryRune1 = QPixmap(f'Runes\{rune2}\{runes[3]}.png')
        self.SecondaryRune1.setPixmap(pixmapSecondaryRune1)
        self.SecondaryRune1.setPixmap(pixmapSecondaryRune1.scaled(self.SecondaryRune1.size(), aspectRatioMode=True))
        self.SecondaryRune1.resize(pixmapSecondaryRune1.width(), pixmapSecondaryRune1.height())

        pixmapSecondaryRune2 = QPixmap(f'Runes\{rune2}\{runes[4]}.png')
        self.SecondaryRune2.setPixmap(pixmapSecondaryRune2)
        self.SecondaryRune2.setPixmap(pixmapSecondaryRune2.scaled(self.SecondaryRune2.size(), aspectRatioMode=True))
        self.SecondaryRune2.resize(pixmapSecondaryRune2.width(), pixmapSecondaryRune2.height())

        shards = rates['Shards']
        pixmapShard1 = QPixmap(f'Runes\{shards[0]}.png')
        self.minorRune1.setPixmap(pixmapShard1)
        self.minorRune1.setPixmap(pixmapShard1.scaled(self.minorRune1.size(), aspectRatioMode=True))
        self.minorRune1.resize(pixmapShard1.width(), pixmapShard1.height())


        pixmapShard2 = QPixmap(f'Runes\{shards[1]}.png')
        self.minorRune2.setPixmap(pixmapShard2)
        self.minorRune2.setPixmap(pixmapShard2.scaled(self.minorRune2.size(), aspectRatioMode=True))
        self.minorRune2.resize(pixmapShard2.width(), pixmapShard2.height())

        pixmapShard3 = QPixmap(f'Runes\{shards[2]}.png')
        self.minorRune3.setPixmap(pixmapShard3)
        self.minorRune3.setPixmap(pixmapShard3.scaled(self.minorRune3.size(), aspectRatioMode=True))
        self.minorRune3.resize(pixmapShard3.width(), pixmapShard3.height())

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