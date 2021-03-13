from fastapi import FastAPI


def create_app():
    app = FastAPI()

    @app.get("/hello")
    def hello():
        return "Hello, World!"

    return app
