from typing import Callable
from fastapi import HTTPException
from src.core.exceptions import (
    DoesNotExists, UniqueConstraint
)
async def response (*, func: Callable, **kwargs):
    try:
        return await func(**kwargs)
    except DoesNotExists as e:
        print(e)
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except UniqueConstraint as e:
        print(e)
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )