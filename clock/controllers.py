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
    return {"total_seconds": state['total_seconds'],
            "last_service": state['last_service'],
            "services_count": state['services_count']}


@app.route("/AddInfo", methods=["PUT"])
async def index(request):
    service_count = request.args.get("service_count")
    last_service = request.args.get("last_service")
    release_day = datetime.datetime.strptime(request.args.get("release_day"), "%d.%m.%Y %X")

    with open(r"..\clock_pusher\state.bd", 'r') as f:
        state = json.load(f)

    now = datetime.datetime.now()
    total_seconds = int((now - release_day).total_seconds())
    print(total_seconds)

    state['total_seconds'] = total_seconds
    state['last_service'] = last_service
    state['services_count'] = service_count
    state['revision'] = int(state['revision']) + 1
    with open(r"..\clock_pusher\state.bd", 'w') as f:
        json.dump(state, f)
    return response.json(state, status=200)
