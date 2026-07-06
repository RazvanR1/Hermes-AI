from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import (
    health,
    brain,
    tasks,
    dashboard,
    copilot,
    copilot_actions,
    context,
    reasoning,
    planner,
    copilot_execute,
    agents,
    missions,
    approval,
    tools,
    docker_tools,
    tool_dispatcher,
    executor,
    inventory,
    health_live,
    planner_v2,
    missionlog,
)

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
app.include_router(agents.router)
app.include_router(missions.router)
app.include_router(approval.router)
app.include_router(tools.router)
app.include_router(docker_tools.router)
app.include_router(tool_dispatcher.router)
app.include_router(executor.router)
app.include_router(inventory.router)
app.include_router(health_live.router)

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
app.include_router(agents.router, prefix="/api/v1")
app.include_router(missions.router, prefix="/api/v1")
app.include_router(approval.router, prefix="/api/v1")
app.include_router(tools.router, prefix="/api/v1")
app.include_router(docker_tools.router, prefix="/api/v1")
app.include_router(tool_dispatcher.router, prefix="/api/v1")
app.include_router(executor.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(health_live.router, prefix="/api/v1")

app.include_router(missionlog.router)
app.include_router(missionlog.router, prefix="/api/v1")

app.include_router(planner_v2.router)
app.include_router(planner_v2.router, prefix="/api/v1")
