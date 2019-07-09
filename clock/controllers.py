from sanic import response
from clock import jinja
from clock import app
import json


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
    seconds = request.args.get("seconds")
    minutes = request.args.get("minutes")
    hours = request.args.get("hours")
    days = request.args.get("days")
    with open(r"..\clock_pusher\state.bd", 'r') as f:
        state = json.load(f)
    state['total_seconds'] = int(seconds) + int(minutes) * 60 + int(hours) * 3600 + int(days) * 3600 * 24
    state['last_service'] = last_service
    state['services_count'] = service_count
    state['revision'] = int(state['revision']) + 1
    with open(r"..\clock_pusher\state.bd", 'w') as f:
        json.dump(state, f)
    return response.json(state, status=200)
