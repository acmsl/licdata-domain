"""
org/acmsl/licdata/client.py

This file defines the Client class.

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

from org.acmsl.licdata.events.clients import (
    BaseClientEvent,
    ClientAlreadyExists,
    ClientDeleted,
    DeleteClientRequested,
    ListClientsRequested,
    MatchingClientsFound,
    NewClientCreated,
    NewClientRequested,
    NoMatchingClientsFound,
)
from pythoneda.shared import (
    Entity,
    Event,
    EventListener,
    primary_key_attribute,
    attribute,
    EventListener,
    listen,
    Ports,
)
from typing import List, Optional


class Client(Entity, EventListener):
    """
    Represents a client.

    Class name: Client

    Responsibilities:
        - Contains all relevant information about a client.

    Collaborators:
        - None

    """

    def __init__(
        self,
        email: str,
        address: Optional[str] = None,
        contact: Optional[str] = None,
        phone: Optional[str] = None,
    ):
        """
        Creates a new Client instance.
        :param email: The email.
        :type email: str
        :param address: The address.
        :type address: Optional[str]
        :param contact: The contact.
        :type contact: Optional[str]
        :param phone: The phone.
        :type phone: Optional[str]
        """
        self._email = email
        self._address = address
        self._contact = contact
        self._phone = phone
        super().__init__()

    @classmethod
    def empty(cls):
        """
        Builds an empty instance. Required for unmarshalling.
        :return: An empty instance.
        :rtype: pythoneda.ValueObject
        """
        return cls(email="", address="", contact="", phone="")

    @property
    @primary_key_attribute
    def email(self) -> str:
        """
        Retrieves the email.
        :return: Such email address.
        :rtype: str
        """
        return self._email

    @property
    @attribute
    def address(self) -> str:
        """
        Retrieves the address.
        :return: Such address.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, newAddress: str):
        """
        Specifies a new address.
        :param newAddress: Such address.
        :type newAddress: str
        """
        self._address = newAddress

    @property
    @attribute
    def contact(self) -> str:
        """
        Retrieves the contact.
        :return: Such contact.
        :rtype: str
        """
        return self._contact

    @contact.setter
    def contact(self, newValue):
        """
        Specifies a new contact.
        :param newValue: Such contact.
        :type newValue: str
        """
        self._contact = newValue

    @property
    @attribute
    def phone(self):
        """
        Retrieves the phone.
        :return: Such phone.
        :rtype: str
        """
        return self._phone

    @phone.setter
    def phone(self, newValue):
        """
        Specifies a new phone.
        :param newValue: Such phone.
        :type newValue: str
        """
        self._phone = newValue

    @classmethod
    @listen(NewClientRequested)
    async def listen_NewClientRequested(
        cls, newClientRequested: NewClientRequested
    ) -> List[BaseClientEvent]:
        """
        Receives an event requesting the creation of a new client.
        :param newClientRequested: The request.
        :type newClientRequested: org.acmsl.licdata.events.NewClientRequested
        :return: The event representing a new client has been created.
        :rtype event: List[org.acmsl.licdata.events.clients.BaseClientEvent]
        """
        from .client_repo import ClientRepo

        cls.logger().info(f"New client requested: {newClientRequested}")

        result = []

        repo = Ports.instance().resolve_first(ClientRepo)

        existing_client = repo.find_by_pk({"email": newClientRequested.email})

        if existing_client is None:
            new_client_created = repo.insert(newClientRequested)

            result.append(new_client_created)
        else:
            result.append(
                ClientAlreadyExists(
                    id=existing_client.id,
                    email=existing_client.email,
                    address=existing_client.address,
                    contact=existing_client.contact,
                    phone=existing_client.phone,
                    previousEventIds=(
                        newClientRequested.previous_event_ids + [newClientRequested.id]
                    ),
                )
            )

        return result

    @classmethod
    @listen(ListClientsRequested)
    async def listen_ListClientsRequested(
        cls, event: ListClientsRequested
    ) -> List[Event]:
        """
        Receives an event requesting the listing of clients.
        :param event: The request.
        :type event: org.acmsl.licdata.events.ListClientsRequested
        :return: The event representing the outcome of the operation.
        :rtype event: List[pythoneda.shared.Event]
        """
        from .client_repo import ClientRepo

        result = []

        repo = Ports.instance().resolve_first(ClientRepo)

        existing_clients = repo.list()

        if len(existing_clients) == 0:
            no_matching_clients_found = NoMatchingClientsFound(
                {}, event.previous_event_ids + [event.id]
            )
            result.append(no_matching_clients_found)
        else:
            result.append(
                MatchingClientsFound(
                    existing_clients,
                    {},
                    event.previous_event_ids + [event.id],
                )
            )

        return result

    @classmethod
    @listen(DeleteClientRequested)
    async def listen_DeleteClientRequested(
        cls, event: DeleteClientRequested
    ) -> List[Event]:
        """
        Receives an event requesting the creation of a new client.
        :param event: The request.
        :type event: org.acmsl.licdata.events.DeleteClientRequested
        :return: The event representing a deleting a client has been requested.
        :rtype event: List[pythoneda.shared.Event]
        """
        from .client_repo import ClientRepo

        cls.logger().info(f"Delete client requested: {event}")

        result = []

        repo = Ports.instance().resolve_first(ClientRepo)

        existing_client = repo.find_by_id(event.entity_id)

        if existing_client is None:
            result.append(
                NoMatchingClientsFound(
                    {"id": event.entity_id},
                    event.previous_event_ids + [event.id],
                )
            )
        else:
            repo.delete(event.entity_id)

            client_deleted = ClientDeleted(
                existing_client.email,
                existing_client.address,
                existing_client.contact,
                existing_client.phone,
                event.previous_event_ids + [event.id],
            )
            result.append(client_deleted)

        return result
