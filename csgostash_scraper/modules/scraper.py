# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2020 supr3me

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
import requests
from bs4 import BeautifulSoup


class ScraperException(Exception):
    """Base exception class for the scraper"""
    pass


class ItemHasNoDescription(ScraperException):
    """Exception that is thrown if the item has no description"""
    pass


class ItemHasNoLore(ScraperException):
    """Exception that is thrown if the item has no lore"""
    pass

class ItemHasNoDateAdded(ScraperException):
    """Exception that is thrown if the item has no date_added"""
    pass

class ItemNoCollection(ScraperException):
    """Exception that is thrown if the item does not belong in a collection"""
    pass


class ItemHasNoWear(ScraperException):
    """Exception that is thrown if the item does have wear"""
    pass


class ItemNoStattrakSouvenir(ScraperException):
    """Exception that is thrown if the item does not come in StatTrak or Souvenir"""
    pass


class PageNoPagination(ScraperException):
    """Exception that is thrown if a page does no have pagination"""
    pass


class PageHandler:

    @staticmethod
    def get_parsed_page(url: str):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        return BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    @staticmethod
    def get_item_frames(url: str, filtered_value: str):
        """Retrieves item frame contents"""
        page = PageHandler.get_parsed_page(url)
        item_frames = page.find_all("div", {"class": filtered_value})

        for item_frame in item_frames:
            yield item_frame

    @staticmethod
    def get_dropdown_items(filtered_value: str):
        """Retrieves dropdown menu item links that match the filter string"""
        page = PageHandler.get_parsed_page('https://csgostash.com/')
        dropdown_items = page.find_all("li", {"class": "dropdown"})

        for item in dropdown_items:
            if item.a.text == filtered_value:
                for link in item.find_all("a"):
                    if link.get('href') != '#':
                        yield link.get('href')

    @staticmethod
    def get_pagination(url: str):
        """Retrieves the pagination list"""

        def gen_url(url):
            yield url

        def gen_pagination(url):
            page = PageHandler.get_parsed_page(url)
            pagination_ul = page.find_all("ul", {"class": "pagination"})
            _ = []

            for item in pagination_ul:
                for a in item.find_all("a"):
                    href = a['href']
                    if href not in _:
                        yield a['href']
                    _.append(href)
                del _
                break

        yield from gen_url(url)
        yield from gen_pagination(url)


class RetrieveObject:
    """Abstract class for object data scraping

    Base class for:
            - RetrieveCase
            - RetrieveSouvenirPackage
            - RetrieveWeaponSkin
    """

    def __init__(self, parsed_page):
        self.parsed_page = parsed_page

    @classmethod
    def _from_page_url(cls, url: str):
        page = PageHandler.get_parsed_page(url)
        return cls(page)

    def get_title(self):
        """Returns item title"""

        # Extract title from meta
        title = self.parsed_page.find("meta", property="og:title")
        title = title['content'].split('- CS:GO Stash')[0].strip()

        return title

    def get_image_url(self):
        """Returns skin image url as a string"""

        # Extract image from meta
        image_url = self.parsed_page.find("meta", property="og:image")
        image_url = image_url['content']

        return image_url


