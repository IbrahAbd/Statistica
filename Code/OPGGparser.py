from bs4 import BeautifulSoup
import aiohttp

SummonerSpellSRCs = [
    "https://static.bigbrain.gg/assets/lol/riot_static/14.14.1/img/spell/SummonerFlash.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.14.1/img/spell/SummonerSmite.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.14.1/img/spell/SummonerBarrier.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.14.1/img/spell/SummonerHaste.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.14.1/img/spell/SummonerHeal.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.14.1/img/spell/SummonerDot.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.14.1/img/spell/SummonerTeleport.webp",
    "https://static.bigbrain.gg/assets/lol/riot_static/14.14.1/img/spell/SummonerExhaust.webp",
]

RuneTypes = ["Domination","Sorcery","Inspiration","Precision","Resolve"]
async def get_page_html(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                return None


def extract_value(text):
    return text.split('%')[0] if '%' in text else text

async def parse_rates(html):
    soup = BeautifulSoup(html, "lxml")
    combo = {}

    try:
        win_rate = soup.find('div', class_='win-rate').get_text().strip()
        pick_rate = soup.find('div', class_='pick-rate').get_text().strip()
        ban_rate = soup.find('div', class_='ban-rate').get_text().strip()
        role = soup.find('span', class_='champion-title').get_text().strip().split()
        mainRune = soup.find('div', class_='perk-style-title').get_text().strip()

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


        return combo
    
    except AttributeError as e:
        print(f"Error parsing rates: {e}")
        return None

async def output(champ):
    url = f'https://u.gg/lol/champions/{champ}/build?rank=overall'
    html = await get_page_html(url)
    
    if html:
        rates = await parse_rates(html)
        if rates:
            return rates
        else:
            print("Could not find rates on the page.")
    else:
        print("Failed to retrieve the page.")

async def counters(champ):
    url = f'https://u.gg/lol/champions/{champ}/counter?rank=overall'
    html = await get_page_html(url)
    counters = {}

    if html:
        soup = BeautifulSoup(html, "lxml")
        i = 0
        outer_divs = soup.find_all('div', class_='col-2')
        if outer_divs:
            for champion in outer_divs:
                inner_div1 = champion.find('div', class_='champion-name')
                if inner_div1:
                    name = inner_div1.get_text().strip()
                    counters[f"champ{i}"] = {"name": name}
                    i += 1

        j = 0
        outer_div2 = soup.find_all('div', class_='col-3')
        if outer_div2:
            for div in outer_div2:
                winRate = div.find('div', class_='win-rate').get_text().strip()
                if winRate:
                    if j > 9:
                        counters[f"champ{j}"]["lose_rate"] = winRate
                    else:
                        counters[f"champ{j}"]["win_rate"] = winRate
                    j += 1

        if counters:
            return counters
        else:
            print("Could not find rates on the page.")
    else:
        print("Failed to retrieve the page.")

