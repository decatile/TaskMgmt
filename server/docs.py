from os import makedirs
from pathlib import Path
from sys import stdout
from fastapi.openapi.utils import get_openapi
from json import dump
from argparse import ArgumentParser
from api.main import app

docs = get_openapi(
    title=app.title,
    version=app.version,
    description=app.description,
    routes=app.routes,
)

p = ArgumentParser()
p.add_argument("--output", default=None)
n = p.parse_args()

f = stdout
if n.output is not None:
    path = Path(n.output)
    makedirs(path.parent, exist_ok=True)
    f = open(path, "w")

dump(docs, f, indent=4)
