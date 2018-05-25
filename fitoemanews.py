from aiohttp import web

from api.handlers import ping


def main():
    app = web.Application()
    app.add_routes([
        web.get("/api/v1/ping", ping.handle),
        # web.post("/api/v1/test", ping.handle_test)
    ])
    web.run_app(app)


if __name__ == '__main__':
    main()
