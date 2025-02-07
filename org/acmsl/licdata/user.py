"""
org/acmsl/licdata/user.py

This file defines the User class.

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

from pythoneda.shared import (
    attribute,
    Entity,
    EventReference,
    filter_attribute,
    primary_key_attribute,
    sensitive,
)
from typing import List


class User(Entity):
    """
    Represents an user.

    Class name: User

    Responsibilities:
        - Contains metadata about an user.

    Collaborators:
        - None
    """

    def __init__(
        self, email: str, password: str, eventHistory: List[EventReference] = []
    ):
        """
        Creates a new User instance.
        :param email: The email.
        :type email: str
        :param password: The password
        :type password: str
        :param eventHistory: The event history.
        :type eventHistory: List[pythoneda.shared.EventReference]
        """
        self._email = email
        self._password = password
        super().__init__(eventHistory=eventHistory)

    @property
    @filter_attribute
    def email(self) -> str:
        """
        Retrieves the email.
        :return: Such value.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, newValue: str):
        """
        Specifies a new email.
        :param newValue: The new email address.
        :type newValue: str
        """
        self._email = newValue

    @property
    @sensitive
    def password(self) -> str:
        """
        Retrieves the password.
        :return: Such value.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, newValue):
        """
        Specifies a new password.
        :param newValue: The new password.
        :type newValue: str
        """
        self._password = newValue
