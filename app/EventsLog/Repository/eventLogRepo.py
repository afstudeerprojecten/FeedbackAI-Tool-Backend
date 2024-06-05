from dataclasses import dataclass
from app.models import EventLog
from app.schemas import CreateEventLog, EventLog as EventLogSchema
from sqlalchemy import select
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional, Protocol
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class InterfaceEventLogRepository(Protocol):
    async def create_EventLog(self, EventLog: CreateEventLog) -> EventLog:
        ...

    async def get_EventLogs(self) -> List[EventLogSchema]:
        ...

    async def get_EventLog_by_id(self, EventLog_id: int) -> Optional[EventLogSchema]:
        ...

    async def get_EventLog_by_name(self, EventLog_name: str) -> Optional[EventLogSchema]:
        ...

    async def delete_EventLog_by_id(self, EventLog_id: int) -> None:
        ...

    async def get_EventLogs_by_event_id(self, event_id: int) -> List[EventLogSchema]:
        ...

    async def get_EventLog_by_user_id(self, user_id: int) -> List[EventLogSchema]:
        ...



@dataclass
class EventLogRepository:
    session: AsyncSession
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_EventLog(self, EventLog: CreateEventLog) -> EventLog:
        new_EventLog = EventLog(event_id=EventLog.event_id, user_id=EventLog.user_id, value=EventLog.value)
        self.session.add(new_EventLog)
        await self.session.commit()
        return new_EventLog
    
    async def get_EventLogs(self) -> List[EventLogSchema]:
        result = await self.session.execute(select(EventLog))
        EventLogs = [EventLogSchema.from_orm(EventLog) for EventLog in result.scalars()]
        return EventLogs
    
    async def get_EventLog_by_id(self, EventLog_id: int) -> Optional[EventLogSchema]:
        result = await self.session.execute(
            select(EventLog).where(EventLog.id == EventLog_id)
        )
        eventLog = result.scalars().first()
        if eventLog:
            return EventLogSchema.from_orm(eventLog)
        return None
    
    async def get_EventLog_by_name(self, EventLog_name: str) -> Optional[EventLogSchema]:
        result = await self.session.execute(
            select(EventLog).where(EventLog.name == EventLog_name)
        )
        eventLog = result.scalars().first()
        if eventLog:
            return EventLogSchema.from_orm(eventLog)
        return None
    
    async def delete_EventLog_by_id(self, EventLog_id: int) -> None:
        result = await self.session.execute(
            select(EventLog).where(EventLog.id == EventLog_id)
            )
        eventLog = result.scalars().first()        
        if eventLog:
            await self.session.delete(eventLog)
            await self.session.commit()
    
    async def get_EventLogs_by_event_id(self, event_id: int) -> List[EventLogSchema]:
        result = await self.session.execute(
            select(EventLog).where(EventLog.event_id == event_id)
        )
        EventLogs = [EventLogSchema.from_orm(EventLog) for EventLog in result.scalars()]
        return EventLogs
    
    async def get_EventLog_by_user_id(self, user_id: int) -> List[EventLogSchema]:
        result = await self.session.execute(
            select(EventLog).where(EventLog.user_id == user_id)
        )
        EventLogs = [EventLogSchema.from_orm(EventLog) for EventLog in result.scalars()]
        return EventLogs

    # async def update_EventLog(self, EventLog_id: int, EventLog_data: UpdateEventLog) -> Optional[EventLogSchema]:
    #     result = await self.session.execute(
    #         select(EventLog).where(EventLog.id == EventLog_id)
    #     )
    #     EventLog = result.scalars().first()
    #     if not EventLog:
    #         return None

    #     # Update only the provided fields from EventLog_data
    #     for key, value in EventLog_data.dict(exclude_unset=True).items():
    #         setattr(EventLog, key, value)

    #     await self.session.commit()
    #     # Refresh the EventLog object to reflect the changes in the database
    #     await self.session.refresh(EventLog)
    #     return EventLogSchema.from_orm(EventLog)
