import re
import requests
from bs4 import BeautifulSoup
import json
import time
import click
import os

class ItemHandler:

    def _get_skin_title(self, page_url):
        """Returns skin title"""
        # Parse page
        page = PageHandler().get_parsed_page(page_url)
        # Extract title from meta
        title = page.find("meta", property="og:title")
        title = title['content'].split(' - CS:GO Stash')[0]
        # Return
        return title

    def _get_skin_url(self, page_context):
        """Returns skin URL"""
        try:
            skin_url = page_context.find_all(href=re.compile('https://csgostash.com/skin/'))
            skin_url = str(skin_url).split('">')[0].split('"')[1]
        except IndexError or TypeError:
            skin_url = page_context.h3
            skin_url = skin_url.a['href']
        # Return
        return skin_url

    def _get_skin_image_url(self, page_url):
        """Returns skin image url"""
        # Parse page
        page = PageHandler().get_parsed_page(page_url)
        # Extract image from meta
        image_url = page.find("meta", property="og:image")
        image_url = image_url['content']
        # Return
        return image_url

    def _get_skin_collection(self, page_url):
        # Parse page
        page = PageHandler().get_parsed_page(page_url)
        # Get case (or collection) name(s)
        collections = []
        collection_p = page.find_all("p", {"class": "collection-text-label"})
        for collection in collection_p:
            collections.append(collection.text)
        return collections

    def _get_skin_rarity(self, page_url):
        """Returns skin rarity"""
        # Parse page
        page = PageHandler().get_parsed_page(page_url)
        # Isolate elements related to rarity
        div = page.find("div", {"class": "well result-box nomargin"})
        rarity = div.find("p", {"class": "nomargin"})
        rarity = rarity.text
        # Return
        return rarity

    def _get_skin_description_and_lore(self, page_url):
        """Returns skin description and lore"""
        possible_wears = []
        # Parse page
        page = PageHandler().get_parsed_page(page_url)
        page_paragraphs = page.find_all("p")
        # Set default values
        description = "This item has no description"
        lore = "This item has no lore"
        # Replace them if possible
        for paragraph in page_paragraphs:
            if paragraph.strong != None:
                if 'Description' in paragraph.strong.text:
                    description = paragraph.text
                    description = description.split(': ')[1]
                elif 'Flavor Text' in paragraph.strong.text:
                    lore = paragraph.text
                    lore = lore.split(': ')[1]
        # Return
        return description,lore

    def _get_skin_wears(self, page_url):
        """Returns skin possible wears and their preview images"""
        possible_wears = []
        # Parse page
        page = PageHandler().get_parsed_page(page_url)
        # Isolate elements related to the skin wear
        div = page.find_all("div", {"class": "marker-value cursor-default"})
        # If skin has no wear, mark it as Vanilla
        is_vanilla = False
        try:
            min_wear = div[0].text
            max_wear = div[1].text
        except IndexError:
            is_vanilla = True

        wear_img = []
        for url in page.find_all("a"):
            if url.get('data-hoverimg') != None:
                wear_img.append(url.get('data-hoverimg'))

        if len(wear_img) == 0: # Vanilla skin, get default skin image
            wear_img.append(self._get_skin_image_url(page_url))

        # Define possible wears
        if is_vanilla:
            possible_wears.append("vanilla")
        else:
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
        # Zip lists
        possible_wears = dict(zip(possible_wears, wear_img))
        # Return
        return possible_wears

    def _get_skin_details(self, page_context):
        """Returns every skin detail"""
        # Set variables that need page context
        skin_url = self._get_skin_url(page_context)
        # Set variables that need skin url
        rarity = self._get_skin_rarity(skin_url)
        image = self._get_skin_image_url(skin_url)
        title = self._get_skin_title(skin_url)
        possible_wears = self._get_skin_wears(skin_url)
        desc,lore = self._get_skin_description_and_lore(skin_url)
        collection = self._get_skin_collection(skin_url)
        return rarity,skin_url,image,title,possible_wears,desc,lore,collection

    def _get_special_items(self, page_url):
        """Retrieves all rare special items"""
        special_items = {}
        item_frames = PageHandler().get_item_frames(page_url)
        total_items = len(item_frames)
        i=0
        # Get each item individually
        for frame in item_frames:
            i+=1
            if i == 1:
                continue
            # Set skin details
            rarity,skin_url,image,title,possible_wears,desc,lore,collection = self._get_skin_details(frame)
            skin_details = dict(title=title,url=skin_url,image=image,possible_wears=possible_wears,desc=desc,lore=lore)
            special_items[title] = skin_details
            print(f'[+] [{i-1}/{total_items-1}] {title}')
        return special_items