class RetrieveWeaponSkin(RetrieveObject):

    def __init__(self, parsed_page):
        super().__init__(parsed_page)

    @staticmethod
    def get_all_urls(url, *, has_special_frames=True):
        """Generator that retrieves all weapon skin page urls"""

        def get_args(url):
            item_frames = PageHandler.get_item_frames(url, 'details-link')
            get_all_pages = PageHandler.get_pagination(url)
            return item_frames, get_all_pages

        def gen1(item_frames):
            for frame in item_frames:
                href = frame.a['href']
                yield from gen2(get_args(href)[0], get_args(href)[1])
                break

        def gen2(item_frames, pages):
            for _ in pages:
                for frame in item_frames:
                    href = frame.a['href']
                    if url in href:
                        continue
                    yield href

        if has_special_frames:
            yield from gen1(get_args(url)[0])
        yield from gen2(get_args(url)[0], get_args(url)[1])

    def get_description(self):
        """Returns skin description as string"""

        # Find description from page paragraphs
        page_paragraphs = self.parsed_page.find_all("p")

        for paragraph in page_paragraphs:
            if paragraph.strong != None:
                if 'Description' in paragraph.strong.text:
                    description = paragraph.text
                    return description.split('Description:')[1].strip()
        else:
            raise ItemHasNoDescription()

    def get_flavor_text(self):
        """Returns skin flavor text as string"""

        # Find lore from page paragraphs
        page_paragraphs = self.parsed_page.find_all("p")

        for paragraph in page_paragraphs:
            if paragraph.strong != None:
                if 'Flavor Text:' in paragraph.strong.text:
                    description = paragraph.text
                    return description.split('Flavor Text:')[1].strip()
        else:
            raise ItemHasNoLore()

    get_lore = get_flavor_text

    def get_date_added(self):
        """Returns skin date_added as string"""

        # Find date_added from page paragraphs
        page_paragraphs = self.parsed_page.find_all("p")

        for paragraph in page_paragraphs:
            if paragraph.strong != None:
                if 'Added:' in paragraph.strong.text:
                    description = paragraph.text
                    return description.split('Added:')[1].strip()
        else:
            raise ItemHasNoDateAdded()

    def get_collection(self, filters=['Collection']):
        """Returns the collection name(s) as a list of strings
        It can also return the containers the item is found in, by setting the filtered_value to 'Case'
        """

        found_values = []
        # Collection info is found inside a dedicated class attribute, so we extract it from there
        page_paragraphs = self.parsed_page.find_all(
            "p", {"class": "collection-text-label"})

        for value in page_paragraphs:
            for filtered_value in filters:
                if filtered_value in value.text:
                    found_values.append(value.text)
                    break
            if found_values != []:
                break
        else:
            if filtered_value == 'Collection':
                raise ItemNoCollection()

        return found_values

    get_collections = get_collection

    def get_rarity(self):
        """Returns the skin rarity as a string"""

        div = self.parsed_page.find(
            "div", {"class": "well result-box nomargin"})
        rarity = div.find("p", {"class": "nomargin"})
        rarity = str(rarity.text).strip()

        return rarity

    def get_stattrak_souvenir_info(self):
        """Returns the 'StatTrak Available' or 'Souvenir Available' strings"""

        div = self.parsed_page.find(
            "div", {"class": "well result-box nomargin"})
        results = div.find_all("p", {"class": "nomargin"})

        for result in results:
            if 'Available' in result.text:
                return result.text
        else:
            raise ItemNoStattrakSouvenir()

    def get_wears(self):
        """Returns a dictionary of possible skin wears

        Dict Format: 
        """
        possible_wears = []

        # Isolate elements related to the skin wear
        div = self.parsed_page.find_all(
            "div", {"class": "marker-value cursor-default"})

        try:
            min_wear = float(div[0].text)
            max_wear = float(div[1].text)
        except IndexError:
            raise ItemHasNoWear()

        wear_img = []
        for url in self.parsed_page.find_all("a"):
            if url.get('data-hoverimg') != None:
                wear_img.append(url.get('data-hoverimg'))

        # Define possible wears
        if min_wear < 0.07 and max_wear > 0.00:
            possible_wears.append("Factory New")
        if min_wear < 0.15 and max_wear > 0.07:
            possible_wears.append("Minimal Wear")
        if min_wear < 0.38 and max_wear > 0.15:
            possible_wears.append("Field-Tested")
        if min_wear < 0.45 and max_wear > 0.38:
            possible_wears.append("Well-Worn")
        if min_wear < 1 and max_wear > 0.45:
            possible_wears.append("Battle-Scarred")

        possible_wears = dict(zip(possible_wears, wear_img))

        return possible_wears


class RetrieveCollection(RetrieveObject):

    def __init__(self, parsed_page):
        self.parsed_page = parsed_page

    @staticmethod
    def get_all_urls():
        """Generator that retrieves all collection page urls"""
        dropdown_items = PageHandler.get_dropdown_items('Collections')

        for url in dropdown_items:
            yield url

    def get_title(self):
        """Returns item title"""

        # Extract title from meta
        title = self.parsed_page.find("meta", property="og:title")
        title = title['content'].split('Skins - CS:GO Stash')[0].strip()

        return title


class RetrieveCase(RetrieveObject):

    def __init__(self, parsed_page):
        self.parsed_page = parsed_page

    @staticmethod
    def get_all_urls():
        """Generator that retrieves all skin case page urls"""
        PAGE_CASES = 'https://csgostash.com/containers/skin-cases'

        item_frames = PageHandler.get_item_frames(
            PAGE_CASES, 'well result-box nomargin')

        for frame in item_frames:
            try:
                yield frame.a['href']
            except TypeError:
                continue

    def get_title(self):
        """Returns item title"""

        # Extract title from meta
        title = self.parsed_page.find("meta", property="og:title")
        title = title['content'].split('Skins - CS:GO Stash')[0].strip()

        return title


class RetrieveSouvenirPackage(RetrieveObject):

    def __init__(self, page_url):
        self.parsed_page = PageHandler.get_parsed_page(page_url)
        self.page_url = page_url

    @classmethod
    def _from_page_url(cls, url: str):
        return cls(url)

    @staticmethod
    def get_all_urls():
        """Generator that retrieves all souvenir package page urls"""
        PAGE_SOUVENIR_PACKAGES = 'https://csgostash.com/containers/souvenir-packages'
        pages = PageHandler.get_pagination(PAGE_SOUVENIR_PACKAGES)

        for page in pages:
            for frame in PageHandler.get_item_frames(page, 'well result-box nomargin'):
                try:
                    yield frame.a['href']
                except TypeError:
                    continue

    def get_title(self):
        """Returns item title"""

        # Extract title from meta
        title = self.parsed_page.find("meta", property="og:title")
        title = title['content'].split('- CS:GO Stash')[0].strip()

        return title

    def get_collection_url(self):
        """Returns the souvenir package collection url and name as lists"""
        for frame in PageHandler.get_item_frames(self.page_url, 'containers-details-link'):
            return frame.a['href']

    def get_collection_name(self):
        """Returns the souvenir package collection url and name as lists"""
        for frame in PageHandler.get_item_frames(self.page_url, 'containers-details-link'):
            return frame.a.text
