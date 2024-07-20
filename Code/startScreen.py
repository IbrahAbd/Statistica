import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
from loadingScreen import MainWindow3
from GUI import MainWindow2

class ScraperThread(QThread):
    scraping_done = pyqtSignal(str)  # Pass the champion name as a signal

    def __init__(self, champ):
        super().__init__()
        self.champ = champ

    def run(self):
        self.scraping_done.emit(self.champ)



class MainWindow1(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('_internal/StartScreen.ui', self)

        self.stacked_widget = self.findChild(QStackedWidget, 'stackedWidget')
        self.lineEdit = self.findChild(QLineEdit, 'lineEdit')

        self.loading_screen = None
        self.main_window_2 = None

        self.initialize_line_edit()


    def initialize_line_edit(self):
        champions = [
            "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe", "AurelionSol", "Aurora",
            "Azir", "Bard", "Belveth", "Blitzcrank", "Brand", "Braum", "Briar", "Caitlyn", "Camille", "Cassiopeia", "ChoGath", "Corki",
            "Darius", "Diana", "DrMundo", "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora",
            "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Hwei",
            "Illaoi", "Irelia", "Ivern", "Janna", "JarvanIV", "Jax", "Jayce", "Jhin", "Jinx", "Kaisa", "Kalista",
            "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Khazix", "Kindred", "Kled",
            "KogMaw", "Ksante", "Leblanc", "LeeSin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite", "Naafiri",
            "Malzahar", "Maokai", "MasterYi", "MissFortune", "Milio", "Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus",
            "Neeko", "Nidalee", "Nilah", "Nocturne", "Nunu&Willump", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana",
            "Quinn", "Rakan", "Rammus", "RekSai", "Rell", "RenataGlasc", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira",
            "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner", "Smolder",
            "Sona", "Soraka", "Swain", "Sylas", "Syndra", "TahmKench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh",
            "Tristana", "Trundle", "Tryndamere", "TwistedFate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar",
            "Velkoz", "Vex", "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "XinZhao",
            "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed", "Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"
        ]
            
        championsLower = [champ.lower() for champ in champions]

        for i, champ in enumerate(champions, 1):
            button_name = f"pushButton_{i}"
            button = getattr(self, button_name, None)
            if button:
                button.setStyleSheet(f"background-image: url('_internal/Images/{champ}.png');")
                button.setText("")
                button.setObjectName(champ)
                button.clicked.connect(self.on_button_clicked)

        completer = QtWidgets.QCompleter(champions + championsLower)
        self.lineEdit.setCompleter(completer)
        self.lineEdit.returnPressed.connect(self.on_return_pressed)

    def on_button_clicked(self):
        button = self.sender()  
        champ_name = button.objectName()
        self.lineEdit.setText(champ_name) 
        self.on_return_pressed()

    def on_return_pressed(self):
        champ = self.lineEdit.text()
        champ = champ[0].upper() + champ[1:]
        self.lineEdit.clear()

        self.scraper_thread = ScraperThread(champ)
        self.scraper_thread.scraping_done.connect(self.on_scraping_done)
        self.scraper_thread.start()

    def on_scraping_done(self, champ):
        # Create and show the loading screen
        self.loading_screen = MainWindow3("_internal\gifs")
        self.stacked_widget.addWidget(self.loading_screen)
        self.stacked_widget.setCurrentWidget(self.loading_screen)

        # Create MainWindow2 and connect its signal
        self.main_window_2 = MainWindow2(champ)
        self.main_window_2.results_shown.connect(self.on_results_shown)
        self.main_window_2.back_to_main.connect(self.handle_back_to_main)

        # Wait for results and switch to MainWindow2
        self.wait_for_results_shown()

    def wait_for_results_shown(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_if_results_shown)
        self.timer.start(100)  # Check every 100 ms

    def check_if_results_shown(self):
        if self.main_window_2 and hasattr(self.main_window_2, 'results_shown_emitted') and self.main_window_2.results_shown_emitted:
            self.timer.stop()
            if not self.stacked_widget.widget(self.stacked_widget.indexOf(self.main_window_2)):
                self.stacked_widget.addWidget(self.main_window_2)
            self.stacked_widget.setCurrentWidget(self.main_window_2)

    def on_results_shown(self):

        self.main_window_2.results_shown_emitted = True

    def handle_back_to_main(self):
        if self.main_window_2:
            self.stacked_widget.removeWidget(self.main_window_2)
            self.main_window_2.close()
            self.main_window_2 = None

        self.stacked_widget.setCurrentIndex(0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow1()
    mainWindow.show()
    sys.exit(app.exec_())