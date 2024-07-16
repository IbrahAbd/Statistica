from bs4 import BeautifulSoup
import requests

SummonerSpellSRCs = [
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/spell/SummonerFlash.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/spell/SummonerSmite.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/spell/SummonerBarrier.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/spell/SummonerHaste.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/spell/SummonerHeal.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/spell/SummonerDot.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/spell/SummonerTeleport.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/spell/SummonerExhaust.webp",

]
MainRuneSRCs = [
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Resolve/GraspOfTheUndying/GraspOfTheUndying.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Resolve/VeteranAftershock/VeteranAftershock.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Resolve/Guardian/Guardian.webp",

    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Domination/Electrocute/Electrocute.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Domination/DarkHarvest/DarkHarvest.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Domination/HailOfBlades/HailOfBlades.webp",

    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Sorcery/SummonAery/SummonAery.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Sorcery/ArcaneComet/ArcaneComet.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Sorcery/PhaseRush/PhaseRush.webp",

    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Precision/Conqueror/Conqueror.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Precision/FleetFootwork/FleetFootwork.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Precision/PressTheAttack/PressTheAttack.webp",

    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Inspiration/GlacialAugment/GlacialAugment.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Inspiration/UnsealedSpellbook/UnsealedSpellbook.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.13.1/img/small-perk-images/Styles/Inspiration/FirstStrike/FirstStrike.webp",
]

RuneTypes = ["Domination","Sorcery","Inspiration","Precision","Resolve"]

def get_page_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None


def extract_value(text):
    return text.split('%')[0] if '%' in text else text

def parse_rates(html):
    soup = BeautifulSoup(html, "lxml")
    combo = {}

    try:
        win_rate = soup.find('div', class_='win-rate').get_text().strip()
        pick_rate = soup.find('div', class_='pick-rate').get_text().strip()
        ban_rate = soup.find('div', class_='ban-rate').get_text().strip()
        role = soup.find('span', class_='champion-title').get_text().strip().split()
        mainRune = soup.find('div', class_='perk-style-title').get_text().strip()
        secondaryRune = soup.find('div', class_='perk-style-title').get_text().strip()

        combo['win_rate'] = extract_value(win_rate) + '%'
        combo['pick_rate'] = extract_value(pick_rate) + '%'
        combo['ban_rate'] = extract_value(ban_rate) + '%'
        position = role[2]
        combo['role'] = extract_value(position[:-1])
        
        count = 0

        runes = soup.find_all('div', class_='perk-style-title')
        combo['MainRuneName'] = runes[0].text
        combo['SecondaryRuneName'] = runes[1].text
        
        mainRuneHTML = soup.find('div',class_="perk keystone perk-active")
        perk_name1 = mainRuneHTML.img['alt'].split()
        mainRune = ' '.join(perk_name1[2:])
        combo['MainPrimaryRune']  = mainRune

        mainSecondaryRuneHTML = soup.find_all('div',class_="perk perk-active")

        perk_names = []

        for rune in mainSecondaryRuneHTML:
            alt_text = rune.img['alt'].split()
            minorRune = (' '.join(alt_text[2:])).replace(" ", "").replace(":","")
            perk_names.append(minorRune)


        combo['MinorRunes'] = perk_names
        print(perk_names)

        shard_names = []
        shardRuneHTML = soup.find_all('div',class_="shard shard-active")
        for shard in shardRuneHTML:
            altText = shard.img['alt']
            shard_names.append(altText)

        combo['Shards'] = shard_names
            
        for i in range (2):
            for src in SummonerSpellSRCs:
                img = soup.find('img', {'src': src})
                if img:
                    alt_text = img['alt']
                    if count == 0:
                        combo['SumSpell1'] = alt_text.split()[-1:]
                        count += 1
                    elif count == 1:
                        combo['SumSpell2'] = alt_text.split()[-1:]


        img = soup.find_all('img', {'src': src})
        return combo
    
    except AttributeError as e:
        print(f"Error parsing rates: {e}")
        return None

def output(champ):
    url = f'https://u.gg/lol/champions/{champ}/build?rank=overall'
    html = get_page_html(url)
    
    if html:
        rates = parse_rates(html)
        if rates:
            return rates
        else:
            print("Could not find rates on the page.")
    else:
        print("Failed to retrieve the page.")