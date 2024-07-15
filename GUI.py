import sys
from OPGGparser import *
from PyQt5 import QtWidgets, QtGui, QtCore, uic

champ = "Jhin"

rates = output(champ)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self) 


        
        self.display_image(f'E:\github\Statistica\Images\{champ}.png')

        font = QtGui.QFont()
        font.setPointSize(40)  
        self.name.setText(champ)
        self.name.setFont(font)


        font2 = QtGui.QFont()
        font2.setPointSize(20)  

        self.WinRate.setText("Win rate: " + rates['win_rate'])
        self.WinRate.setFont(font2)

        self.BanRate.setText("Ban rate: " + rates['ban_rate'])
        self.BanRate.setFont(font2)

        self.PickRate.setText("Pick rate: " + rates['pick_rate'])
        self.PickRate.setFont(font2)

        

    def display_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            # Scale the pixmap to fit the label while preserving aspect ratio
            scaled_pixmap = pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            
            # Set the scaled pixmap as label's pixmap
            self.label.setPixmap(scaled_pixmap)
            self.label.setAlignment(QtCore.Qt.AlignCenter)  # Optional: Center the image in the label
        else:
            print(f"Error: Unable to load image from {image_path}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())




