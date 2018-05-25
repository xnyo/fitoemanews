from aiohttp import web

from utils.singletons import singleton


@singleton
class EmaNews:
    def __init__(self):
        self.app: web.Application = None
        self.setup_web_app()

    def setup_web_app(self):
        from api.handlers import ping
        self.app: web.Application() = web.Application()
        self.app.add_routes([
            web.get("/api/v1/ping", ping.handle)
        ])

    def start(self):
        web.run_app(self.app)
