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

import os
import pickle
import json

from csgostash_scraper.modules.objects.souvenirpackage import SouvenirPackage
from csgostash_scraper.modules.objectfactory import CollectionFactory, ContainerFactory
from csgostash_scraper.modules.scraper import RetrieveCollection, RetrieveCase, RetrieveSouvenirPackage

main_dir = os.getcwd()


def root_path():
    return os.path.abspath(main_dir)


data_path = os.path.join(root_path(), 'data')


def filename(name):
    name_replacements = {'II': '2',
                         ':': '',
                         ' ': '_'}

    for i in name_replacements:
        name = name.replace(i, name_replacements[i])

    return name.lower()


def fmt_dict(container):

    rare = []
    covert = []
    classified = []
    restricted = []
    milspec = []
    industrial = []
    consumer = []

    for item in container:
        itemdict = {"name": item.name,
                    "desc": item.description,
                    "lore": item.lore,
                    "can_be_souvenir": item.can_be_souvenir,
                    "can_be_stattrak": item.can_be_stattrak,
                    "wears": item.wears}

        if "★" in item.name:
            rare.append(itemdict)
        else:
            rar = {"Extraordinary": rare,
                   "Covert": covert,
                   "Classified": classified,
                   "Restricted": restricted,
                   "Mil-Spec": milspec,
                   "Industrial": industrial,
                   "Consumer": consumer}

            rar[item.rarity].append(itemdict)

    content = {"Rare Special Items": rare,
               "Covert Skins": covert,
               "Classified Skins": classified,
               "Restricted Skins": restricted,
               "Mil-Spec Skins": milspec,
               "Industrial Grade Skins": industrial,
               "Consumer Grade Skins": consumer}

    fmt_dict = {"name": container.name,
                "image_url": container.icon,
                "content": content}

    return fmt_dict


def save_data(*, obj='', save_to='', overwrite=False):
    """Retrieves data and saves it as a pickle and json"""

    # Set file save location
    object_retrieve = {
        "collections": RetrieveCollection,
        "cases": RetrieveCase,
        "souvenir_packages": RetrieveSouvenirPackage
    }

    object_factory = {
        "collections": CollectionFactory.create_collection,
        "cases": ContainerFactory.create_case,
        "souvenir_packages": ContainerFactory.create_souvenir_package
    }

    object_retrieve = object_retrieve[obj]
    object_factory = object_factory[obj]

    if save_to == '':
        save_to = obj
        # Set CWD to root path
        os.chdir(root_path())
        os.chdir(os.path.join(data_path, save_to))
    for url in object_retrieve.get_all_urls():
        # Retrieve title for filename and overwrite checks
        _ = object_retrieve._from_page_url(url)
        fname = filename(_.get_title())
        del _

        for ext in ('pickle', 'json'):
            if (overwrite) or (not os.path.isfile(f'{ext}/{fname}.{ext}')):
                # Create object
                if obj != 'souvenir_packages':
                    container = object_factory(url)
                else:
                    container = object_factory(
                        url, path=f"{data_path}/collections/pickle/")
                # Dump
                if ext == 'pickle':
                    with open(f'{ext}/{fname}.{ext}', 'wb') as fp:
                        pickle.dump(container, fp)
                elif ext == 'json':
                    with open(f'{ext}/{fname}.{ext}', 'w') as fp:
                        if type(container) == SouvenirPackage and container.has_multiple_collections:
                            fmtdict = {}
                            for col in container.collection:
                                fmtdict[col.name] = fmt_dict(col)
                        else:
                            fmtdict = fmt_dict(container)
                        json.dump(fmtdict, fp, indent=2,
                                  ensure_ascii=False)


to_be_scraped = ("collections",
                 "cases",
                 "souvenir_packages")

for obj in to_be_scraped:
    save_data(obj=obj, overwrite=True)
