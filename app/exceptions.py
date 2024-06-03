
from fastapi.responses import JSONResponse


class EntityNotFoundException(Exception):
    def __init__(self, message: str):
        self.message=message


async def entity_not_found_exception(request, e: EntityNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"message": f"{e.message}"}
    )