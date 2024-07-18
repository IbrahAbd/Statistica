import sys
import time
from OPGGparser import *
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from PyQt5.QtGui import QPixmap


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

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI.ui', self) 

        champ = "Jhin" 
        counter = counters(champ)

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
        self.name.setStyleSheet("color: white;")

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
        self.PickRate.setStyleSheet("color: white;")

        self.role.setText(role)
        self.role.setFont(font2)
        self.role.setStyleSheet("color: white;")

        rune1 = rates['MainRuneName']
        rune2 = rates['SecondaryRuneName']
        primaryRune = rates['MainPrimaryRune'].replace(" ", "")
        runes = rates['MinorRunes']

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

        shards = rates['Shards']
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


        extractAbilityDescriptionFromFile("Champion_abilities.txt", champ)

        pixmapQ = QPixmap(f'Abilities\{champ}Q.png')
        self.Q.setPixmap(pixmapQ)
        self.Q.setPixmap(pixmapQ.scaled(self.Q.size(), aspectRatioMode=True))
        self.Q.resize(pixmapQ.width(), pixmapQ.height())
        self.Q.setToolTip((abilityNames[0] + "\n" + abilityDescription[0]).replace(". ",".").replace(".",".\n"))
        
        pixmapW = QPixmap(f'Abilities\{champ}W.png')
        self.W.setPixmap(pixmapW)
        self.W.setPixmap(pixmapW.scaled(self.W.size(), aspectRatioMode=True))
        self.W.resize(pixmapW.width(), pixmapW.height())
        self.W.setToolTip((abilityNames[1] + "\n" + abilityDescription[1]).replace(". ",".").replace(".",".\n"))

        pixmapE = QPixmap(f'Abilities\{champ}E.png')
        self.E.setPixmap(pixmapE)
        self.E.setPixmap(pixmapE.scaled(self.E.size(), aspectRatioMode=True))
        self.E.resize(pixmapE.width(), pixmapE.height())
        self.E.setToolTip((abilityNames[2] + "\n" + abilityDescription[2]).replace(". ",".").replace(".",".\n"))

        pixmapR = QPixmap(f'Abilities\{champ}R.png')
        self.R.setPixmap(pixmapR)
        self.R.setPixmap(pixmapR.scaled(self.R.size(), aspectRatioMode=True))
        self.R.resize(pixmapR.width(), pixmapR.height())
        self.R.setToolTip((abilityNames[3] + "\n" + abilityDescription[3]).replace(". ",".").replace(".",".\n"))

        pixmapP = QPixmap(f'passive\{champ}_P.png')
        self.P.setPixmap(pixmapP)
        self.P.setPixmap(pixmapP.scaled(self.P.size(), aspectRatioMode=True))
        self.P.resize(pixmapP.width(), pixmapP.height())
        self.P.setToolTip((abilityNames[4] + "\n" + abilityDescription[4]).replace(". ",".").replace(".",".\n"))


        name0 = counter['champ0']['name'].replace("'","").replace(" ","").replace(".","")
        winRate0 = str(round(float(counter['champ0']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap0 = QPixmap(f'Images\{name0}.png')
        self.BestPicked1.setPixmap(pixmap0)
        self.BestPicked1.setPixmap(pixmap0.scaled(self.BestPicked1.size(), aspectRatioMode=True))
        self.BestPicked1.resize(pixmap0.width(), pixmap0.height())
        self.BestPickedWR0.setText(winRate0)
        self.BestPickedWR0.setFont(font)
        self.BestPickedWR0.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        name1 = counter['champ1']['name'].replace("'","").replace(" ","").replace(".","")
        winRate1 = str(round(float(counter['champ1']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap1 = QPixmap(f'Images\{name1}.png')
        self.BestPicked2.setPixmap(pixmap1)
        self.BestPicked2.setPixmap(pixmap1.scaled(self.BestPicked2.size(), aspectRatioMode=True))
        self.BestPicked2.resize(pixmap1.width(), pixmap1.height())
        self.BestPickedWR1.setText(winRate1)
        self.BestPickedWR1.setFont(font)
        self.BestPickedWR1.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        name2 = counter['champ2']['name'].replace("'","").replace(" ","").replace(".","")
        winRate2 = str(round(float(counter['champ2']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap2 = QPixmap(f'Images\{name2}.png')
        self.BestPicked3.setPixmap(pixmap2)
        self.BestPicked3.setPixmap(pixmap2.scaled(self.BestPicked3.size(), aspectRatioMode=True))
        self.BestPicked3.resize(pixmap2.width(), pixmap2.height())
        self.BestPickedWR2.setText(winRate2)
        self.BestPickedWR2.setFont(font)
        self.BestPickedWR2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        name3 = counter['champ3']['name'].replace("'","").replace(" ","").replace(".","")
        winRate3 = str(round(float(counter['champ3']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap3 = QPixmap(f'Images\{name3}.png')
        self.BestPicked4.setPixmap(pixmap3)
        self.BestPicked4.setPixmap(pixmap3.scaled(self.BestPicked4.size(), aspectRatioMode=True))
        self.BestPicked4.resize(pixmap3.width(), pixmap3.height())
        self.BestPickedWR3.setText(winRate3)
        self.BestPickedWR3.setFont(font)
        self.BestPickedWR3.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        name4 = counter['champ4']['name'].replace("'","").replace(" ","").replace(".","")
        winRate4 = str(round(float(counter['champ4']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap4 = QPixmap(f'Images\{name4}.png')
        self.BestPicked5.setPixmap(pixmap4)
        self.BestPicked5.setPixmap(pixmap4.scaled(self.BestPicked5.size(), aspectRatioMode=True))
        self.BestPicked5.resize(pixmap4.width(), pixmap4.height())
        self.BestPickedWR4.setText(winRate4)
        self.BestPickedWR4.setFont(font)
        self.BestPickedWR4.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        name5 = counter['champ5']['name'].replace("'","").replace(" ","").replace(".","")
        winRate5 = str(round(float(counter['champ5']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap5 = QPixmap(f'Images\{name5}.png')
        self.BestPicked6.setPixmap(pixmap5)
        self.BestPicked6.setPixmap(pixmap5.scaled(self.BestPicked6.size(), aspectRatioMode=True))
        self.BestPicked6.resize(pixmap5.width(), pixmap5.height())
        self.BestPickedWR5.setText(winRate5)
        self.BestPickedWR5.setFont(font)
        self.BestPickedWR5.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        name6 = counter['champ6']['name'].replace("'","").replace(" ","").replace(".","")
        winRate6 = str(round(float(counter['champ6']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap6 = QPixmap(f'Images\{name6}.png')
        self.BestPicked7.setPixmap(pixmap6)
        self.BestPicked7.setPixmap(pixmap6.scaled(self.BestPicked7.size(), aspectRatioMode=True))
        self.BestPicked7.resize(pixmap6.width(), pixmap6.height())
        self.BestPickedWR6.setText(winRate6)
        self.BestPickedWR6.setFont(font)
        self.BestPickedWR6.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        name7 = counter['champ7']['name'].replace("'","").replace(" ","").replace(".","")
        winRate7 = str(round(float(counter['champ7']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap7 = QPixmap(f'Images\{name7}.png')
        self.BestPicked8.setPixmap(pixmap7)
        self.BestPicked8.setPixmap(pixmap7.scaled(self.BestPicked8.size(), aspectRatioMode=True))
        self.BestPicked8.resize(pixmap7.width(), pixmap7.height())
        self.BestPickedWR7.setText(winRate7)
        self.BestPickedWR7.setFont(font)
        self.BestPickedWR7.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        name8 = counter['champ8']['name'].replace("'","").replace(" ","").replace(".","")
        winRate8 = str(round(float(counter['champ8']["win_rate"].replace("% WR","")),1)) + "%"
        pixmap8 = QPixmap(f'Images\{name8}.png')
        self.BestPicked9.setPixmap(pixmap8)
        self.BestPicked9.setPixmap(pixmap8.scaled(self.BestPicked9.size(), aspectRatioMode=True))
        self.BestPicked9.resize(pixmap8.width(), pixmap8.height())
        self.BestPickedWR8.setText(winRate8)
        self.BestPickedWR8.setFont(font)
        self.BestPickedWR8.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")


        CounterName0 = counter['champ10']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate0 = str(round(float(counter['champ10']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap0 = QPixmap(f'Images\{CounterName0}.png')
        self.BestPicked1_2.setPixmap(CounterPixmap0)
        self.BestPicked1_2.setPixmap(CounterPixmap0.scaled(self.BestPicked1_2.size(), aspectRatioMode=True))
        self.BestPicked1_2.resize(CounterPixmap0.width(), CounterPixmap0.height())
        self.BestPickedWR0_2.setText(CounterWinRate0)
        self.BestPickedWR0_2.setFont(font)
        self.BestPickedWR0_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")


        CounterName1 = counter['champ11']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate1 = str(round(float(counter['champ11']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap1 = QPixmap(f'Images\{CounterName1}.png')
        self.BestPicked2_2.setPixmap(CounterPixmap1)
        self.BestPicked2_2.setPixmap(CounterPixmap1.scaled(self.BestPicked2_2.size(), aspectRatioMode=True))
        self.BestPicked2_2.resize(CounterPixmap1.width(), CounterPixmap1.height())
        self.BestPickedWR1_2.setText(CounterWinRate1)
        self.BestPickedWR1_2.setFont(font)
        self.BestPickedWR1_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        CounterName2 = counter['champ12']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate2 = str(round(float(counter['champ12']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap2 = QPixmap(f'Images\{CounterName2}.png')
        self.BestPicked3_2.setPixmap(CounterPixmap2)
        self.BestPicked3_2.setPixmap(CounterPixmap2.scaled(self.BestPicked3_2.size(), aspectRatioMode=True))
        self.BestPicked3_2.resize(CounterPixmap2.width(), CounterPixmap2.height())
        self.BestPickedWR2_2.setText(CounterWinRate2)
        self.BestPickedWR2_2.setFont(font)
        self.BestPickedWR2_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        CounterName3 = counter['champ13']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate3 = str(round(float(counter['champ13']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap3 = QPixmap(f'Images\{CounterName3}.png')
        self.BestPicked4_2.setPixmap(CounterPixmap3)
        self.BestPicked4_2.setPixmap(CounterPixmap3.scaled(self.BestPicked3_2.size(), aspectRatioMode=True))
        self.BestPicked4_2.resize(CounterPixmap3.width(), CounterPixmap3.height())
        self.BestPickedWR3_2.setText(CounterWinRate3)
        self.BestPickedWR3_2.setFont(font)
        self.BestPickedWR3_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        CounterName4 = counter['champ14']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate4 = str(round(float(counter['champ14']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap4 = QPixmap(f'Images\{CounterName4}.png')
        self.BestPicked5_2.setPixmap(CounterPixmap4)
        self.BestPicked5_2.setPixmap(CounterPixmap4.scaled(self.BestPicked4_2.size(), aspectRatioMode=True))
        self.BestPicked5_2.resize(CounterPixmap4.width(), CounterPixmap4.height())
        self.BestPickedWR4_2.setText(CounterWinRate4)
        self.BestPickedWR4_2.setFont(font)
        self.BestPickedWR4_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        CounterName5 = counter['champ15']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate5 = str(round(float(counter['champ15']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap5 = QPixmap(f'Images\{CounterName5}.png')
        self.BestPicked6_2.setPixmap(CounterPixmap5)
        self.BestPicked6_2.setPixmap(CounterPixmap5.scaled(self.BestPicked5_2.size(), aspectRatioMode=True))
        self.BestPicked6_2.resize(CounterPixmap5.width(), CounterPixmap5.height())
        self.BestPickedWR5_2.setText(CounterWinRate5)
        self.BestPickedWR5_2.setFont(font)
        self.BestPickedWR5_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        CounterName6 = counter['champ16']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate6 = str(round(float(counter['champ16']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap6 = QPixmap(f'Images\{CounterName6}.png')
        self.BestPicked7_2.setPixmap(CounterPixmap6)
        self.BestPicked7_2.setPixmap(CounterPixmap6.scaled(self.BestPicked6_2.size(), aspectRatioMode=True))
        self.BestPicked7_2.resize(CounterPixmap6.width(), CounterPixmap6.height())
        self.BestPickedWR6_2.setText(CounterWinRate6)
        self.BestPickedWR6_2.setFont(font)
        self.BestPickedWR6_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        CounterName7 = counter['champ17']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate7 = str(round(float(counter['champ17']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap7 = QPixmap(f'Images\{CounterName7}.png')
        self.BestPicked8_2.setPixmap(CounterPixmap7)
        self.BestPicked8_2.setPixmap(CounterPixmap7.scaled(self.BestPicked7_2.size(), aspectRatioMode=True))
        self.BestPicked8_2.resize(CounterPixmap7.width(), CounterPixmap7.height())
        self.BestPickedWR7_2.setText(CounterWinRate7)
        self.BestPickedWR7_2.setFont(font)
        self.BestPickedWR7_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")

        CounterName8 = counter['champ18']['name'].replace("'","").replace(" ","").replace(".","")
        CounterWinRate8 = str(round(float(counter['champ18']["lose_rate"].replace("% WR","")),1)) + "%"
        CounterPixmap8 = QPixmap(f'Images\{CounterName8}.png')
        self.BestPicked9_2.setPixmap(CounterPixmap8)
        self.BestPicked9_2.setPixmap(CounterPixmap8.scaled(self.BestPicked8_2.size(), aspectRatioMode=True))
        self.BestPicked9_2.resize(CounterPixmap8.width(), CounterPixmap8.height())
        self.BestPickedWR8_2.setText(CounterWinRate8)
        self.BestPickedWR8_2.setFont(font)
        self.BestPickedWR8_2.setStyleSheet("color: white;font-size: 18px;background-color: transparent;")



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