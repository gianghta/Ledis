from urllib.parse import unquote_plus

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response
from starlette.routing import Route, Mount
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from ledis.cli import CLI
from ledis.exceptions import InvalidUsage


templates = Jinja2Templates(directory="templates")
cli = CLI()


async def homepage(request):
    return templates.TemplateResponse("index.html", {"request": request})


async def command_page(request):
    body = await request.body()
    body_str = unquote_plus(body.decode("utf-8"))

    if "=" not in body_str:
        raise InvalidUsage("Invalid command format")

    query = body_str.split("=", 1)[-1].strip()
    return Response(str(cli.call(query)))


routes = [
    Route("/", endpoint=homepage),
    Route("/command", endpoint=command_page, methods=["POST"]),
    Mount("/static", StaticFiles(directory="static"), name="static"),
]

middleware = [
    Middleware(
        CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
    )
]


async def http_exception(request, exc):
    return Response(f"[ERROR] {exc.detail}", status_code=exc.status_code)


app = Starlette(
    debug=True,
    routes=routes,
    exception_handlers={HTTPException: http_exception},
    middleware=middleware,
)
