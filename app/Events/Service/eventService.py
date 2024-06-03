from app.models import Event
from app.schemas import CreateEvent, Event as EventSchema
from app.Events.Repository.eventRepo import Event, InterfaceEventRepository
from sqlalchemy.ext.asyncio import AsyncSession


class EventAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name

class EventNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

class EventIdNotFoundException(Exception):
    def __init__(self, Event_id: int):
        self.Event_id = Event_id

class NoEventsFoundException(Exception):
    def __init__(self):
        pass

class EventService():
    def __init__(self, Event_repo: InterfaceEventRepository):
        self.Event_repo = Event_repo
    async def create_Event(self, Event: CreateEvent):
        if await self.Event_repo.get_Event_by_name(Event.name):
            raise EventAlreadyExistsException(Event.name)
        else:
            await self.Event_repo.create_Event(Event)
            return {"message": "Event created successfully"}

        
    async def get_Events(self):
        if await self.Event_repo.get_Events() == []:
            raise NoEventsFoundException()
        else:
            Events = await self.Event_repo.get_Events()
            return Events

    async def get_Event_by_id(self, Event_id: int):
        if not await self.Event_repo.get_Event_by_id(Event_id):
            raise EventIdNotFoundException(Event_id)
        else:
            Event = await self.Event_repo.get_Event_by_id(Event_id)
            return Event
        
    async def delete_Event(self, Event_id: int):
        if not await self.Event_repo.get_Event_by_id(Event_id):
            raise EventIdNotFoundException(Event_id)
        else:
            await self.Event_repo.delete_Event_by_id(Event_id)
            return {"message": "Event deleted successfully"}
        
    async def get_Event_name_by_id(self, Event_id: int):
        if not await self.Event_repo.get_Event_by_id(Event_id):
            raise EventIdNotFoundException(Event_id)
        else:
            Event = await self.Event_repo.get_Event_by_id(Event_id)
            return Event.name