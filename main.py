from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cms.v1 import routes as v1_video_routes
from conf.settings import Settings
from healthcheck import routes as healthcheck_routes
from iam.routes.v1 import routes as v1_auth_routes

load_dotenv()

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
app.include_router(v1_video_routes.router, prefix="/api/v1/cms")
app.include_router(v1_auth_routes.router, prefix="/api/v1/iam")
