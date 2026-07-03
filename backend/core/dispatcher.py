from core.router import route

def dispatch(request: str):
    r = route(request)
    return r