class CaseDataHandler:

    def _get_containers_case_content(self, page_url, case):
        """Returns entire case contents"""
        XRAY_PACKAGE_PAGE = 'https://csgostash.com/case/292/X-Ray-P250-Package'
        case_content = {
        "Rare Special Items": [],
        "Covert Skins" : [],
        "Classified Skins" : [],
        "Restricted Skins" : [],
        "Mil-Spec Skins" : []
        }
        item_frames = PageHandler().get_item_frames(page_url)
        # Get each skin individually
        total_skins = len(item_frames)
        i=0
        for frame in item_frames:
            i+=1
            if i == 1 and page_url != XRAY_PACKAGE_PAGE: # Special Items page frame
                page_url = frame.a['href']
                print('[=] Rare Special Items')
                special_items = ItemHandler()._get_special_items(page_url)
                for special_item in special_items:
                    case_content['Rare Special Items'].append(special_items[special_item])
                print('[=] Weapon Skins')
                continue
            # Set skin details
            rarity,skin_url,image,title,possible_wears,desc,lore,collection = ItemHandler()._get_skin_details(frame)
            skin_details = dict(title=title,url=skin_url,image=image,possible_wears=possible_wears,desc=desc,lore=lore)
            # Add to case_content separated by rarity
            print(f'[+] [{i-1}/{total_skins-1}] {title}')
            if 'Covert' in rarity:
                case_content['Covert Skins'].append(skin_details)
            elif 'Classified' in rarity:
                case_content['Classified Skins'].append(skin_details)
            elif 'Restricted' in rarity:
                case_content['Restricted Skins'].append(skin_details)
            elif 'Mil-Spec' in rarity:
                case_content['Mil-Spec Skins'].append(skin_details)

        return case_content

    def _get_containers_case_(self):
        """Retrieves all the cases available and their info"""
        PAGE_CASES = 'https://csgostash.com/containers/skin-cases'
        csgo_cases = {}
        item_frames = PageHandler().get_item_frames(PAGE_CASES)
        # Get each case individually
        for frame in item_frames:
            title = frame.h4.text
            url = frame.a['href']
            image = frame.img['src']
            csgo_cases[title] = dict(url=url, image_url=image)

        return csgo_cases

    def add_cases(self, method, indent):
        """Adds cases to the database"""
        cases = self._get_containers_case_()
        total_cases = len(cases)
        i=0
        print('\n[*] Retrieving cases:')
        for case in cases:
            i+=1
            print(f'\n[{i}/{total_cases}] Adding {case} contents:\n')
            content = self._get_containers_case_content(cases[case]['url'], case)
            cases[case]['content'] = content
            time.sleep(1) # Sleep to prevent overload
        # Dump data
        if method == 1:
            with open('output.json', 'w') as fp:
                json.dump(cases, fp, indent=indent)
                print(f'Wrote to file: {fp.name}')
        elif method == 2:
            for case in cases:
                filename = str(case).lower().replace(" ","_")
                with open(f'{filename}.json', 'w') as fp:
                    json.dump(cases[case], fp, indent=indent)
                    print(f'Wrote to file: {fp.name}')
        elif method == 3:
            with open('output.json', 'w') as fp:
                json.dump(cases, fp, indent=indent)
                print(f'Wrote to file: {fp.name}')
            for case in cases:
                filename = str(case).lower().replace(" ","_")
                filename = filename.replace(":","")
                with open(f'{filename}.json', 'w') as fp:
                    json.dump(cases[case], fp, indent=indent)
                    print(f'Wrote to file: {fp.name}')
class PageHandler:

    def get_parsed_page(self, url):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    def get_item_frames(self, url):
        """Retrieves item frame contents"""
        page = PageHandler().get_parsed_page(url)
        _item_frames =  page.find_all("div", {"class": "col-lg-4 col-md-6 col-widen text-center"})
        item_frames = []
        for item_frame in _item_frames:
            item_frames.append(item_frame)
        return item_frames

    def get_dropdown_items(self, tree):
        """Retrieves dropdown menu item links"""
        page = PageHandler().get_parsed_page('https://csgostash.com/')
        _dropdown_items = page.find_all("li", {"class": "dropdown"})
        dropdown_items = []
        for item in _dropdown_items:
            if item.a.text == tree:
                for link in item.find_all("a"):
                    dropdown_items.append(link.get('href'))
        dropdown_items.pop(0) # Delete '#' entry
        return dropdown_items

@click.command()
@click.option('--method', default=1, type=click.IntRange(1,3), help="Sets the data saving method")
@click.option('--indent', default=2, help="Sets the JSON indentation level")
def dump_data(method, indent):
    """supr3me's csgostash-scraper
    Command-line syntax: python3 main.py --method 1 --indent 2
    Available methods:
    1 - Save in a single file
    2 - Save in separate files
    3 - Save in single & separate files
    """

    # Save output onto data folder, create one if it doesn't exist
    if os.path.exists('data'):
        os.chdir('data')
    else:
        os.mkdir('data')
        os.chdir('data')

    # Save Cases
    CaseDataHandler().add_cases(method, indent)

if __name__ == '__main__':
    dump_data()
