from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from conf.settings import Settings
from healthcheck import routes as healthcheck_routes

app = FastAPI(debug=Settings.DEBUG)

origins = Settings.CORS_ORIGINS

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(healthcheck_routes.router, prefix="/healthcheck")
