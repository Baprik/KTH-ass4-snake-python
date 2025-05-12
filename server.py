import logging
import os
import typing

from pyngrok import ngrok
from flask import Flask
from flask import request


def run_server(handlers: typing.Dict):
    app = Flask("Battlesnake")

    @app.get("/")
    def on_info():
        return handlers["info"]()

    @app.post("/start")
    def on_start():
        game_state = request.get_json()
        handlers["start"](game_state)
        return "ok"

    @app.post("/move")
    def on_move():
        game_state = request.get_json()
        return handlers["move"](game_state)

    @app.post("/end")
    def on_end():
        game_state = request.get_json()
        handlers["end"](game_state)
        return "ok"

    @app.after_request
    def identify_server(response):
        response.headers.set(
            "server", "battlesnake/replit/starter-snake-python"
        )
        return response

    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))

    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    # Set up ngrok for local development
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        public_url = ngrok.connect(port)
        print(f"Public Battlesnake URL: {public_url}")

    print(f"\nRunning Battlesnake at http://{host}:{port}")
    app.run(host=host, port=port,debug=True, use_reloader=True)
