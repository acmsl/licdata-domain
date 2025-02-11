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
    ClientUpdated,
    DeleteClientRequested,
    FindClientByIdRequested,
    ListClientsRequested,
    MatchingClientFound,
    MatchingClientsFound,
    NewClientCreated,
    NewClientRequested,
    NoMatchingClientsFound,
    UpdateClientRequested,
)
from pythoneda.shared import (
    attribute,
    Entity,
    Event,
    EventListener,
    EventReference,
    listen,
    Ports,
    primary_key_attribute,
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
        eventHistory: List[EventReference] = [],
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
        :param eventHistory: The event history.
        :type eventHistory: List[pythoneda.shared.EventReference]
        """
        self._email = email
        self._address = address
        self._contact = contact
        self._phone = phone
        super().__init__(eventHistory=eventHistory)
        print(f"email: {email}, address: {address}, contact: {contact}, phone: {phone}")

    @classmethod
    def empty(cls):
        """
        Builds an empty instance. Required for unmarshalling.
        :return: An empty instance.
        :rtype: pythoneda.ValueObject
        """
        return cls(email="[not-set]")

    def apply_updated(self, event: ClientUpdated):
        """
        Applies given updated event.
        :param event: The updated event.
        :type event: org.acmsl.licdata.events.clients.ClientUpdated
        """
        print(f"Applying updated event: {event}")
        self._address = event.address
        self._contact = event.contact
        self._phone = event.phone
        self._annotate_event(event)

    @classmethod
    def _create_instance_from(cls, event: NewClientRequested):
        """
        Creates a new instance from a NewClientRequested event.
        :param event: The event.
        :type event: org.acmsl.licdata.events.NewClientRequested
        :return: A new instance.
        :rtype: org.acmsl.licdata.Client
        """
        return cls(
            email=event.email,
            address=event.address,
            contact=event.contact,
            phone=event.phone,
            eventHistory=[EventReference(event.id, event.__class__.__name__)],
        )

    def create_created_event(
        self, createRequested: NewClientRequested
    ) -> NewClientCreated:
        """
        Creates a new client created event.
        :param createRequested: The request.
        :type createRequested: org.acmsl.licdata.events.NewClientRequested
        :return: The event.
        :rtype: org.acmsl.licdata.events.NewClientCreated
        """
        return NewClientCreated(
            entityId=self.id,
            email=self.email,
            address=self.address,
            contact=self.contact,
            phone=self.phone,
            previousEventIds=(
                createRequested.previous_event_ids + [createRequested.id]
            ),
        )

    def create_deleted_event(
        self, deleteRequest: DeleteClientRequested
    ) -> ClientDeleted:
        """
        Creates a deleted event.
        :param deleteRequest: The request.
        :type deleteRequest: org.acmsl.licdata.events.DeleteClientRequested
        :return: The event.
        :rtype: org.acmsl.licdata.events.ClientDeleted
        """
        return ClientDeleted(
            entityId=self.id,
            email=self.email,
            address=self.address,
            contact=self.contact,
            phone=self.phone,
            previousEventIds=deleteRequest.previous_event_ids + [deleteRequest.id],
        )

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
            result.append(repo.insert(newClientRequested))
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
    @listen(FindClientByIdRequested)
    async def listen_FindClientByIdRequested(
        cls, event: FindClientByIdRequested
    ) -> List[Event]:
        """
        Receives an event requesting a client by its id.
        :param event: The request.
        :type event: org.acmsl.licdata.events.FindClientByIdRequested
        :return: The event representing the outcome of the operation.
        :rtype event: List[pythoneda.shared.Event]
        """
        from .client_repo import ClientRepo

        result = []

        repo = Ports.instance().resolve_first(ClientRepo)

        existing_client = repo.find_by_id(event.entity_id)

        if existing_client is None:
            no_matching_clients_found = NoMatchingClientsFound(
                {}, event.previous_event_ids + [event.id]
            )
            result.append(no_matching_clients_found)
        else:
            result.append(
                MatchingClientFound(
                    existing_client,
                    event.previous_event_ids + [event.id],
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

        result = []

        repo = Ports.instance().resolve_first(ClientRepo)

        result.append(repo.delete(event))

        return result

    @classmethod
    @listen(UpdateClientRequested)
    async def listen_UpdateClientRequested(
        cls, updateClientRequested: UpdateClientRequested
    ) -> List[Event]:
        """
        Receives an event requesting updating a client.
        :param updateClientRequested: The request.
        :type updateClientRequested: org.acmsl.licdata.events.UpdateClientRequested
        :return: The event representing the request to update a client.
        :rtype event: List[pythoneda.shared.Event]
        """
        from .client_repo import ClientRepo

        result = []

        cls.logger().info(f"Update client requested: {updateClientRequested}")

        repo = Ports.instance().resolve_first(ClientRepo)

        existing_client = repo.find_by_id(updateClientRequested.entity_id)

        if existing_client is None:
            result.append(
                NoMatchingClientsFound(
                    id=updateClientRequested.entity_id,
                    previousEventIds=(
                        updateClientRequested.previous_event_ids
                        + [updateClientRequested.id]
                    ),
                )
            )
        else:
            result.append(repo.update(updateClientRequested))

        return result
