from functools import partial
from fastapi import FastAPI

from src.main.di import init_dependencies
from src.main.routers import init_routers


def create_app() -> FastAPI:
    app = FastAPI()
    app.on_event("startup")(partial(init_dependencies, app))
    init_routers(app)

    return app


def main():
    import uvicorn
    from src.utils.settings import SystemSettings

    settings = SystemSettings()
    app = create_app()

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
