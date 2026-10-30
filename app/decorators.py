from functools import wraps
from flask import request, abort

def wymagany_parametr(nazwa):
    def decorator(widok):
        @wraps(widok)
        def opakowana(*args, **kwargs):
            if request.args.get(nazwa) is None:
                abort(400, description=f"Brak parametru {nazwa}")
            return widok(*args, **kwargs)
        return opakowana
    return decorator
