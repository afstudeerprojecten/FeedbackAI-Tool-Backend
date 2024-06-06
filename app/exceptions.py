
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


class EntityNotFoundException(Exception):
    """
    Called when not found...
    """
    def __init__(self, message: str):
        self.message=message

class EntityAlreadyExistsException(Exception):
    """
    Called when it already exists... Programmer should have checked before calling this function.
    """
    def __init__(self, message: str):
        self.message=message

class EntityValidationException(Exception):
    """
    Callsed when validation fails...
    """
    def __init__(self, message: str):
        self.message=message

async def entity_not_found_handler(request, e: EntityNotFoundException):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"message": f"{e.message}"})
    )

async def entity_already_exists_handler(request, e: EntityAlreadyExistsException):
    return JSONResponse(
        status_code=409,
        content=jsonable_encoder({"message": f"{e.message}"})
    )

async def entity_validation_handler(request, e: EntityValidationException):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"message": f"{e.message}"})
    )
