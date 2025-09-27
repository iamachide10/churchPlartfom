from flask import Blueprint
print(">>> loading auth/__init__.py")
auth_bp = Blueprint("auth",__name__,url_prefix="/auth")

from . import routes
from . import other_routes
from . import refresh
print(">>> finished loading auth/__init__.py")







