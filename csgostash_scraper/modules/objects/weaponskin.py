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

from random import randint
from random import choice as randchoice

from .item import Item


class WeaponSkin(Item):
    """Represents a Weapon Skin

    CSGOStash Page: https://csgostash.com/skin/(id)/(name)
    """
    __slots__ = ('_spawned', 'weapon_type', 'title', 'description', 'lore', 'date_added', 'collection', 'collections',
                 'found_in', 'rarity', 'wears', 'can_be_stattrak', 'can_be_souvenir', 'is_stattrak')

    def __init__(self, weapon_type: str, title: str, desc: str, lore: str, date_added: str, collection: list, found_in: list, rarity: str, wears: dict):
        super().__init__(title, desc, lore, date_added, collection, found_in, rarity)
        self.weapon_type = weapon_type
        self.wears = wears
        self.can_be_stattrak = False
        self.can_be_souvenir = False

    @classmethod
    def __base__(cls):
        """Get base class."""

        return cls

    def __eq__(self, other):
        return (
            isinstance(other, self.__base__()) and
            all([getattr(other, key) == getattr(self, key)
                 for key in self.__slots__])
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Item.WeaponSkin name='%s' custom='%s'>" % (self.title, self._spawned)

    def __hash__(self):
        return hash((self._spawned, self.title))

    @property
    def name(self):
        if self.weapon_type == 'Knife' or self.weapon_type == 'Gloves':
            return f'★ {self.title}'
        return self.title

    @name.setter
    def name(self, value):
        self.title = value

    def _get_random_wear(self):
        """Helper function that returns a random item wear"""
        return randchoice(list(self.wears.keys()))

    def _set_prefix(self):
        """Helper function to set StatTrak or Souvenir prefix in random skin variation"""
        if self.can_be_stattrak:
            st_odds = randint(0, 10)
            if st_odds == 10:
                self.is_stattrak = True
                return 'StatTrak™ '

        if self.can_be_souvenir:
            return 'Souvenir '

        return ''

    def get_random_variation(self):
        """Returns a random skin variation.
        This is used to return an item entity as you would have in your Steam Inventory
        An example variation would be ("AK-47 | Asiimov (Field-Tested)",<wear_img>)

        Returns a tuple of skin name and skin image
        """
        wear = self._get_random_wear()
        image = self.wears[wear]

        if wear == 'vanilla':
            wear = ''
        else:
            wear = f'({wear})'
        variation = f'{self._set_prefix()} {self.name} {wear}'.strip()
        return (variation, image)

    @classmethod
    def _from_data(cls, d):
        """Object constructor from dictionary
        This method is called by the scraper and should not be called manually
        """
        weapon_type = d['weapon_type']
        title = d['title']
        description = d['desc']
        lore = d['lore']
        date_added = d['date_added']
        collection = d['collection']
        found_in = d['found_in']
        rarity = d['rarity']
        wears = d['wears']

        _cls = cls(weapon_type, title, description, lore, date_added,
                   collection, found_in, rarity, wears)
        _cls._spawned = False
        return _cls
