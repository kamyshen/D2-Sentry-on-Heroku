import os
import sentry_sdk
from bottle import Bottle, route, run
from sentry_sdk.integrations.bottle import BottleIntegration

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[BottleIntegration()]
)

app = Bottle()


@app.route("/success")
def index():
    html: str = 'Success!'
    return html


@app.route("/fail")
def err():
    raise RuntimeError("There is an error!")
    return


if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host="localhost", port=8080, debug=True)
