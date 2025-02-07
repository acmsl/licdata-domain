"""
org/acmsl/licdata/incident.py

This file defines the Incident class.

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

from pythoneda.shared import Entity, EventReference, primary_key_attribute
from typing import List


class Incident(Entity):
    """
    Represents a incident.

    Class name: Incident

    Responsibilities:
        - Contains relevant information about an incident.

    Collaborators:
        - License: Each incident is related to a license.
        - PC: Each incident is related to a PC.
    """

    def __init__(
        self, licenseId: str, pcId: str, eventHistory: List[EventReference] = []
    ):
        """
        Creates a new Incident instance.
        :param licenseId: The id of the license.
        :type licenseId: str
        :param pcId: The id of the PC.
        :type pcId: str
        :param eventHistory: The event history.
        :type eventHistory: List[pythoneda.shared.EventReference]
        """
        self._license_id = licenseId
        self._pc_id = pcId
        super().__init__(eventHistory=eventHistory)

    @property
    @primary_key_attribute
    def license_id(self) -> str:
        """
        Retrieves the license id.
        :return: Such id.
        :rtype: str
        """
        return self._license_id

    @property
    @primary_key_attribute
    def pc_id(self) -> str:
        """
        Retrieves the PC id.
        :return: Such id.
        :rtype: str
        """
        return self._pc_id
