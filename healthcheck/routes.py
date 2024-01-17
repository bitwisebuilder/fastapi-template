from fastapi import APIRouter
from fastapi import Request
from starlette.responses import JSONResponse

router = APIRouter()


@router.get("/")
async def rualive(request: Request):
    return JSONResponse(content={
        "status": "OK"
    }, status_code=200)
