import sys
from OPGGparser import *
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap

roles = ["Top","Jungle","ADC","Mid","Support"]
champ = "Zac" 
role = roles[0]

rates = output(champ,role)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self) 
        
        self.display_image(f'Images\{champ}.png')

        font = QtGui.QFont()
        font.setPointSize(40)  
        self.name.setText(champ)
        self.name.setFont(font)

        pixmap = QPixmap(f'Roles\{role}.png')
        self.roleIMG.setPixmap(pixmap)
        self.roleIMG.setPixmap(pixmap.scaled(self.roleIMG.size(), aspectRatioMode=True))
        self.roleIMG.resize(pixmap.width(), pixmap.height())


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

    print("dog")