from dataclasses import dataclass
from app.models import Event
from app.schemas import CreateEvent, Event as EventSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Protocol


class InterfaceEventRepository(Protocol):
    async def create_Event(self, Event: CreateEvent) -> Event:
        ...

    async def get_Events(self) -> List[EventSchema]:
        ...

    async def get_Event_by_id(self, Event_id: int) -> Optional[EventSchema]:
        ...

    async def get_Event_by_name(self, Event_name: str) -> Optional[EventSchema]:
        ...

    async def delete_Event_by_id(self, Event_id: int) -> None:
        ...



@dataclass
class EventRepository:
    session: AsyncSession
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_Event(self, event: CreateEvent) -> Event:
        new_Event = Event(name=event.name)
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
        event = result.scalars().first()
        if event:
            return EventSchema.from_orm(event)
        return None
    
    async def get_Event_by_name(self, Event_name: str) -> Optional[EventSchema]:
        result = await self.session.execute(
            select(Event).where(Event.name == Event_name)
        )
        event = result.scalars().first()
        if event:
            return EventSchema.from_orm(event)
        return None

    async def delete_Event_by_id(self, Event_id: int) -> None:
        result = await self.session.execute(
            select(Event).where(Event.id == Event_id)
            )
        event = result.scalars().first()        
        if event:
            await self.session.delete(event)
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
