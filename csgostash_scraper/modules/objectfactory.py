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

import pickle
import logging
import os

from .scraper import PageHandler, RetrieveCollection, RetrieveCase, RetrieveSouvenirPackage, RetrieveWeaponSkin
from .scraper import ItemHasNoWear, ItemNoCollection, ItemNoStattrakSouvenir, ItemHasNoDescription, ItemHasNoLore
from .objects import Collection, SkinCase, SouvenirPackage, WeaponSkin

# logging.basicConfig(level=logging.DEBUG)


def filename(name):
    name_replacements = {'II': '2',
                         ':': '',
                         ' ': '_'}

    for i in name_replacements:
        name = name.replace(i, name_replacements[i])

    return name.lower()


class Factory:
    """Base Class for Factories
    All objects are created using scraped data from CSGOStash
    """
    pass


class ItemFactory(Factory):
    """Object Factory for Items"""
    @staticmethod
    def create_weaponskin(page_url):
        """Creates an Item.WeaponSkin object"""
        ws = RetrieveWeaponSkin._from_page_url(page_url)

        title = ws.get_title()

        try:
            description = ws.get_description()
        except ItemHasNoDescription:
            description = 'This item has no description.'

        try:
            lore = ws.get_flavor_text()
        except ItemHasNoLore:
            lore = 'This item has no Lore'

        try:
            collection = ws.get_collection()
        except ItemNoCollection:
            collection = 'This item does not belong to a Collection'

        found_in = ws.get_collection(['Case', 'Package', 'Collection'])

        try:
            wears = ws.get_wears()
        except ItemHasNoWear:
            wears = dict(vanilla=ws.get_image_url())

        get_rarity = ws.get_rarity()
        rarity = get_rarity.split(' ')[0]
        weapon_type = get_rarity.split(' ')[1]

        data_dict = dict(weapon_type=weapon_type, title=title, desc=description, lore=lore,
                         collection=collection, found_in=found_in, rarity=rarity, wears=wears)
        item = WeaponSkin._from_data(data_dict)

        try:
            stsouv = ws.get_stattrak_souvenir_info()
            if stsouv == 'StatTrak Available':
                item.can_be_stattrak = True
            elif stsouv == 'Souvenir Available':
                item.can_be_souvenir = True
        except ItemNoStattrakSouvenir:
            pass

        logging.debug(f'Created object: {repr(item)}')
        logging.info(f'Retrieving: {item.name}')

        return item


class CollectionFactory(Factory):
    """Object Factory for Collections"""
    @staticmethod
    def create_collection(page_url):
        """Creates a Collection object"""
        c = RetrieveCollection._from_page_url(page_url)

        name = c.get_title()
        icon = c.get_image_url()
        content = set()

        for url in RetrieveWeaponSkin.get_all_urls(page_url):
            item = ItemFactory.create_weaponskin(url)
            content.add(item)

        data_dict = dict(name=name, icon=icon, content=content)
        col = Collection._from_data(data_dict)

        logging.debug(f'Created object: {repr(col)}')
        logging.info(f'Adding retrieved items to \'{col.name}\'')

        return col


class ContainerFactory(Factory):
    """Object Factory for Containers"""
    @staticmethod
    def create_case(page_url):
        """Creates a Container.Case object"""
        c = RetrieveCase._from_page_url(page_url)

        name = c.get_title()
        icon = c.get_image_url()
        content = set()

        for url in RetrieveWeaponSkin.get_all_urls(page_url):
            item = ItemFactory.create_weaponskin(url)
            content.add(item)

        data_dict = dict(name=name, icon=icon, content=content)
        case = SkinCase._from_data(data_dict)

        logging.debug(f'Created object: {repr(case)}')
        logging.info(f'Adding retrieved items to \'{case.name}\'')

        return case

    @staticmethod
    def create_souvenir_package(page_url, collection_from_file=True, path=None):
        """Creates a Container.SouvenirPackage object"""
        sp = RetrieveSouvenirPackage._from_page_url(page_url)

        name = sp.get_title()
        icon = sp.get_image_url()
        collections = []

        # Internal collection object creation
        collection_urls = [sp.get_collection_url()]
        if collection_urls == [None]:
            # This only happens with the 'EMS One 2014 Souvenir Package' and the 'Dreamhack 2013 Souvenir Package'
            collection_urls = ['https://csgostash.com/collection/The+Dust+2+Collection', 'https://csgostash.com/collection/The+Safehouse+Collection', 'https://csgostash.com/collection/The+Lake+Collection',
                               'https://csgostash.com/collection/The+Italy+Collection', 'https://csgostash.com/collection/The+Train+Collection', 'https://csgostash.com/collection/The+Mirage+Collection']

        if not collection_from_file:
            # Create collection object. This does not save the collection
            for url in collection_urls:
                col = CollectionFactory.create_collection(url)
                collections.append(col)
        else:
            # Check each collection from URL
            for url in collection_urls:
                col = RetrieveCollection._from_page_url(url)
                # Load collection object from pickle file
                fname = filename(col.get_title())
                fpath = os.path.join(path, f'{fname}.pickle')
                if os.path.isfile(fpath):
                    with open(fpath, 'rb') as fp:
                        col = pickle.load(fp)
                        collections.append(col)
                # If it doesn't exist, go back and create one
                else:
                    ContainerFactory.create_souvenir_package(page_url, False)

        data_dict = dict(name=name, icon=icon, collection=collections)
        package = SouvenirPackage._from_data(data_dict)

        logging.debug(f'Created object: {repr(package)}')
        logging.info(f'Adding retrieved items to \'{package.name}\'')

        return package
