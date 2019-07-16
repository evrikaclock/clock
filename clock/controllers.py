from sanic import response
from clock import jinja
from clock import app
import json
import datetime


@app.route("/", methods=["GET"])
@jinja.template("index.html")
async def index(_):
    with open(r"..\clock_pusher\state.bd", 'r') as f:
        state = json.load(f)

    release_day = datetime.datetime.strptime(state["release_day"], "%d.%m.%Y %X")
    now = datetime.datetime.now()
    total_seconds = int((now - release_day).total_seconds())

    return {"total_seconds": total_seconds,
            "last_service": state['last_service'],
            "services_count": state['services_count']}


@app.route("/AddInfo", methods=["PUT"])
async def index(request):
    service_count = request.args.get("service_count")
    last_service = request.args.get("last_service")
    release_day = request.args.get("release_day")

    with open(r"..\clock_pusher\state.bd", 'r') as f:
        state = json.load(f)

    state['release_day'] = release_day
    state['last_service'] = last_service
    state['services_count'] = service_count
    state['revision'] = int(state['revision']) + 1
    with open(r"..\clock_pusher\state.bd", 'w') as f:
        json.dump(state, f)
    return response.json(state, status=200)
