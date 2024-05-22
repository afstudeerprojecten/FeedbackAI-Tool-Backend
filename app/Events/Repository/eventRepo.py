from dataclasses import dataclass
from app.models import Event
from app.schemas import CreateEvent, Event as EventSchema
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Protocol

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class InterfaceEventRepository(Protocol):
    async def create_Event(self, Event: CreateEvent) -> Event:
        ...

    async def get_Events(self) -> List[EventSchema]:
        ...

    async def get_Event_by_id(self, Event_id: int) -> Optional[EventSchema]:
        ...

    async def delete_Event_by_id(self, Event_id: int) -> None:
        ...



@dataclass
class EventRepository:
    session: AsyncSession
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_Event(self, Event: CreateEvent) -> Event:
        hashed_password = pwd_context.hash(Event.password)
        new_Event = Event(name=Event.name, lastname=Event.lastname, email=Event.email, password=hashed_password, organisation_id=Event.organisation_id)
        self.session.add(new_Event)
        await self.session.commit()
        return new_Event
    
    async def get_Events(self) -> List[EventSchema]:
        result = await self.session.execute(select(Event))
        Events = [EventSchema.from_orm(Event) for Event in result.scalars()]
        return Events
    
    async def get_Event_by_id(self, Event_id: int) -> Optional[EventSchema]:
        result = await self.session.execute(
            select(Event).where(Event.id == Event_id)
        )
        Event = result.scalars().first()
        if Event:
            return EventSchema.from_orm(Event)
        return None
    
    async def delete_Event_by_id(self, Event_id: int) -> None:
        result = await self.session.execute(
            select(Event).where(Event.id == Event_id)
            )
        Event = result.scalars().first()        
        if Event:
            await self.session.delete(Event)
            await self.session.commit()
    

    # async def update_Event(self, Event_id: int, Event_data: UpdateEvent) -> Optional[EventSchema]:
    #     result = await self.session.execute(
    #         select(Event).where(Event.id == Event_id)
    #     )
    #     Event = result.scalars().first()
    #     if not Event:
    #         return None

    #     # Update only the provided fields from Event_data
    #     for key, value in Event_data.dict(exclude_unset=True).items():
    #         setattr(Event, key, value)

    #     await self.session.commit()
    #     # Refresh the Event object to reflect the changes in the database
    #     await self.session.refresh(Event)
    #     return EventSchema.from_orm(Event)
