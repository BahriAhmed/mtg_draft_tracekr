from fastapi import FastAPI
from draft_tracker_system.routes.user_routes import router as user_router

app = FastAPI()

app.include_router(user_router)