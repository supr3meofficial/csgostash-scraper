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
from ._utils import RarityColour


class Item:
    """Represents an Item

    Base class for all Item derived objects:
            - Weapon Skin
            - Sticker
            - Agent Patches
            - Music Kits
            - Grafitti
            - Key
            - Pin
    """
    __slots__ = ('_spawned', 'title', 'description', 'lore', 'date_added',
                 'collection', 'collections', 'found_in', 'rarity')

    def __init__(self, title: str, desc: str, lore: str, date_added: str, collection: list, found_in: list, rarity: str):
        self.title = title
        self.description = desc
        self.lore = lore
        self.date_added = date_added
        self.collection = collection
        self.collections = collection
        self.found_in = found_in
        self.rarity = rarity
        # Defines the object as manually spawned. This variable should not be changed manually
        self._spawned = True

    @classmethod
    def __base__(cls):
        """Get base class."""

        return cls

    def __repr__(self):
        return "<Item name='%s' custom='%s'>" % (self.title, self._spawned)

    def __str__(self):
        return self.title

    def __eq__(self, other):
        return (
            isinstance(other, self.__base__()) and
            all([getattr(other, key) == getattr(self, key)
                 for key in self.__slots__])
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._spawned, self.title))

    def get_rarity_colour(self):
        """Returns the item rarity colour"""
        return str(RarityColour._from_string(self.rarity))

    @classmethod
    def _from_data(cls, d):
        """Object constructor from dictionary
        This method is called by the scraper and should not be called manually
        """
        name = d['name']
        description = d['desc']
        lore = d['lore']
        date_added = d['date_added']
        collection = d['collection']
        rarity = d['rarity']

        _cls = cls(name, description, lore, date_added, collection, collection, rarity)
        _cls._spawned = False
        return _cls
