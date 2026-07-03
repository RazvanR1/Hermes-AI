def run(request: str = ""):
    from brain.orchestrator import handle
    return handle(request)
