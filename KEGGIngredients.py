import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

def fetch_kegg_ingredients(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        th_element = soup.find('th', string="Component")
        if th_element:
            td_element = th_element.find_next_sibling('td')
            if td_element:
                component_text = td_element.text.strip()
                components = [component.split(' [')[0] for component in component_text.split(', ')]
                return components
            else:
                print("No <td> sibling element found.")
        else:
            print("No <th> element with 'Component' found.")
    else:
        print(f"Failed to retrieve webpage, status code {response.status_code}")
    return []

def main():
    excel_path = '
    df = pd.read_excel(excel_path)
    for index, row in df.iterrows():
        kegg_id = row['id'].strip()
        url = f'https://www.kegg.jp/entry/{kegg_id}'
        ingredients = fetch_kegg_ingredients(url)
        print(f"Ingredients for {kegg_id}:")
        print(ingredients)
        time.sleep(1)

if __name__ == "__main__":
    main()
