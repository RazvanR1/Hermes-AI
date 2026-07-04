from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import health, brain, tasks, dashboard, copilot, copilot_actions, context, reasoning, planner, copilot_execute

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
app.include_router(copilot_actions.router)
app.include_router(context.router)
app.include_router(reasoning.router)
app.include_router(planner.router)
app.include_router(copilot_execute.router)

# API v1 routes
app.include_router(health.router, prefix="/api/v1")
app.include_router(brain.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(dashboard.router, prefix="/api/v1")
app.include_router(copilot.router, prefix="/api/v1")
app.include_router(copilot_actions.router, prefix="/api/v1")
app.include_router(context.router, prefix="/api/v1")
app.include_router(reasoning.router, prefix="/api/v1")
app.include_router(planner.router, prefix="/api/v1")
app.include_router(copilot_execute.router, prefix="/api/v1")
