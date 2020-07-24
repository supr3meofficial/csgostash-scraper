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


class RarityColour:

    colours = {
        'Consumer Grade': '0xafafaf',
        'Base Grade': '0xafafaf',

        'Industrial Grade': '0x6496e1',

        'Mil-Spec': '0x177cc7',
        'High Grade': '0x177cc7',

        'Restricted': '0x872de0',
        'Remarkable': '0x872de0',

        'Classified': '0xc917e0',
        'Exotic': '0xc917e0',

        'Covert': '0xe7191b',
        'Extraordinary': '0xe7191b',

        'Rare Special Item': '0xa47719',

        'Contraband': '0x886a08'
    }

    def __init__(self, colour):
        self.colour = colour
        self.color = colour
        pass

    def __str__(self):
        return str(self.colour)

    @staticmethod
    def get(self):
        """Returns the colour dictionary"""
        return self.colours

    @classmethod
    def _from_string(cls, string: str):
        """Constructs a RarityColour object from a string
        This is used by the scraper to set colour based on the item rarity attribute
        """
        for colour, v in cls.colours.items():
            if string.split(' ')[0] in colour:
                return cls(v)


RarityColor = RarityColour
