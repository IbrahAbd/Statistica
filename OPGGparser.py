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

# Function to parse the HTML content and extract Jhin's win rate and pick rate
def parse_rates(html):
    soup = BeautifulSoup(html, 'html.parser')
    combo = {}
    
    # Find all elements with the class 'css-oxevym e1y855lo3'
    rate_elements = soup.find_all('div', class_='css-oxevym e1y855lo3')
    
    if rate_elements and len(rate_elements) >= 3:
        win_rate = rate_elements[0].get_text().strip()
        pick_rate = rate_elements[1].get_text().strip()
        ban_rate = rate_elements[2].get_text().strip()

        combo['win_rate'] = win_rate
        combo['pick_rate'] = pick_rate
        combo['ban_rate'] = ban_rate
        
        return combo
    else:
        return None

# Main function to get and display Jhin's win rate and pick rate
def output(champ):
    url = f'https://www.op.gg/champions/{champ}/build/adc'
    html = get_page_html(url)
    if html:
        rates = parse_rates(html)
        if rates:
            return rates
        else:
            print("Could not find the win rate and pick rate on the page.")
    else:
        print("Failed to retrieve the page.")

