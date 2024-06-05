from app.models import EventLog
from app.schemas import CreateEventLog, EventLog as EventLogSchema
from app.EventsLog.Repository.eventLogRepo import EventLog, InterfaceEventLogRepository
from sqlalchemy.ext.asyncio import AsyncSession


class EventLogAlreadyExistsException(Exception):
    def __init__(self, name: str):
        self.name = name

class EventLogNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name

class EventLogIdNotFoundException(Exception):
    def __init__(self, EventLog_id: int):
        self.EventLog_id = EventLog_id

class NoEventLogsFoundException(Exception):
    def __init__(self):
        pass

class UserNotFoundException(Exception):
    def __init__(self, id: int):
        self.id = id

class EventNotFoundException(Exception):
    def __init__(self, id: int):
        self.id = id

class EventLogService():
    def __init__(self, EventLog_repo: InterfaceEventLogRepository):
        self.EventLog_repo = EventLog_repo
    async def create_EventLog(self, EventLog: CreateEventLog):
        await self.EventLog_repo.create_EventLog(EventLog)
        return {"message": "EventLog created successfully"}

        
    async def get_EventLogs(self):
        if await self.EventLog_repo.get_EventLogs() == []:
            raise NoEventLogsFoundException()
        else:
            EventLogs = await self.EventLog_repo.get_EventLogs()
            return EventLogs

    async def get_EventLog_by_id(self, EventLog_id: int):
        if not await self.EventLog_repo.get_EventLog_by_id(EventLog_id):
            raise EventLogIdNotFoundException(EventLog_id)
        else:
            EventLog = await self.EventLog_repo.get_EventLog_by_id(EventLog_id)
            return EventLog
        
    async def get_EventLog_by_name(self, EventLog_name: str):
        if not await self.EventLog_repo.get_EventLog_by_name(EventLog_name):
            raise EventLogIdNotFoundException(EventLog_name)
        else:
            EventLog = await self.EventLog_repo.get_EventLog_by_id(EventLog_name)
            return EventLog
        
    async def delete_EventLog(self, EventLog_id: int):
        if not await self.EventLog_repo.get_EventLog_by_id(EventLog_id):
            raise EventLogIdNotFoundException(EventLog_id)
        else:
            await self.EventLog_repo.delete_EventLog_by_id(EventLog_id)
            return {"message": "EventLog deleted successfully"}
        
    async def get_EventLogs_by_event_id(self, event_id: int):
        if await self.EventLog_repo.get_EventLogs_by_event_id(event_id)==[]:
            raise EventNotFoundException(event_id)
        else:
            EventLog = await self.EventLog_repo.get_EventLogs_by_event_id(event_id)
            return EventLog
        
    async def get_EventLog_by_user_id(self, user_id: int):
        if await self.EventLog_repo.get_EventLog_by_user_id(user_id)==[]:
            raise UserNotFoundException(user_id)
        else:
            EventLog = await self.EventLog_repo.get_EventLog_by_user_id(user_id)
            return EventLog