from fastapi.openapi.utils import get_openapi
from json import dump
from api.main import app

docs = get_openapi(
    title=app.title,
    version=app.version,
    description=app.description,
    routes=app.routes,
)

with open("docs/openapi.json", "w") as f:
    dump(docs, f, indent=4)
