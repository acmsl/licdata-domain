"""
org/acmsl/licdata/prelicense.py

This file defines the Prelicense class.

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

from pythoneda.shared import Entity, EventReference, primary_key_attribute, attribute
from typing import List


class Prelicense(Entity):
    """
    Represents a prelicense.

    Class name: Prelicense

    Responsibilities:
        - Represents a prelicense, i.e. a floating license.

    Collaborators:
        - Order: A Prelicense belongs to an order.
    """

    def __init__(
        self,
        orderId: str,
        seats: int,
        duration: int,
        eventHistory: List[EventReference] = [],
    ):
        """
        Creates a new Prelicense instance.
        :param id: The id.
        :type id: str
        :param orderId: The order id.
        :type orderId: str
        :param seats: The number of seats for this prelicense.
        :type seats: int
        :param duration: The duration.
        :type duration: int
        :param eventHistory: The event history.
        :type eventHistory: List[pythoneda.shared.EventReference]
        """
        self._order_id = orderId
        self._seats = seats
        self._duration = duration
        super().__init__(eventHistory=eventHistory)

    @property
    @primary_key_attribute
    def order_id(self) -> str:
        """
        Retrieves the order id.
        :return: Such information.
        :rtype: str
        """
        return self._order_id

    @property
    @attribute
    def seats(self) -> int:
        """
        Retrieves the number of seats.
        :return: Such value.
        :rtype: int
        """
        return self._seats

    @seats.setter
    def seats(self, newValue: int):
        """
        Specifies a new value for the number of seats.
        :param newValue: The new number of seats.
        :type newValue: int
        """
        self._seats = newValue

    @property
    @attribute
    def duration(self) -> int:
        """
        Retrieves the duration.
        :return: Such value.
        :rtype: int
        """
        return self._duration

    @duration.setter
    def duration(self, newValue: int):
        """
        Specifies a new duration.
        :param newValue: The new duration of the order.
        :type newValue: int
        """
        self._duration = newValue
