import re
import requests
from bs4 import BeautifulSoup
import json
import time
import click
import os

def get_parsed_page(url):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

class CasesHandler():
    def _get_skin_description_and_lore(self, skin_page_url):
        possible_wears = []
        # Parse main page
        page = get_parsed_page(skin_page_url)
        # Isolate elements related to the skin lore
        page_content = page.find_all("p")
        description = page_content[6].text.split(": ")[1]
        lore = page_content[7].text.split(": ")[1]
        # Return
        return description,lore

    def _get_skin_wears(self, skin_page_url):
        possible_wears = []
        # Parse main page
        page = get_parsed_page(skin_page_url)
        # Isolate elements related to the skin wear
        page_content = page.find_all("div", {"class": "marker-value cursor-default"})
        min_wear = page_content[0].text
        max_wear = page_content[1].text
        # Define possible wears
        if float(min_wear) < 0.07 and float(max_wear) > 0.00:
            possible_wears.append("fn")
        if float(min_wear) < 0.15 and float(max_wear) > 0.07:
            possible_wears.append("mw")
        if float(min_wear) < 0.38 and float(max_wear) > 0.15:
            possible_wears.append("ft")
        if float(min_wear) < 0.45 and float(max_wear) > 0.38:
            possible_wears.append("ww")
        if float(min_wear) < 1 and float(max_wear) > 0.45:
            possible_wears.append("bs")
        # Return
        return possible_wears

    def _get_case_contents(self, case_page_url):
        case_content = {
        "Covert Skins" : [],
        "Classified Skins" : [],
        "Restricted Skins" : [],
        "Mil-Spec Skins" : []
        }
        # Parse main page
        page = get_parsed_page(case_page_url)
        # Isolate elements related to the actual skins
        page_content = page.find_all("div", {"class": "col-lg-4 col-md-6 col-widen text-center"})
        # Isolate single instances
        for page_content_single in page_content:
            # Skin url
            get_skin_url = page_content_single.find_all(href=re.compile('https://csgostash.com/skin/'))
            skin_url = str(get_skin_url).split('">')[0].split('"')[1]
            # Image URL
            get_image_url = page_content_single.img['src']
            image_url = get_image_url
            # Title
            get_title = page_content_single.h3
            title = f"{get_title.find_all('a')[0].text} | {get_title.find_all('a')[1].text}"
            # Rarity
            get_rarity = page_content_single.find("a", {"class": "nounderline"})
            rarity = get_rarity['href'].split('/skin-rarity/')[1]
            # Possible wears
            possible_wears = self._get_skin_wears(skin_url)
            # Description & Lore
            description,lore = self._get_skin_description_and_lore(skin_url)
            # Add
            if rarity == 'Covert':
                case_content['Covert Skins'] += [{"title" : title}, {"image" : image_url}, {"possible_wears" : possible_wears}, {"desc" : description}, {"lore" : lore}]
            elif rarity == 'Classified':
                case_content['Classified Skins'] += [{"title" : title}, {"image" : image_url}, {"possible_wears" : possible_wears}, {"desc" : description}, {"lore" : lore}]
            elif rarity == 'Restricted':
                case_content['Restricted Skins'] += [{"title" : title}, {"image" : image_url}, {"possible_wears" : possible_wears}, {"desc" : description}, {"lore" : lore}]
            elif rarity == 'Mil-Spec':
                case_content['Mil-Spec Skins'] += [{"title" : title}, {"image" : image_url}, {"possible_wears" : possible_wears}, {"desc" : description}, {"lore" : lore}]
        return case_content

    def _get_all_cases(self):
        csgo_cases = {}
        total_cases = 0
        # Parse main page
        page = get_parsed_page("https://csgostash.com/containers/skin-cases")
        # Isolate elements related to the actual cases
        page_content = page.find_all("div", {"class": "col-lg-4 col-md-6 col-widen text-center"})
        # Get total cases
        for page_content_single in page_content:
            total_cases += 1
        # Isolate single instances
        i = 1
        for page_content_single in page_content:
            title = page_content_single.h4.text
            url = page_content_single.a['href']
            image = page_content_single.img['src']
            print(f'Adding case: {title} [{i}/{total_cases}]')
            content = self._get_case_contents(url)
            csgo_cases[title] = [{"url" : url}, {"image_url" : image}, content]
            print(f'Done!\n')
            i += 1
            time.sleep(2) # Sleep to prevent overload
        # Return the dict
        return csgo_cases

    def get_case_skins(self):
        return self._get_all_cases()


@click.command()
@click.option('--method', default=1, type=click.IntRange(1,2), help="Sets the data saving method")
@click.option('--indent', default=2, help="Sets the JSON indentation level")
def dump_data(method, indent):
    """supr3me's csgostash-scraper
    Command-line syntax: python3 main.py --method 1 --indent 2
    Available methods:
    1 - Save in a single file
    2 - Save in separate files
    """
    # Preload data
    print('This process can take a while, please be patient..')
    ch = CasesHandler()
    data_to_dump = ch.get_case_skins()

    # Save output onto data folder, create one if it doesn't exist
    if os.path.exists('data'):
        os.chdir('data')
    else:
        os.mkdir('data')
        os.chdir('data')

    if method == 1: # Dump into single file
        with open('output.json', 'w') as fp:
            json.dump(data_to_dump, fp, indent=indent)
        print("\nFinished! Data saved to 'data\output.json'")
    elif method == 2: # Dump into separate case files
        for case in data_to_dump:
            filename = str(case).lower().replace(" ","_")
            with open(f'{filename}.json', 'w') as fp:
                json.dump(data_to_dump[case], fp, indent=indent)
            print(f"Creating 'data\{filename}.json'")
        print("Finished!")

if __name__ == '__main__':
    dump_data()
