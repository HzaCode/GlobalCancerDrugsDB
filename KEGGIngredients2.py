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
        th_element = soup.find('th', string="Name")
        if th_element:
            td_element = th_element.find_next_sibling('td')
            if td_element:
                names = [line.strip() for line in td_element.text.split('\n') if line.strip()]
                return names
    else:
        print(f"Failed，status code {response.status_code}")
    return []

def clean_names(ingredients):
    cleaned_ingredients = []
    for ingredient in ingredients:
        # Handle semicolon and parentheses
        if ';' in ingredient:
            ingredient = ingredient.split(';')[0]
        # Strip unwanted annotations within parentheses
        parts = ingredient.split('(')
        base_name = parts[0].strip()
        if len(parts) > 1:
            additional_info = []
            for part in parts[1:]:
                content = part.split(')')[0].strip()
                if content not in {"USP", "USAN", "JAN"}:
                    additional_info.append(content)
            if additional_info:
                base_name += f" ({', '.join(additional_info)})"
        if base_name.lower() != "dried" and base_name != "":
            cleaned_ingredients.append(f'"{base_name}"')
    return cleaned_ingredients

def main():
    excel_path = 
    df = pd.read_excel(excel_path)
    for index, row in df.iterrows():
        kegg_id = row['id'].strip()
        url = f'https://www.kegg.jp/entry/{kegg_id}'
        ingredients = fetch_kegg_ingredients(url)
        cleaned_ingredients = clean_names(ingredients)  # Clean names after all are fetched
        ingredients_count = len(cleaned_ingredients)
        print(f"Ingredients for {kegg_id} (Total: {ingredients_count}):")
        print('[' + ', '.join(cleaned_ingredients) + ']')
        time.sleep(1)

if __name__ == "__main__":
    main()
