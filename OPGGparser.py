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

        runes = soup.find_all('div', class_='perk-style-title')
        combo['MainRune'] = runes[0].text
        combo['SecondaryRune'] = runes[1].text

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
