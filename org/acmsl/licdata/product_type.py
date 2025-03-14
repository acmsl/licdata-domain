"""
org/acmsl/licdata/product_type.py

This file defines the ProductType class.

Copyright (C) 2023-today ACM S.L. Licdata-Domain

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from pythoneda.shared import attribute, Entity, EventReference, primary_key_attribute
from typing import List


class ProductType(Entity):
    """
    Represents a product type.

    Class name: ProductType

    Responsibilities:
        - Contains metadata shared by a group of products.

    Collaborators:
        - None
    """

    def __init__(
        self, name: str, version: str, eventHistory: List[EventReference] = []
    ):
        """
        Creates a new ProductType instance.
        :param name: The name.
        :type name: str
        :param version: The version.
        :type version: str
        :param eventHistory: The event history.
        :type eventHistory: List[pythoneda.shared.EventReference]
        """
        self._name = name
        self._version = version
        super().__init__(eventHistory=eventHistory)

    @property
    @primary_key_attribute
    def name(self) -> str:
        """
        Retrieves the name.
        :return: Such information.
        :rtype: str
        """
        return self._name

    @property
    @primary_key_attribute
    def version(self):
        """
        Retrieves the version.
        :return: Such information.
        :rtype: str
        """
        return self._version
