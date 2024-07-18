import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QPushButton, QHBoxLayout, QWidget, QScrollArea
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('StartScreen.ui', self)
        
        champions = [
            "Aatrox", "Ahri", "Akali", "Akshan", "Alistar", "Amumu", "Anivia", "Annie", "Aphelios", "Ashe", "AurelionSol","Aurora",
            "Azir", "Bard","Belveth", "Blitzcrank", "Brand", "Braum","Briar", "Caitlyn", "Camille", "Cassiopeia", "ChoGath", "Corki",
            "Darius", "Diana", "DrMundo", "Draven", "Ekko", "Elise", "Evelynn", "Ezreal", "Fiddlesticks", "Fiora",
            "Fizz", "Galio", "Gangplank", "Garen", "Gnar", "Gragas", "Graves", "Gwen", "Hecarim", "Heimerdinger", "Hwei",
            "Illaoi", "Irelia", "Ivern", "Janna", "JarvanIV", "Jax", "Jayce", "Jhin", "Jinx", "Kaisa", "Kalista",
            "Karma", "Karthus", "Kassadin", "Katarina", "Kayle", "Kayn", "Kennen", "Khazix", "Kindred", "Kled",
            "KogMaw","Ksante", "Leblanc", "LeeSin", "Leona", "Lillia", "Lissandra", "Lucian", "Lulu", "Lux", "Malphite","Naafiri",
            "Malzahar", "Maokai", "MasterYi", "MissFortune","Milio" ,"Mordekaiser", "Morgana", "Nami", "Nasus", "Nautilus",
            "Neeko", "Nidalee","Nilah", "Nocturne", "Nunu&Willump", "Olaf", "Orianna", "Ornn", "Pantheon", "Poppy", "Pyke", "Qiyana",
            "Quinn", "Rakan", "Rammus", "RekSai", "Rell", "RenataGlasc", "Renekton", "Rengar", "Riven", "Rumble", "Ryze", "Samira",
            "Sejuani", "Senna", "Seraphine", "Sett", "Shaco", "Shen", "Shyvana", "Singed", "Sion", "Sivir", "Skarner","Smolder",
            "Sona", "Soraka", "Swain", "Sylas", "Syndra", "TahmKench", "Taliyah", "Talon", "Taric", "Teemo", "Thresh",
            "Tristana", "Trundle", "Tryndamere", "TwistedFate", "Twitch", "Udyr", "Urgot", "Varus", "Vayne", "Veigar",
            "Velkoz","Vex", "Vi", "Viego", "Viktor", "Vladimir", "Volibear", "Warwick", "Wukong", "Xayah", "Xerath", "XinZhao",
            "Yasuo", "Yone", "Yorick", "Yuumi", "Zac", "Zed","Zeri", "Ziggs", "Zilean", "Zoe", "Zyra"]
            
        championsLower = ["aatrox", "ahri", "akali", "akshan", "alistar", "amumu", "anivia", "annie", "aphelios", "ashe", "aurelionsol","aurora",
            "azir", "bard","belveth", "blitzcrank", "brand", "braum","briar", "caitlyn", "camille", "cassiopeia", "chogath", "corki",
            "darius", "diana", "drmundo", "draven", "ekko", "elise", "evelynn", "ezreal", "fiddlesticks", "fiora",
            "fizz", "galio", "gangplank", "garen", "gnar", "gragas", "graves", "gwen", "hecarim", "heimerdinger", "hwei",
            "illaoi", "irelia", "ivern", "janna", "jarvaniv", "jax", "jayce", "jhin", "jinx", "kaisa", "kalista",
            "karma", "karthus", "kassadin", "katarina", "kayle", "kayn", "kennen", "khazix", "kindred", "kled",
            "kogmaw","ksante", "leblanc", "leesin", "leona", "lillia", "lissandra", "lucian", "lulu", "lux", "malphite","naafiri",
            "malzahar", "maokai", "masteryi", "missfortune","milio" ,"mordekaiser", "morgana", "nami", "nasus", "nautilus",
            "neeko", "nidalee","nilah", "nocturne", "nunu&willump", "olaf", "orianna", "ornn", "pantheon", "poppy", "pyke", "qiyana",
            "quinn", "rakan", "rammus", "reksai", "rell", "renataglasc", "renekton", "rengar", "riven", "rumble", "ryze", "samira",
            "sejuani", "senna", "seraphine", "sett", "shaco", "shen", "shyvana", "singed", "sion", "sivir", "skarner","smolder",
            "sona", "soraka", "swain", "sylas", "syndra", "tahmkench", "taliyah", "talon", "taric", "teemo", "thresh",
            "tristana", "trundle", "tryndamere", "twistedfate", "twitch", "udyr", "urgot", "varus", "vayne", "veigar",
            "velkoz","vex", "vi", "viego", "viktor", "vladimir", "volibear", "warwick", "wukong", "xayah", "xerath", "xinzhao",
            "yasuo", "yone", "yorick", "yuumi", "zac", "zed","zeri", "ziggs", "zilean", "zoe", "zyra"]

        # Create buttons for each champion and add them to the layout
        for i, champ in enumerate(champions, 1):
            if i == 50 or i == 52:
                i += 1
            button_name = f"pushButton_{i}"
            button = getattr(self, button_name)
            button.setStyleSheet(f"background-image: url('Images/{champ}.png');")
            button.setText("")  # Clear the text if needed

        completer = QtWidgets.QCompleter(champions+championsLower)
        
        # Set QCompleter object to QLineEdit
        self.lineEdit.setCompleter(completer)
        self.lineEdit.returnPressed.connect(self.on_return_pressed)

        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
