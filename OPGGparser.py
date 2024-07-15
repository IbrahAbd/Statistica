import requests
from bs4 import BeautifulSoup

# Function to get the HTML content of the page
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

# Function to parse the HTML content and extract Jhin's win rate and pick rate
def parse_rates(html):
    soup = BeautifulSoup(html, 'html.parser')
    combo = {}
    
    # Find all elements with the class 'css-oxevym e1y855lo3'
    winR = (soup.find('div', class_='win-rate okay-tier')).get_text().strip()
    pickR = (soup.find('div', class_='pick-rate')).get_text().strip()
    banR = (soup.find('div', class_='ban-rate')).get_text().strip()
    
    combo['win_rate'] = extract_value(winR) + '%'
    combo['pick_rate'] = extract_value(pickR) + '%'
    combo['ban_rate'] = extract_value(banR) + '%'
        
    return combo


# Main function to get and display Jhin's win rate and pick rate
def output(champ,role):
    url = f'https://u.gg/lol/champions/{champ}/build/{role}?rank=overall'
    html = get_page_html(url)
    if html:
        rates = parse_rates(html)
        if rates:
            return rates
        else:
            print("Could not find the win rate and pick rate on the page.")
    else:
        print("Failed to retrieve the page.")