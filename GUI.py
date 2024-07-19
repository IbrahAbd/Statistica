import sys
import time
from OPGGparser import *
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QThread
import asyncio


filePath = 'RuneDescriptions.txt'
champFilePath = 'Champion_abilities.txt'

def getRuneDescription(file_path, rune_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    description = []
    found_rune = False

    for line in lines:
        stripped_line = line.strip()
        if found_rune:
            if stripped_line == "":
                break
            description.append(line)
        if stripped_line == rune_name:
            found_rune = True

    return ''.join(description).strip()

def extractChampionInfo(input_text, champion_name, ability_label):
    with open(input_text, 'r', encoding='utf-8') as file:
        input_text = file.read()

    lines = input_text.strip().splitlines()
    capture_description = False
    ability_description = []

    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(f"Champion: {champion_name}"):
            capture_description = False
        elif capture_description:
            if stripped_line.startswith("Description:"):
                ability_description.append(stripped_line.replace("Description:", "").strip())
            elif stripped_line.startswith(("Q Ability:", "W Ability:", "E Ability:", "R Ability:", "Passive:")):
                break
        elif stripped_line.startswith(f"{ability_label} Ability:"):
            capture_description = True

    if ability_description:
        return '\n'.join(ability_description)  
    else:
        return f"No {ability_label} Ability description found for {champion_name}."
    
abilityDescription = ["","","","",""]
abilityNames = ["","","","",""]
abilities = ["Q","W","E", "R", "P"]

def extractAbilityDescriptionFromFile(input_file, champion_name):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    characterFound = False
    
    i = 0
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(f"Champion: {champion_name}"):
            characterFound = True
            
        if characterFound == True:
            
            if (stripped_line.startswith("Q Ability:")):
                abilityNames[0] = stripped_line.replace("Q Ability: ", "").strip()

            elif (stripped_line.startswith("W Ability:")):
                abilityNames[1] = stripped_line.replace("W Ability: ", "").strip()

            elif (stripped_line.startswith("E Ability:")):
                abilityNames[2] = stripped_line.replace("E Ability: ", "").strip()

            elif (stripped_line.startswith("R Ability:")):
                    abilityNames[3] = stripped_line.replace("R Ability: ", "").strip()
                    
            elif (stripped_line.startswith("Passive:")):
                abilityNames[4] = stripped_line.replace("Passive: ", "").strip()

                
            elif (stripped_line.startswith("Description:")):
                abilityDescription[i] = stripped_line.replace("Description:", "").strip()
                i += 1
             
        if i == 5:
            break

class ScrapingThread(QThread):
    scraping_done = pyqtSignal(dict, dict)

    def __init__(self, champ):
        super().__init__()
        self.champ = champ

    def run(self):
        asyncio.run(self.scrape())

    async def scrape(self):
        rates, counter = await self.concurrentRun(self.champ)
        self.scraping_done.emit(rates, counter)

    async def concurrentRun(self,champion):
        output_task = asyncio.create_task(output(champion))
        counters_task = asyncio.create_task(counters(champion))
    
        rates = await output_task
        counter = await counters_task
        
        return rates, counter
    
    
class MainWindow2(QtWidgets.QMainWindow):
    def __init__(self,champ):
        self.champ = champ
        self.rates = {}
        self.counter = {}
        super().__init__()
        uic.loadUi('GUI.ui', self) 
        self.initUI()

    def initUI(self):
        self.thread = ScrapingThread(self.champ)
        self.thread.scraping_done.connect(self.on_scraping_done)
        self.thread.start()

    def on_scraping_done(self, rates, counter):
        self.rates = rates
        self.counter = counter
        self.show_results()

    def show_results(self):
        # Ensure that this method handles the case where rates and counter might be None
        role = self.rates.get('role')
        font = QtGui.QFont()
        font.setPointSize(40)  
        
        pixmap = QPixmap(f'Roles\{role}.png')
        self.roleIMG.setPixmap(pixmap)
        self.roleIMG.setPixmap(pixmap.scaled(self.roleIMG.size(), aspectRatioMode=True))
        self.roleIMG.resize(pixmap.width(), pixmap.height())

        self.display_image(f'Images\{self.champ}.png')

        if (self.champ.find(" ") == False):
            champName = self.champ.split(" ")
            self.champ = champName[0] + " " + champName[1]

        self.name.setText(self.champ)
        self.name.setFont(font)
        self.name.setStyleSheet("color: white;")

        sumSpell1 = self.rates.get('SumSpell1'[0])
        sumSpell2 = self.rates.get('SumSpell2'[0])

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

        self.WinRate.setText("Win rate: " + self.rates.get('win_rate'))
        self.WinRate.setFont(font2)
        self.WinRate.setStyleSheet("color: green;")

        self.BanRate.setText("Ban rate: " + self.rates.get('ban_rate'))
        self.BanRate.setFont(font2)
        self.BanRate.setStyleSheet("color: red;")

        self.PickRate.setText("Pick rate: " + self.rates.get('pick_rate'))
        self.PickRate.setFont(font2)
        self.PickRate.setStyleSheet("color: white;")

        self.role.setText(role)
        self.role.setFont(font2)
        self.role.setStyleSheet("color: white;")

        rune1 = self.rates.get('MainRuneName')
        rune2 = self.rates.get('SecondaryRuneName')
        primaryRune = self.rates.get('MainPrimaryRune').replace(" ", "")
        runes = self.rates.get('MinorRunes')

        pixmapMainRune = QPixmap(f'Runes\{rune1}\{primaryRune}.png')
        self.MainRune.setPixmap(pixmapMainRune)
        self.MainRune.setPixmap(pixmapMainRune.scaled(self.MainRune.size(), aspectRatioMode=True))
        self.MainRune.resize(pixmapMainRune.width(), pixmapMainRune.height())
        self.MainRune.setToolTip(getRuneDescription(filePath,primaryRune))


        pixmapSecondaryRune = QPixmap(f'Runes\{rune2}.png')
        self.SecondaryRune.setPixmap(pixmapSecondaryRune)
        self.SecondaryRune.setPixmap(pixmapSecondaryRune.scaled(self.SecondaryRune.size(), aspectRatioMode=True))
        self.SecondaryRune.resize(pixmapSecondaryRune.width(), pixmapSecondaryRune.height())

        pixmapPrimaryRune1 = QPixmap(f'Runes\{rune1}\{runes[0]}.png')
        self.MainRune1.setPixmap(pixmapPrimaryRune1)
        self.MainRune1.setPixmap(pixmapPrimaryRune1.scaled(self.MainRune1.size(), aspectRatioMode=True))
        self.MainRune1.resize(pixmapPrimaryRune1.width(), pixmapPrimaryRune1.height())
        self.MainRune1.setToolTip(getRuneDescription(filePath,runes[0]))
        
        pixmapPrimaryRune2 = QPixmap(f'Runes\{rune1}\{runes[1]}.png')
        self.MainRune2.setPixmap(pixmapPrimaryRune2)
        self.MainRune2.setPixmap(pixmapPrimaryRune2.scaled(self.MainRune2.size(), aspectRatioMode=True))
        self.MainRune2.resize(pixmapPrimaryRune2.width(), pixmapPrimaryRune2.height())
        self.MainRune2.setToolTip(getRuneDescription(filePath,runes[1]))
        
        pixmapPrimaryRune3 = QPixmap(f'Runes\{rune1}\{runes[2]}.png')
        self.MainRune3.setPixmap(pixmapPrimaryRune3)
        self.MainRune3.setPixmap(pixmapPrimaryRune3.scaled(self.MainRune3.size(), aspectRatioMode=True))
        self.MainRune3.resize(pixmapPrimaryRune3.width(), pixmapPrimaryRune3.height())
        self.MainRune3.setToolTip(getRuneDescription(filePath,runes[2]))

        pixmapSecondaryRune1 = QPixmap(f'Runes\{rune2}\{runes[3]}.png')
        self.SecondaryRune1.setPixmap(pixmapSecondaryRune1)
        self.SecondaryRune1.setPixmap(pixmapSecondaryRune1.scaled(self.SecondaryRune1.size(), aspectRatioMode=True))
        self.SecondaryRune1.resize(pixmapSecondaryRune1.width(), pixmapSecondaryRune1.height())
        self.SecondaryRune1.setToolTip(getRuneDescription(filePath,runes[3]))


        pixmapSecondaryRune2 = QPixmap(f'Runes\{rune2}\{runes[4]}.png')
        self.SecondaryRune2.setPixmap(pixmapSecondaryRune2)
        self.SecondaryRune2.setPixmap(pixmapSecondaryRune2.scaled(self.SecondaryRune2.size(), aspectRatioMode=True))
        self.SecondaryRune2.resize(pixmapSecondaryRune2.width(), pixmapSecondaryRune2.height())
        self.SecondaryRune2.setToolTip(getRuneDescription(filePath,runes[4]))

        shards = self.rates.get('Shards')
        pixmapShard1 = QPixmap(f'Runes\{shards[0]}.png')
        self.minorRune1.setPixmap(pixmapShard1)
        self.minorRune1.setPixmap(pixmapShard1.scaled(self.minorRune1.size(), aspectRatioMode=True))
        self.minorRune1.resize(pixmapShard1.width(), pixmapShard1.height())
        self.minorRune1.setToolTip(getRuneDescription(filePath,shards[0]))

        pixmapShard2 = QPixmap(f'Runes\{shards[1]}.png')
        self.minorRune2.setPixmap(pixmapShard2)
        self.minorRune2.setPixmap(pixmapShard2.scaled(self.minorRune2.size(), aspectRatioMode=True))
        self.minorRune2.resize(pixmapShard2.width(), pixmapShard2.height())
        self.minorRune2.setToolTip(getRuneDescription(filePath,shards[1]))

        pixmapShard3 = QPixmap(f'Runes\{shards[2]}.png')
        self.minorRune3.setPixmap(pixmapShard3)
        self.minorRune3.setPixmap(pixmapShard3.scaled(self.minorRune3.size(), aspectRatioMode=True))
        self.minorRune3.resize(pixmapShard3.width(), pixmapShard3.height())
        self.minorRune3.setToolTip(getRuneDescription(filePath,shards[2]))


        extractAbilityDescriptionFromFile("Champion_abilities.txt", self.champ)

        pixmapQ = QPixmap(f'Abilities\{self.champ}Q.png')
        self.Q.setPixmap(pixmapQ)
        self.Q.setPixmap(pixmapQ.scaled(self.Q.size(), aspectRatioMode=True))
        self.Q.resize(pixmapQ.width(), pixmapQ.height())
        self.Q.setToolTip((abilityNames[0] + "\n" + abilityDescription[0]).replace(". ",".").replace(".",".\n"))
        
        pixmapW = QPixmap(f'Abilities\{self.champ}W.png')
        self.W.setPixmap(pixmapW)
        self.W.setPixmap(pixmapW.scaled(self.W.size(), aspectRatioMode=True))
        self.W.resize(pixmapW.width(), pixmapW.height())
        self.W.setToolTip((abilityNames[1] + "\n" + abilityDescription[1]).replace(". ",".").replace(".",".\n"))

        pixmapE = QPixmap(f'Abilities\{self.champ}E.png')
        self.E.setPixmap(pixmapE)
        self.E.setPixmap(pixmapE.scaled(self.E.size(), aspectRatioMode=True))
        self.E.resize(pixmapE.width(), pixmapE.height())
        self.E.setToolTip((abilityNames[2] + "\n" + abilityDescription[2]).replace(". ",".").replace(".",".\n"))

        pixmapR = QPixmap(f'Abilities\{self.champ}R.png')
        self.R.setPixmap(pixmapR)
        self.R.setPixmap(pixmapR.scaled(self.R.size(), aspectRatioMode=True))
        self.R.resize(pixmapR.width(), pixmapR.height())
        self.R.setToolTip((abilityNames[3] + "\n" + abilityDescription[3]).replace(". ",".").replace(".",".\n"))

        pixmapP = QPixmap(f'passive\{self.champ}_P.png')
        self.P.setPixmap(pixmapP)
        self.P.setPixmap(pixmapP.scaled(self.P.size(), aspectRatioMode=True))
        self.P.resize(pixmapP.width(), pixmapP.height())
        self.P.setToolTip((abilityNames[4] + "\n" + abilityDescription[4]).replace(". ",".").replace(".",".\n"))

        for i in range(0,9):
            champ_data = self.counter.get(f'champ{i}', {})  # Default to empty dict if 'champ1' is not present
            name = champ_data.get('name', '').replace("'", "").replace(" ", "").replace(".", "")
            win_rate_raw = champ_data.get('win_rate', '')
            winRate = ""
            if win_rate_raw:
                winRate = str(round(float(win_rate_raw.replace("% WR", "")), 1)) + "%"
                pixmap = QPixmap(f'Images\{name}.png')

                widget_name = getattr(self, f'BestPicked{i+1}', None)
                widget_name2 = getattr(self, f'BestPickedWR{i}', None)

                widget_name.setPixmap(pixmap)
                widget_name.setPixmap(pixmap.scaled(widget_name.size(), aspectRatioMode=True))

                widget_name.resize(pixmap.width(), pixmap.height())
                widget_name2.setText(winRate)
                widget_name2.setFont(font)
                widget_name2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")
        j = 10
        for i in range(0,9):
            champ_data = self.counter.get(f'champ{j}', {})  # Default to empty dict if 'champ1' is not present
            j += 1
            name = champ_data.get('name', '').replace("'", "").replace(" ", "").replace(".", "")
            lose_rate_raw = champ_data.get('lose_rate', '')
            loseRate = ""
            if lose_rate_raw:
                loseRate = str(round(float(lose_rate_raw.replace("% WR", "")), 1)) + "%"
                pixmap = QPixmap(f'Images\{name}.png')

                widget_name = getattr(self, f'BestPicked{i+1}_2', None)
                widget_name2 = getattr(self, f'BestPickedWR{i}_2', None)

                widget_name.setPixmap(pixmap)
                widget_name.setPixmap(pixmap.scaled(widget_name.size(), aspectRatioMode=True))

                widget_name.resize(pixmap.width(), pixmap.height())
                widget_name2.setText(loseRate)
                widget_name2.setFont(font)
                widget_name2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")
        print('Done')
        #pass


    def display_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            
            self.label.setPixmap(scaled_pixmap)
            self.label.setAlignment(QtCore.Qt.AlignCenter) 
        else:
            print(f"Error: Unable to load image from {image_path}")
