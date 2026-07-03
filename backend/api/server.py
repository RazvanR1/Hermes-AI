from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import health, brain, tasks, dashboard, copilot

app = FastAPI(title="Hermes API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Legacy routes
app.include_router(health.router)
app.include_router(brain.router)
app.include_router(tasks.router)
app.include_router(dashboard.router)
app.include_router(copilot.router)

# API v1 routes
app.include_router(health.router, prefix="/api/v1")
app.include_router(brain.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(copilot.router, prefix="/api/v1")
