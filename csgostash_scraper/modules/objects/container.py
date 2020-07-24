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


class Container:
    """Represents a container
    CSGOStash Page: https://csgostash.com/containers/

    Base class for all derived container objects:
            - Skin Cases
            - Souvenir Packages
            - Sticker Capsules
            - Autograph Capsules
            - Gift Packages

    There is no need to create one of these manually
    """
    __slots__ = ('_spawned', 'name', 'icon')

    def __init__(self, name: str, icon: str):
        self.name = name
        self.icon = icon
        # Defines the object as manually spawned. This variable should not be changed manually
        self._spawned = True

    @classmethod
    def __base__(cls):
        """Get base class."""

        return cls

    def __repr__(self):
        return "<Container name='%s' custom='%s'>" % (self.name, self._spawned)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (
            isinstance(other, self.__base__()) and
            all([getattr(other, key) == getattr(self, key)
                 for key in self.__slots__])
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self._spawned, self.name, self.icon))
